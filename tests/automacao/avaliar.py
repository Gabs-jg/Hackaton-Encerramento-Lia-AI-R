"""Avalia uma coleta já salva com regras numéricas, juiz e revisões humanas.
Consolida casos e pares, gera relatórios e mantém o parecer oficial pendente.
Este arquivo não envia mensagens à Lia.
"""

import argparse
from collections import Counter, defaultdict
import json
import hashlib
import importlib.metadata
import math
from pathlib import Path
import uuid

from .executar import RAIZ
from .funcional import avaliar_turno, status_conjunto
from .golden import digest
from .registros import Registros


def carregar_config(caminho, dataset):
    config = json.loads(caminho.read_text(encoding="utf-8-sig"))
    if not dataset.get("golden_sha256") or config["golden_sha256"] != dataset["golden_sha256"]:
        raise ValueError(
            "Configuração numérica pertence a outro golden. Revisar antes de trocar o hash."
        )
    limites = config["go_no_go"]
    for k in ("aprovacao_minima", "cobertura_minima"):
        if (
            type(limites[k]) not in (int, float)
            or not math.isfinite(limites[k])
            or not 0 <= limites[k] <= 1
        ):
            raise ValueError("Threshold inválido: " + k)
    for k in ("max_falhas_criticas", "max_casos_instaveis", "repeticoes_minimas"):
        if type(limites[k]) is not int or limites[k] < (1 if k == "repeticoes_minimas" else 0):
            raise ValueError("Limite inválido: " + k)
    # O dataset da execução pode ser uma seleção. Validar chaves contra IDs do golden original
    # já conferido pelo adaptador; todas as regras são protegidas pelo hash do golden completo.
    from .funcional import ROTULOS

    for chave, regras in config["numeros_por_turno"].items():
        for campo, valor in regras.items():
            if campo not in {*ROTULOS, "preco_unico"} or type(valor) is not int or valor < 0:
                raise ValueError("Regra numérica inválida: " + chave)
    return config


def comparar_pares(dataset, casos, turnos, repeticoes, revisoes):
    resultados = []
    indice = {(c["id"], c["repeticao"]): c for c in casos}
    for par in dataset.get("pares_metamorficos", []):
        for repeticao in range(1, repeticoes + 1):
            lados = [indice.get((id_, repeticao)) for id_ in par["casos"]]
            chave = f'{par["id"]}/r{repeticao:02}'
            bases = [
                t for t in turnos if t["caso_id"] in par["casos"] and t["repeticao"] == repeticao
            ]
            hash_evidencias = digest(
                {"par": par, "evidencias": [(t["chave"], t["evidencia_sha256"]) for t in bases]}
            )
            relacao, motivo = (
                "inconclusivo",
                "Relação semântica requer revisão; não comparar textos literalmente.",
            )

            def valor(id_, campo):
                for t in bases:
                    if t["caso_id"] == id_ and t["turno"] == 1:
                        return next(
                            (n["obtido_centavos"] for n in t["numeros"] if n["campo"] == campo),
                            None,
                        )
                return None

            a, b = par["casos"]
            if par["id"] in ("PM01", "PM03", "PM04"):
                campos = (
                    ["preco_unico"]
                    if par["id"] == "PM01"
                    else ["subtotal", "desconto", "frete", "total"]
                )
                valores_a, valores_b = [valor(a, k) for k in campos], [valor(b, k) for k in campos]
                deltas = {"PM01": [0], "PM03": [0, 0, 600, 600], "PM04": [890, 4178, 0, -3288]}[
                    par["id"]
                ]
                if None not in valores_a + valores_b:
                    relacao = (
                        "passou"
                        if [y - x for x, y in zip(valores_a, valores_b)] == deltas
                        else "falhou"
                    )
                    motivo = f"Relação numérica em centavos: A={valores_a}; B={valores_b}; diferenças esperadas={deltas}. Os critérios individuais continuam obrigatórios."
            manual = revisoes.get(chave)
            if manual:
                if (
                    manual.get("evidencia_sha256") != hash_evidencias
                    or not manual.get("revisor")
                    or manual.get("confirmado") is not True
                    or manual.get("resultado") not in ("passou", "falhou", "inconclusivo")
                    or not manual.get("motivo")
                ):
                    raise ValueError("Revisão de par inválida: " + chave)
                relacao, motivo = manual["resultado"], manual["motivo"]
            status = [l["resultado"] if l else "inconclusivo" for l in lados]
            status.append(relacao)
            resultados.append(
                {
                    "chave": chave,
                    "par": par["id"],
                    "repeticao": repeticao,
                    "casos": par["casos"],
                    "evidencia_sha256": hash_evidencias,
                    "relacao": relacao,
                    "motivo": motivo,
                    "resultado": status_conjunto(status),
                    "revisor": manual.get("revisor") if manual else None,
                }
            )
    return resultados


def agregar(dataset, manifesto, turnos, config):
    casos = []
    for caso in dataset["casos"]:
        for repeticao in range(1, manifesto["repeticoes"] + 1):
            encontrados = [
                t for t in turnos if t["caso_id"] == caso["id"] and t["repeticao"] == repeticao
            ]
            status = [t["resultado"] for t in encontrados]
            if len(encontrados) != len(caso["turnos"]):
                status.append("inconclusivo")
            casos.append(
                {
                    "id": caso["id"],
                    "categoria": caso["categoria"],
                    "repeticao": repeticao,
                    "resultado": status_conjunto(status),
                    "turnos_planejados": len(caso["turnos"]),
                    "turnos_avaliados": len(encontrados),
                    "revisao_humana": any(t["revisao_humana"] for t in encontrados)
                    or not encontrados,
                    "falha_critica": any(
                        t["resultado"] == "falhou" and t["severidade_sugerida"] == "crítico"
                        for t in encontrados
                    ),
                }
            )
    contagens = Counter(c["resultado"] for c in casos)
    conclusivos = contagens["passou"] + contagens["falhou"]
    por_caso = defaultdict(set)
    for c in casos:
        por_caso[c["id"]].add(c["resultado"])
    instaveis = [id_ for id_, resultados in por_caso.items() if {"passou", "falhou"} <= resultados]
    limites = config["go_no_go"]
    taxa = contagens["passou"] / conclusivos if conclusivos else None
    cobertura = conclusivos / len(casos) if casos else 0
    bloqueios = []
    if taxa is None or taxa < limites["aprovacao_minima"]:
        bloqueios.append("aprovação abaixo do limite ou não calculável")
    if cobertura < limites["cobertura_minima"]:
        bloqueios.append("cobertura conclusiva insuficiente")
    if sum(c["falha_critica"] for c in casos) > limites["max_falhas_criticas"]:
        bloqueios.append("falhas críticas acima do limite")
    if len(instaveis) > limites["max_casos_instaveis"]:
        bloqueios.append("instabilidade acima do limite")
    if manifesto["repeticoes"] < limites["repeticoes_minimas"]:
        bloqueios.append("repetições insuficientes")
    if len(dataset["casos"]) != dataset["total_casos"]:
        bloqueios.append("seleção parcial do golden")
    if manifesto["modo"] != "api":
        bloqueios.append("replay não comprova execução atual/estabilidade")
    if any(c["revisao_humana"] for c in casos):
        bloqueios.append("revisões humanas pendentes")
    if dataset.get("status") != "aprovado":
        bloqueios.append("golden pendente de aprovação")
    if not config["juiz"].get("calibracao_aprovada"):
        bloqueios.append("calibração dos avaliadores pendente")
    if limites.get("provisorio", True):
        bloqueios.append("thresholds provisórios")
    return casos, {
        "planejados": len(casos),
        "passou": contagens["passou"],
        "falhou": contagens["falhou"],
        "inconclusivo": contagens["inconclusivo"],
        "denominador_aprovacao": conclusivos,
        "taxa_aprovacao": taxa,
        "cobertura_conclusiva": cobertura,
        "instaveis": instaveis,
        "por_categoria": {
            cat: dict(Counter(c["resultado"] for c in casos if c["categoria"] == cat))
            for cat in sorted({c["categoria"] for c in casos})
        },
        "simulacao_thresholds": "nao_atende" if bloqueios else "atende",
        "bloqueios": bloqueios,
        "parecer_oficial": "pendente_decisao_da_equipe",
    }


def montar_template_revisao(manifesto, turnos, pares):
    template = {"execucao_id": manifesto["id"], "turnos": {}, "pares": {}}
    for t in turnos:
        template["turnos"][t["chave"]] = {
            "evidencia_sha256": t["evidencia_sha256"],
            "confirmado": False,
            "revisor": "",
            "criterios": [
                {
                    "id": n,
                    "criterio": criterio,
                    "resultado": "inconclusivo",
                    "motivo": "",
                    "trechos_resposta": [],
                }
                for n, criterio in enumerate(t["criterios_esperados"], 1)
            ],
        }
    for p in pares:
        template["pares"][p["chave"]] = {
            "evidencia_sha256": p["evidencia_sha256"],
            "confirmado": False,
            "revisor": "",
            "resultado": "inconclusivo",
            "motivo": "",
        }
    return template


def salvar_resumo_avaliacao(saida, manifesto, casos, turnos, pares, consolidado):
    linhas = [
        "# T15/T16 — Avaliação provisória",
        "",
        f'Execução: `{manifesto["id"]}` · modo: **{manifesto["modo"]}**',
        "",
        "**Parecer oficial pendente.** Limites provisórios e julgamentos sujeitos a calibração/revisão.",
        "",
        f'Casos/repetições planejados: {len(casos)}. Passaram: {consolidado["passou"]}; falharam: {consolidado["falhou"]}; inconclusivos: {consolidado["inconclusivo"]}.',
        f'Aprovação: {consolidado["passou"]}/{consolidado["denominador_aprovacao"]} conclusivos. Inconclusivos não entram como aprovação ou defeito.',
        "",
        "Bloqueios da simulação: " + "; ".join(consolidado["bloqueios"]),
        "",
        "| Caso | Repetição | Turno | Resultado | Severidade sugerida | Evidência |",
        "|---|---:|---:|---|---|---|",
    ]
    for t in sorted(
        turnos,
        key=lambda x: (x["resultado"] != "falhou", x["caso_id"], x["repeticao"], x["turno"]),
    ):
        linhas.append(
            f'| {t["caso_id"]} | {t["repeticao"]} | {t["turno"]} | {t["resultado"]} | {t["severidade_sugerida"]} | [JSON](../../{t["arquivo"]}) |'
        )
    linhas += [
        "",
        "## Pares",
        "",
        "| Par/repetição | Relação | Resultado conjunto |",
        "|---|---|---|",
    ]
    linhas += [f'| {p["chave"]} | {p["relacao"]} | {p["resultado"]} |' for p in pares]
    linhas += [
        "",
        "As justificativas por critério, valores obtidos e limitações estão em [avaliacao.json](avaliacao.json).",
        "Preencher apenas entradas revisadas do template, manter os hashes e remover as demais antes de reaplicar.",
        "Falhas numéricas extraídas automaticamente também precisam de conferência; texto ambíguo não é reprovação automática.",
        "",
    ]
    (saida.pasta / "resumo.md").write_text("\n".join(linhas), encoding="utf-8")


def carregar_evidencia(pasta, tentativa, caso, casos_por_id):
    p = (pasta / tentativa["arquivo"]).resolve()
    if not p.is_relative_to(pasta.resolve()):
        raise ValueError("Evidência fora da pasta de execução.")
    registro = json.loads(p.read_text(encoding="utf-8"))
    if registro["caso_id"] != caso["id"] or registro["repeticao"] != caso["repeticao"]:
        raise ValueError("Registro não corresponde ao caso/repetição do resumo.")
    esperado = casos_por_id[registro["caso_id"]]["turnos"][registro["turno"] - 1]
    for campo in (
        "criterios_esperados",
        "contexto_oficial",
        "pontos_de_revisao",
        "referencias_nao_locais",
    ):
        if registro.get(campo, []) != esperado.get(campo, []):
            raise ValueError("Critério/referência do registro diverge do snapshot.")
    if registro["requisicao"]["mensagem"] != esperado["mensagem"]:
        raise ValueError("Entrada difere do golden executado.")
    return registro


def avaliar_pasta(pasta, config_path, revisao_path=None, juiz=None):
    dataset = json.loads((pasta / "dataset.json").read_text(encoding="utf-8"))
    manifesto = json.loads((pasta / "manifesto.json").read_text(encoding="utf-8"))
    resumo = json.loads((pasta / "resumo.json").read_text(encoding="utf-8"))
    if digest(dataset) != manifesto["dataset_sha256"]:
        raise ValueError("Snapshot de dataset alterado após execução.")
    config = carregar_config(config_path, dataset)
    revisoes = json.loads(revisao_path.read_text(encoding="utf-8-sig")) if revisao_path else {}
    if revisoes and revisoes.get("execucao_id") != manifesto["id"]:
        raise ValueError("Revisões de outra execução.")
    saida = Registros(pasta / "avaliacoes" / uuid.uuid4().hex[:12])
    from .juiz import RUBRICA, RUBRICA_VERSAO

    (saida.pasta / "rubrica.txt").write_text(RUBRICA, encoding="utf-8")
    if juiz:
        juiz.on_update = lambda: saida.salvar(
            "juiz-parcial.json",
            {
                "chamadas": juiz.chamadas,
                "custo_estimado_usd": juiz.custo_estimado,
                "registros": juiz.registros,
            },
        )
    casos_por_id = {c["id"]: c for c in dataset["casos"]}
    turnos, metricas = [], []
    for caso in resumo["casos"]:
        finais = {}
        for tentativa in caso["turnos"]:
            registro = carregar_evidencia(pasta, tentativa, caso, casos_por_id)
            # Todas as tentativas são preservadas, mas só o último 429 recuperado decide esse turno.
            anteriores = finais.get(registro["turno"])
            if anteriores and anteriores["http_status"] != 429:
                raise ValueError("Reexecução de resposta válida não pode substituir reprovação.")
            finais[registro["turno"]] = registro
            corpo = registro.get("resposta_api")
            if isinstance(corpo, dict):
                metricas.extend(corpo.get("metricas", []) or [])
        for registro in finais.values():
            chave = f'{registro["caso_id"]}/r{registro["repeticao"]:02}/t{registro["turno"]:02}'
            aval = avaliar_turno(registro, config, revisoes.get("turnos", {}).get(chave), juiz)
            aval["arquivo"] = next(
                t["arquivo"] for t in reversed(caso["turnos"]) if t["turno"] == registro["turno"]
            )
            turnos.append(aval)
            saida.salvar("turnos-parciais.json", turnos)
    desconhecidas = set(revisoes.get("turnos", {})) - {t["chave"] for t in turnos}
    if desconhecidas:
        raise ValueError("Revisão contém turno inexistente.")
    casos, consolidado = agregar(dataset, manifesto, turnos, config)
    pares = comparar_pares(
        dataset, casos, turnos, manifesto["repeticoes"], revisoes.get("pares", {})
    )
    if set(revisoes.get("pares", {})) - {p["chave"] for p in pares}:
        raise ValueError("Revisão contém par inexistente.")
    if any(p["resultado"] != "passou" for p in pares):
        consolidado["bloqueios"].append("pares metamórficos reprovados ou pendentes")
        consolidado["simulacao_thresholds"] = "nao_atende"
    template = montar_template_revisao(manifesto, turnos, pares)
    resultado = {
        "execucao_id": manifesto["id"],
        "modo": manifesto["modo"],
        "rubrica_versao": RUBRICA_VERSAO,
        "rubrica_sha256": digest(RUBRICA),
        "deepeval": importlib.metadata.version("deepeval"),
        "avaliador_codigo_sha256": {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in Path(__file__).parent.glob("*.py")
        },
        "golden_sha256": dataset["golden_sha256"],
        "config_sha256": digest(config),
        "status_config": config["status"],
        "casos": casos,
        "turnos": turnos,
        "pares": pares,
        "resumo": consolidado,
        "metricas_api_preservadas": metricas,
        "juiz": (
            {
                "chamadas": juiz.chamadas,
                "custo_estimado_usd": juiz.custo_estimado,
                "registros": juiz.registros,
            }
            if juiz
            else {"chamadas": 0, "custo_estimado_usd": 0}
        ),
    }
    saida.salvar("avaliacao.json", resultado)
    from .juiz import RUBRICA

    saida.salvar(
        "julgamentos.json",
        {
            "rubrica_sha256": digest(RUBRICA),
            "julgamentos": {
                t["evidencia_sha256"]: t["juiz"]
                for t in turnos
                if t.get("juiz")
                and not any(p.startswith("Saída do juiz inválida") for p in t["pendencias"])
            },
        },
    )
    saida.salvar("config.json", config)
    saida.salvar("revisao-template.json", template)
    if revisoes:
        saida.salvar("revisao-aplicada.json", revisoes)
    salvar_resumo_avaliacao(saida, manifesto, casos, turnos, pares, consolidado)
    return saida.pasta, resultado


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("execucao", type=Path)
    parser.add_argument(
        "--config", type=Path, default=RAIZ / "tests/automacao/config/avaliacao-provisoria.json"
    )
    parser.add_argument("--revisao", type=Path)
    parser.add_argument("--juiz", choices=("humano", "bedrock", "salvo"), default="humano")
    parser.add_argument(
        "--julgamentos", type=Path, help="Julgamentos salvos para reavaliar sem custo."
    )
    args = parser.parse_args(argv)
    try:
        juiz = None
        if args.juiz == "bedrock":
            from .juiz import JuizBedrock

            config_juiz = json.loads(args.config.read_text(encoding="utf-8-sig"))["juiz"]
            if args.julgamentos:
                from .julgamentos import JuizComCache, JuizSalvo

                salvo = JuizSalvo(args.julgamentos, config_juiz)
                juiz = JuizComCache(salvo, JuizBedrock(config_juiz))
            else:
                juiz = JuizBedrock(config_juiz)
        if args.julgamentos and args.juiz == "humano":
            raise ValueError("--julgamentos exige --juiz salvo ou bedrock.")
        if args.juiz == "salvo":
            if not args.julgamentos:
                raise ValueError("--juiz salvo exige --julgamentos.")
            from .julgamentos import JuizSalvo

            juiz = JuizSalvo(
                args.julgamentos, json.loads(args.config.read_text(encoding="utf-8-sig"))["juiz"]
            )
        pasta, resultado = avaliar_pasta(args.execucao.resolve(), args.config, args.revisao, juiz)
        print(f"Avaliação salva: {pasta}")
        print(json.dumps(resultado["resumo"], ensure_ascii=False))
        return 0
    except (ValueError, KeyError, OSError, ImportError) as exc:
        print(
            f"Avaliação não concluída: {type(exc).__name__}; confira configuração, dataset e revisões."
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
