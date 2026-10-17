"""Executa as conversas do dataset, uma mensagem por vez.
Mantém a sessão entre turnos, separa casos e repetições e salva cada tentativa.
A avaliação das regras do golden acontece depois, em avaliar.py.
"""

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import time
import uuid
from pathlib import Path

from .casos import carregar
from .cliente import ClienteLia, ClienteReplay, ClienteReplayGolden, ENDPOINT, agora
from .registros import Registros

RAIZ = Path(__file__).resolve().parents[2]


def sha256(conteudo):
    return hashlib.sha256(conteudo).hexdigest()


def chave_local(caminho):
    chave = os.environ.get("LIA_API_KEY", "").strip()
    if not chave and caminho.is_file():
        for linha in caminho.read_text(encoding="utf-8-sig").splitlines():
            nome, separador, valor = linha.strip().partition("=")
            if separador and nome.strip() == "LIA_API_KEY":
                chave = valor.strip().strip('"').strip("'")
                break
    if not chave or "\n" in chave or "\r" in chave:
        raise ValueError("Configurar LIA_API_KEY no ambiente ou no arquivo .env local.")
    return chave


def estado_transporte(registro):
    status, erro = registro["http_status"], registro["erro_tecnico"]
    if (
        status in (408, 429)
        or status is not None
        and status >= 500
        or erro in ("timeout", "conexao")
    ):
        return "inconclusivo_ambiente"
    if status is not None and 300 <= status < 500:
        return "erro_configuracao"
    if status != 200 or erro:
        return "erro_contrato"
    return "concluida"


def montar_requisicao(turno, sessao, prompt):
    payload = {"mensagem": turno["mensagem"]}
    if sessao:
        payload["sessao"] = sessao
    if prompt is not None:
        payload["prompt_sistema"] = prompt
    return payload


def enviar_turno(cliente, payload, turno):
    try:
        recebido = cliente.enviar(payload, turno)
    except Exception as exc:
        recebido = {
            "inicio_utc": agora(),
            "fim_utc": agora(),
            "http_status": None,
            "erro_tecnico": "executor",
            "tipo_excecao": type(exc).__name__,
            "resposta_api": None,
        }
    return recebido


def montar_evidencia(
    manifesto, caso, turno, *, numero, repeticao, tentativa, payload, historico, recebido
):
    registro = {
        "formato": "lia-evidencia-t15-v1",
        "execucao_id": manifesto["id"],
        "caso_id": caso["id"],
        "categoria": caso["categoria"],
        "turno": numero,
        "repeticao": repeticao,
        "tentativa": tentativa,
        "modo": manifesto["modo"],
        "versao_solicitada": manifesto["versao_solicitada"],
        "fase_base": manifesto["fase_base"],
        "requisicao": payload,
        "criterio_esperado": turno["criterio_esperado"],
        "referencias": turno.get("referencias", caso["referencias"]),
        "criterios_esperados": turno.get("criterios_esperados", [turno["criterio_esperado"]]),
        "contexto_oficial": turno.get("contexto_oficial", []),
        "referencias_nao_locais": turno.get("referencias_nao_locais", []),
        "pontos_de_revisao": turno.get("pontos_de_revisao", []),
        "data_referencia": turno.get("data_referencia"),
        "historico_conversa": list(historico),
        "resultado_funcional": "nao_avaliado",
        **recebido,
        "avisos": [],
    }
    return registro


def verificar_resposta(registro, recebido, manifesto, historico, sessao, sessoes, numero):
    from .avaliacao import avaliar_registro

    estado = (
        "erro_executor"
        if recebido.get("erro_tecnico") == "executor"
        else estado_transporte(registro)
    )
    corpo = registro.get("resposta_api")
    if estado == "concluida":
        try:
            registro["deepeval"] = avaliar_registro(registro, historico)
            if registro["deepeval"]["resultado_contrato"] != "passou":
                estado = "erro_contrato"
        except Exception as exc:
            estado = "erro_executor"
            registro["erro_avaliacao"] = type(exc).__name__
        if isinstance(corpo, dict):
            if "versao" not in corpo:
                registro["avisos"].append("versao ausente; versão retornada não confirmada")
            elif corpo["versao"] != manifesto["versao_solicitada"]:
                registro["avisos"].append("versao retornada difere da solicitada")
                estado = "erro_contrato"
            if sessao and corpo.get("sessao") != sessao:
                registro["avisos"].append("sessao retornada mudou dentro do mesmo caso")
                estado = "erro_contrato"
            if numero == 1 and corpo.get("sessao") in sessoes:
                registro["avisos"].append("sessao retornada reutilizada entre casos/repetições")
                estado = "erro_contrato"
    return estado


def executar(
    dataset,
    cliente,
    registros,
    manifesto,
    repeticoes=1,
    prompt=None,
    retentativas_429=0,
    espera=3,
    dormir=time.sleep,
):
    casos, sessoes = [], set()
    manifesto["estado"], manifesto["chamadas_api_tentadas"] = "em_andamento", 0
    registros.salvar("dataset.json", dataset)
    registros.salvar("manifesto.json", manifesto)
    try:
        for caso in dataset["casos"]:
            for repeticao in range(1, repeticoes + 1):
                sessao, historico = None, []
                resultado = {
                    "id": caso["id"],
                    "origem_exploracao": caso.get("origem_exploracao"),
                    "repeticao": repeticao,
                    "resultado_execucao": "em_andamento",
                    "turnos": [],
                }
                casos.append(resultado)
                for numero, turno in enumerate(caso["turnos"], 1):
                    payload = montar_requisicao(turno, sessao, prompt)
                    for tentativa in range(1, retentativas_429 + 2):
                        if manifesto["modo"] == "api":
                            manifesto["chamadas_api_tentadas"] += 1
                        # Persistir antes da chamada: interrupção externa pode impedir o finally.
                        registros.salvar("manifesto.json", manifesto)
                        recebido = enviar_turno(cliente, payload, turno)
                        registro = montar_evidencia(
                            manifesto,
                            caso,
                            turno,
                            numero=numero,
                            repeticao=repeticao,
                            tentativa=tentativa,
                            payload=payload,
                            historico=historico,
                            recebido=recebido,
                        )
                        estado = verificar_resposta(
                            registro, recebido, manifesto, historico, sessao, sessoes, numero
                        )
                        corpo = registro.get("resposta_api")
                        registro["resultado_execucao"] = estado
                        arquivo = f'{caso["id"]}/r{repeticao:02}/t{numero:02}-a{tentativa:02}.json'
                        registros.salvar(arquivo, registro)
                        resumo_turno = {
                            campo: registro.get(campo)
                            for campo in (
                                "turno",
                                "tentativa",
                                "http_status",
                                "resultado_execucao",
                                "avisos",
                            )
                        }
                        resumo_turno["arquivo"] = arquivo
                        if "deepeval" in registro:
                            resumo_turno["deepeval"] = {
                                k: v for k, v in registro["deepeval"].items() if k != "test_case"
                            }
                        resultado["turnos"].append(resumo_turno)
                        resultado["resultado_execucao"] = estado
                        registros.resumo(manifesto, casos)
                        # Somente 429 tem retry opcional. Timeout/5xx podem ter processado o turno.
                        if registro["http_status"] == 429 and tentativa <= retentativas_429:
                            dormir(espera)
                            continue
                        break
                    if estado != "concluida":
                        break  # Nunca envia T2 sem um T1 válido.
                    if numero == 1:
                        sessoes.add(corpo["sessao"])
                    sessao = corpo["sessao"]
                    historico += [
                        {"papel": "user", "conteudo": turno["mensagem"]},
                        {"papel": "assistant", "conteudo": corpo["resposta"]},
                    ]
                if resultado["resultado_execucao"] in ("erro_configuracao", "erro_executor"):
                    manifesto["estado"] = "interrompida_por_erro"
                    return casos
        manifesto["estado"] = "finalizada"
        return casos
    except BaseException:
        manifesto["estado"] = "interrompida"
        if casos:
            casos[-1]["resultado_execucao"] = "interrompida"
        raise
    finally:
        manifesto["fim_utc"] = agora()
        registros.salvar("manifesto.json", manifesto)
        registros.resumo(manifesto, casos)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="T15: coleta sequencial com DeepEval; avaliação funcional separada em tests.automacao.avaliar."
    )
    parser.add_argument("--dataset", type=Path, default=RAIZ / "datasets/pilotos/t15-piloto.json")
    parser.add_argument("--modo", choices=("replay", "api"), default="replay")
    parser.add_argument(
        "--replay-resultados", type=Path, help="Consolidado histórico T14; não faz chamadas."
    )
    parser.add_argument("--versao", choices=("original", "corrigida"), default="original")
    parser.add_argument("--prompt", type=Path)
    parser.add_argument("--env-file", type=Path, default=RAIZ / ".env")
    parser.add_argument("--saida", type=Path, default=RAIZ / "results/automacao")
    parser.add_argument("--fase-base", default="nao_confirmada")
    parser.add_argument("--repeticoes", type=int, default=1)
    parser.add_argument("--retentativas-429", type=int, choices=(0, 1, 2), default=0)
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--caso", action="append", help="ID do piloto; pode repetir a opção.")
    parser.add_argument(
        "--pares", action="store_true", help="Selecionar somente os casos dos pares metamórficos."
    )
    parser.add_argument(
        "--validar", action="store_true", help="Conferir formato sem executar ou exigir chave."
    )
    args = parser.parse_args(argv)
    try:
        if args.repeticoes < 1 or args.timeout <= 0:
            raise ValueError("Repetições e timeout devem ser positivos.")
        dataset = carregar(args.dataset, RAIZ)
        if args.pares:
            if args.caso or not dataset.get("pares_metamorficos"):
                raise ValueError("--pares exige pares no dataset e não combina com --caso.")
            selecionados = {id_ for par in dataset["pares_metamorficos"] for id_ in par["casos"]}
            dataset["casos"] = [c for c in dataset["casos"] if c["id"] in selecionados]
        if args.caso:
            existentes = {c["id"] for c in dataset["casos"]}
            if set(args.caso) - existentes:
                raise ValueError("ID selecionado não está no dataset.")
            dataset["casos"] = [c for c in dataset["casos"] if c["id"] in args.caso]
        if args.validar:
            turnos = sum(len(c["turnos"]) for c in dataset["casos"])
            print(
                f'Dataset provisório válido: {len(dataset["casos"])} casos, {turnos} turnos. Plano: {turnos * args.repeticoes} chamadas por versão, antes de retentativas. Nenhuma chamada realizada.'
            )
            return 0
        if args.modo == "replay" and (args.versao != "original" or args.repeticoes != 1):
            raise ValueError(
                "Replay usa somente a versão original e uma leitura; não é repetição independente."
            )
        if (args.versao == "corrigida") != bool(args.prompt):
            raise ValueError("Versão corrigida exige --prompt; original não recebe prompt_sistema.")
        prompt = args.prompt.read_text(encoding="utf-8-sig") if args.prompt else None
        if prompt is not None and not prompt.strip():
            raise ValueError("Arquivo de prompt vazio.")
        if args.replay_resultados and args.modo != "replay":
            raise ValueError("--replay-resultados exige --modo replay.")
        if (
            args.modo == "replay"
            and not args.replay_resultados
            and any("evidencia_replay" not in t for c in dataset["casos"] for t in c["turnos"])
        ):
            raise ValueError("Todos os turnos precisam de evidencia_replay para esse modo.")
        # Importar/verificar dependência antes de enviar qualquer requisição.
        from . import avaliacao  # noqa: F401

        chave = chave_local(args.env_file) if args.modo == "api" else ""
        if args.modo == "api":
            cliente = ClienteLia(chave, args.timeout)
        elif args.replay_resultados:
            cliente = ClienteReplayGolden(args.replay_resultados.resolve(), dataset)
        else:
            cliente = ClienteReplay(RAIZ)
        identificador = (
            agora().replace(":", "").replace(".", "-").replace("+0000", "Z")
            + "-"
            + uuid.uuid4().hex[:8]
        )
        try:
            commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=RAIZ, text=True, stderr=subprocess.DEVNULL
            ).strip()
            alterado = bool(
                subprocess.check_output(
                    ["git", "status", "--porcelain"], cwd=RAIZ, text=True
                ).strip()
            )
        except (OSError, subprocess.SubprocessError):
            commit, alterado = None, None
        manifesto = {
            "id": identificador,
            "tarefa": "T15",
            "modo": args.modo,
            "versao_solicitada": args.versao,
            "fase_base": args.fase_base,
            "inicio_utc": agora(),
            "dataset_sha256": sha256(
                json.dumps(dataset, ensure_ascii=False, sort_keys=True).encode()
            ),
            "prompt_sha256": sha256(prompt.encode()) if prompt is not None else None,
            "commit": commit,
            "codigo_com_alteracoes_locais": alterado,
            "codigo_sha256": {
                p.name: sha256(p.read_bytes()) for p in Path(__file__).parent.glob("*.py")
            },
            "python": platform.python_version(),
            "deepeval": importlib.metadata.version("deepeval"),
            "repeticoes": args.repeticoes,
            "concorrencia": 1,
            "retentativas_429": args.retentativas_429,
            "timeout_segundos": args.timeout,
            "endpoint": ENDPOINT if args.modo == "api" else None,
            "golden_sha256": dataset.get("golden_sha256"),
            "dataset_arquivo_sha256": sha256(args.dataset.read_bytes()),
            "dataset_status": dataset.get("status", dataset.get("estado")),
            "casos_planejados": len(dataset["casos"]) * args.repeticoes,
            "turnos_planejados": sum(len(c["turnos"]) for c in dataset["casos"]) * args.repeticoes,
            "data_referencia_aplicada_ao_agente": False,
            "finalidade": (
                "execucao_golden_provisorio"
                if dataset.get("golden_sha256")
                else "piloto_integracao_nao_golden"
            ),
        }
        registros = Registros(args.saida / identificador, chave)
        print(f"Registros: {registros.pasta}", flush=True)
        casos = executar(
            dataset, cliente, registros, manifesto, args.repeticoes, prompt, args.retentativas_429
        )
        completos = sum(c["resultado_execucao"] == "concluida" for c in casos)
        print(
            f"Integração: {completos}/{len(casos)} casos concluídos. Avaliação funcional: não realizada."
        )
        return 0 if completos == len(dataset["casos"]) * args.repeticoes else 1
    except KeyboardInterrupt:
        print("Execução interrompida; evidências já gravadas foram preservadas.")
        return 130
    except (ValueError, OSError, ImportError) as exc:
        print(
            f'Não foi possível executar: {type(exc).__name__}. {exc if isinstance(exc, (ValueError, ImportError)) else "Verifique os arquivos e as permissões locais."}'
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
