"""Compara o juiz com rótulos propostos para exemplos controlados.
Salva divergências, respostas e consumo, sem considerar a calibração aprovada.
Só permite chamadas pagas quando a opção Bedrock é informada.
"""

import argparse
import json
from pathlib import Path
import uuid

from .funcional import validar_julgamento
from .golden import digest
from .juiz import JuizBedrock, RUBRICA, RUBRICA_VERSAO
from .registros import Registros


def validar_exemplos(dados):
    ids = set()
    for exemplo in dados["exemplos"]:
        id_ = exemplo["id"]
        r = exemplo["registro"]
        if id_ in ids or r["caso_id"] != id_:
            raise ValueError("ID de exemplo duplicado ou incompatível.")
        ids.add(id_)
        esperados = exemplo["rotulos_propostos"]
        if len(esperados) != len(r["criterios_esperados"]) or not esperados:
            raise ValueError("Cada critério precisa de um rótulo proposto.")
        if any(v not in ("passou", "falhou", "inconclusivo") for v in esperados):
            raise ValueError("Rótulo inválido.")
        if not exemplo.get("origem") or exemplo.get("revisao_humana") != "pendente":
            raise ValueError(
                "Identificar origem e manter a revisão humana pendente neste teste controlado."
            )
    if not ids:
        raise ValueError("Conjunto de calibração vazio.")


def executar_calibracao(dados, config, saida, juiz):
    validar_exemplos(dados)
    saida.salvar("exemplos.json", dados)
    saida.salvar("config.json", config)
    (saida.pasta / "rubrica.txt").write_text(RUBRICA, encoding="utf-8")
    juiz.on_update = lambda: saida.salvar(
        "juiz-parcial.json",
        {
            "chamadas": juiz.chamadas,
            "custo_estimado_usd": juiz.custo_estimado,
            "registros": juiz.registros,
        },
    )
    resultados = []
    for exemplo in dados["exemplos"]:
        registro = exemplo["registro"]
        item = {
            "id": exemplo["id"],
            "origem": exemplo["origem"],
            "registro_sha256": digest(registro),
            "rotulos_propostos": exemplo["rotulos_propostos"],
            "revisao_humana": "pendente",
        }
        try:
            julgamento = juiz.julgar(registro)
            criterios = validar_julgamento(
                julgamento, registro["criterios_esperados"], registro["resposta_api"]["resposta"]
            )
            item.update(julgamento=julgamento, rotulos_obtidos=[c["resultado"] for c in criterios])
            item["coincide_com_proposta"] = item["rotulos_obtidos"] == item["rotulos_propostos"]
        except Exception as exc:
            item["erro"] = type(exc).__name__
        resultados.append(item)
        saida.salvar("resultados-parciais.json", resultados)
        if item.get("erro"):
            break
    resultado = {
        "rubrica_versao": RUBRICA_VERSAO,
        "rubrica_sha256": digest(RUBRICA),
        "exemplos_sha256": digest(dados),
        "planejados": len(dados["exemplos"]),
        "avaliados": len(resultados),
        "concordantes_com_proposta": sum(r.get("coincide_com_proposta", False) for r in resultados),
        "chamadas": juiz.chamadas,
        "custo_estimado_usd": juiz.custo_estimado,
        "calibracao_humana_aprovada": False,
        "resultados": resultados,
    }
    saida.salvar("resultado.json", resultado)
    linhas = [
        "# Teste controlado da rubrica",
        "",
        "Estes exemplos verificam o juiz. Não são novos casos ou respostas da Lia; os rótulos são propostas pendentes de revisão humana.",
        "",
        "| Exemplo | Rótulos propostos | Rótulos obtidos | Concorda? |",
        "|---|---|---|---|",
    ]
    for r in resultados:
        linhas.append(
            f"| {r['id']} | {', '.join(r['rotulos_propostos'])} | {', '.join(r.get('rotulos_obtidos', [r.get('erro', 'não avaliado')]))} | {r.get('coincide_com_proposta', False)} |"
        )
    linhas += [
        "",
        f"Chamadas: {juiz.chamadas}. Custo estimado: US$ {juiz.custo_estimado:.7f}.",
        "",
        "[Julgamentos e justificativas](resultado.json) · [Exemplos](exemplos.json) · [Retornos brutos](juiz-parcial.json)",
        "",
        "Concordância nesta amostra não mede acurácia geral e não aprova automaticamente o juiz.",
    ]
    (saida.pasta / "resumo.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    return resultado


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exemplos", type=Path, required=True)
    parser.add_argument("--config", type=Path)
    parser.add_argument(
        "--bedrock", action="store_true", help="Permite chamadas pagas dentro do lote configurado."
    )
    parser.add_argument("--saida", type=Path, default=Path("results/automacao/calibracao"))
    args = parser.parse_args(argv)
    dados = json.loads(args.exemplos.read_text(encoding="utf-8-sig"))
    validar_exemplos(dados)
    if not args.bedrock:
        print(f"Exemplos válidos: {len(dados['exemplos'])}. Nenhuma chamada realizada.")
        return 0
    if not args.config:
        raise ValueError("--bedrock exige --config com limites do lote.")
    config = json.loads(args.config.read_text(encoding="utf-8-sig"))
    if len(dados["exemplos"]) > config["juiz"]["max_chamadas"]:
        raise ValueError("Quantidade de exemplos excede o limite de chamadas configurado.")
    saida = Registros(args.saida / uuid.uuid4().hex[:12])
    print(f"Registros: {saida.pasta}", flush=True)
    resultado = executar_calibracao(dados, config, saida, JuizBedrock(config["juiz"]))
    print(json.dumps({k: v for k, v in resultado.items() if k != "resultados"}, ensure_ascii=False))
    return 0 if resultado["concordantes_com_proposta"] == resultado["planejados"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
