"""Testa a coleta com clientes simulados e arquivos temporários.
Confere sessões, turnos, erros, prompt e gravação de evidências sem chamar a Lia.
"""

import copy
import json
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

from .avaliacao import problemas_contrato
from .casos import carregar
from .cliente import ClienteLia, ClienteReplay
from .executar import RAIZ, executar, main
from .registros import Registros


class ClienteControlado:
    def __init__(self, respostas=None):
        self.chamadas, self.respostas = [], list(respostas or [])

    def enviar(self, payload, turno):
        self.chamadas.append(copy.deepcopy(payload))
        if self.respostas:
            resposta = self.respostas.pop(0)
            if isinstance(resposta, Exception):
                raise resposta
            return copy.deepcopy(resposta)
        return envelope(sessao=payload.get("sessao") or str(uuid.uuid4()))


def envelope(sessao=None, status=200, **campos):
    return {
        "http_status": status,
        "erro_tecnico": None,
        "resposta_api": {
            "resposta": "Total comercial propositalmente incorreto R$ 0,01.",
            "sessao": sessao or str(uuid.uuid4()),
            "ferramentas": [],
            "metricas": [{"usage": {"totalTokens": 8}}, {"usage": {"totalTokens": 13}}],
            **campos,
        },
    }


class ExecutorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.pasta = Path(self.tmp.name)
        self.dataset = carregar(RAIZ / "datasets/pilotos/t15-piloto.json", RAIZ)
        self.manifesto = {
            "id": "teste",
            "modo": "api",
            "versao_solicitada": "original",
            "fase_base": "teste_controlado",
        }

    def rodar(self, cliente=None, **kwargs):
        cliente = cliente or ClienteControlado()
        registros = Registros(self.pasta / "run", "SEGREDO-DE-TESTE")
        casos = executar(self.dataset, cliente, registros, self.manifesto, **kwargs)
        return cliente, casos

    def test_casos_pilotos_validos(self):
        self.assertEqual(len(self.dataset["casos"]), 3)
        self.assertEqual(sum(len(c["turnos"]) for c in self.dataset["casos"]), 4)

    def test_sessoes_novas_por_caso_repeticao_e_mantidas_entre_turnos(self):
        cliente, casos = self.rodar(repeticoes=2)
        self.assertEqual(len(cliente.chamadas), 8)
        self.assertEqual(sum("sessao" in p for p in cliente.chamadas), 2)
        self.assertEqual(len(casos), 6)
        for caso in casos:
            self.assertEqual(caso["resultado_execucao"], "concluida")

    def test_prompt_em_todos_os_turnos_corrigidos(self):
        self.manifesto["versao_solicitada"] = "corrigida"
        cliente, _ = self.rodar(prompt="prompt técnico de teste")
        self.assertTrue(
            all(p["prompt_sistema"] == "prompt técnico de teste" for p in cliente.chamadas)
        )

    def test_original_sem_prompt_e_funcional_nao_aprovado(self):
        cliente, casos = self.rodar()
        self.assertTrue(all("prompt_sistema" not in p for p in cliente.chamadas))
        resumo = json.loads((self.pasta / "run/resumo.json").read_text(encoding="utf-8"))
        self.assertEqual(resumo["avaliacao_funcional"], "nao_avaliado")
        self.assertEqual(casos[0]["turnos"][0]["deepeval"]["resultado_contrato"], "passou")

    def test_preserva_campos_extras_todas_metricas_e_argumentos_de_ferramentas(self):
        ferramentas = [
            {
                "ferramenta": "consulta",
                "entrada": {"numero": "PD-1001", "email": "ana.souza@example.com"},
            }
        ]
        resposta = envelope(campo_novo={"dados": [1, 2]}, ferramentas=ferramentas)
        self.rodar(ClienteControlado([resposta]))
        registro = json.loads(
            (self.pasta / "run/T15-P01/r01/t01-a01.json").read_text(encoding="utf-8")
        )
        self.assertEqual(registro["resposta_api"], resposta["resposta_api"])
        self.assertEqual(
            registro["deepeval"]["test_case"]["tools_called"][0]["input_parameters"],
            ferramentas[0]["entrada"],
        )

    def test_versao_ausente_vira_aviso_sem_inventar_valor(self):
        _, casos = self.rodar()
        self.assertIn("versao ausente", casos[0]["turnos"][0]["avisos"][0])

    def test_versao_diferente_reprovacao_tecnica(self):
        _, casos = self.rodar(ClienteControlado([envelope(versao="corrigida")]))
        self.assertEqual(casos[0]["resultado_execucao"], "erro_contrato")

    def test_t2_nao_enviado_apos_timeout_em_t1(self):
        self.dataset["casos"] = [self.dataset["casos"][1]]
        cliente, casos = self.rodar(
            ClienteControlado(
                [{"http_status": None, "erro_tecnico": "timeout", "resposta_api": None}]
            ),
            retentativas_429=2,
        )
        self.assertEqual(len(cliente.chamadas), 1)
        self.assertEqual(casos[0]["resultado_execucao"], "inconclusivo_ambiente")

    def test_429_retry_limitado_preserva_tentativas(self):
        self.dataset["casos"] = self.dataset["casos"][:1]
        cliente, casos = self.rodar(
            ClienteControlado([envelope(status=429)]), retentativas_429=1, dormir=lambda _: None
        )
        self.assertEqual(len(cliente.chamadas), 2)
        self.assertEqual(len(casos[0]["turnos"]), 2)
        self.assertTrue((self.pasta / "run/T15-P01/r01/t01-a01.json").exists())
        self.assertEqual(casos[0]["resultado_execucao"], "concluida")

    def test_500_nao_reexecuta_turno_automaticamente(self):
        self.dataset["casos"] = self.dataset["casos"][:1]
        cliente, casos = self.rodar(ClienteControlado([envelope(status=502)]), retentativas_429=2)
        self.assertEqual(len(cliente.chamadas), 1)
        self.assertEqual(casos[0]["resultado_execucao"], "inconclusivo_ambiente")

    def test_401_interrompe_lote(self):
        cliente, casos = self.rodar(ClienteControlado([envelope(status=401)]))
        self.assertEqual(len(cliente.chamadas), 1)
        self.assertEqual(len(casos), 1)
        self.assertEqual(self.manifesto["estado"], "interrompida_por_erro")

    def test_erro_executor_preserva_registro(self):
        _, casos = self.rodar(ClienteControlado([RuntimeError("detalhes internos não publicados")]))
        self.assertEqual(casos[0]["resultado_execucao"], "erro_executor")
        self.assertTrue((self.pasta / "run/T15-P01/r01/t01-a01.json").exists())

    def test_ausencia_ferramentas_difere_lista_vazia(self):
        resposta = envelope()["resposta_api"]
        self.assertFalse(problemas_contrato(resposta))
        del resposta["ferramentas"]
        self.assertTrue(any("ferramentas" in e for e in problemas_contrato(resposta)))

    def test_sessao_alterada_em_t2_interrompe_caso(self):
        self.dataset["casos"] = [self.dataset["casos"][1]]
        _, casos = self.rodar(ClienteControlado([envelope(), envelope()]))
        self.assertEqual(casos[0]["resultado_execucao"], "erro_contrato")

    def test_sessao_reutilizada_entre_casos_detectada(self):
        sessao = str(uuid.uuid4())
        _, casos = self.rodar(ClienteControlado([envelope(sessao), envelope(sessao)]))
        self.assertEqual(casos[1]["resultado_execucao"], "erro_contrato")

    def test_segredo_refletido_na_resposta_nao_e_gravado(self):
        self.rodar(ClienteControlado([envelope(resposta="SEGREDO-DE-TESTE")]))
        for arquivo in (self.pasta / "run").rglob("*"):
            if arquivo.is_file():
                self.assertNotIn("SEGREDO-DE-TESTE", arquivo.read_text(encoding="utf-8"))

    def test_dataset_duplicado_e_secao_inexistente_rejeitados(self):
        for alterar in (
            lambda d: d["casos"].append(d["casos"][0]),
            lambda d: d["casos"][0]["referencias"][0].update(secoes=["SEÇÃO INEXISTENTE"]),
        ):
            dados = copy.deepcopy(self.dataset)
            alterar(dados)
            p = self.pasta / "invalido.json"
            p.write_text(json.dumps(dados), encoding="utf-8")
            with self.assertRaises(ValueError):
                carregar(p, RAIZ)

    def test_cli_replay_nao_conta_copia_como_repeticao(self):
        self.assertEqual(main(["--modo", "replay", "--repeticoes", "3"]), 2)

    def test_replay_resolve_template_da_sessao_sem_alterar_evidencia(self):
        self.manifesto["modo"] = "replay"
        _, casos = self.rodar(ClienteReplay(RAIZ))
        self.assertEqual([c["resultado_execucao"] for c in casos], ["concluida"] * 3)
        registro = json.loads(
            (self.pasta / "run/T15-P02/r01/t02-a01.json").read_text(encoding="utf-8")
        )
        self.assertEqual(registro["sessao_template_na_fonte"], "{{t05_mc10_sessao}}")

    def test_timeout_http_sai_como_limite_ambiente(self):
        cliente = ClienteLia("CHAVE-CONTROLADA")
        with patch.object(cliente.opener, "open", side_effect=TimeoutError):
            registro = cliente.enviar({"mensagem": "teste"}, {})
        self.assertEqual(registro["erro_tecnico"], "timeout")

    def test_cliente_codifica_utf8_e_nao_registra_cabecalho(self):
        from io import BytesIO

        cliente = ClienteLia("CHAVE-CONTROLADA")
        erro = HTTPError("https://local.invalid", 400, "erro", {}, BytesIO(b'{"erro":"JSON"}'))
        with patch.object(cliente.opener, "open", side_effect=erro) as requisicao:
            registro = cliente.enviar({"mensagem": "pipoca e restrição"}, {})
        req = requisicao.call_args.args[0]
        self.assertEqual(json.loads(req.data.decode("utf-8"))["mensagem"], "pipoca e restrição")
        self.assertNotIn("CHAVE-CONTROLADA", json.dumps(registro))

    def test_json_invalido_nao_vira_falha_funcional_nem_dispara_retry(self):
        self.dataset["casos"] = self.dataset["casos"][:1]
        resposta = {
            "http_status": 200,
            "erro_tecnico": "json_invalido",
            "resposta_api": None,
            "corpo_nao_json": "<html>retorno inesperado</html>",
        }
        cliente, casos = self.rodar(ClienteControlado([resposta]), retentativas_429=2)
        self.assertEqual(len(cliente.chamadas), 1)
        self.assertEqual(casos[0]["resultado_execucao"], "erro_contrato")
        registro = json.loads(
            (self.pasta / "run/T15-P01/r01/t01-a01.json").read_text(encoding="utf-8")
        )
        self.assertEqual(registro["corpo_nao_json"], resposta["corpo_nao_json"])
        self.assertEqual(registro["resultado_funcional"], "nao_avaliado")

    def test_interrupcao_em_t2_nao_marca_conversa_completa(self):
        self.dataset["casos"] = [self.dataset["casos"][1]]
        cliente = ClienteControlado()
        enviar = cliente.enviar

        def interrupcao(payload, turno):
            if cliente.chamadas:
                raise KeyboardInterrupt
            return enviar(payload, turno)

        cliente.enviar = interrupcao
        with self.assertRaises(KeyboardInterrupt):
            self.rodar(cliente)
        resumo = json.loads((self.pasta / "run/resumo.json").read_text(encoding="utf-8"))
        self.assertEqual(resumo["casos"][0]["resultado_execucao"], "interrompida")
        self.assertEqual(resumo["execucao"]["estado"], "interrompida")

    def test_contexto_historico_nao_e_oraculo_do_deepeval(self):
        self.rodar()
        registro = json.loads(
            (self.pasta / "run/T15-P02/r01/t02-a01.json").read_text(encoding="utf-8")
        )
        caso = registro["deepeval"]["test_case"]
        self.assertIsNone(caso["context"])
        self.assertEqual(len(caso["metadata"]["historico_conversa"]), 2)

    def test_replay_nao_contabiliza_chamadas_reais(self):
        self.manifesto["modo"] = "replay"
        self.rodar(ClienteReplay(RAIZ))
        self.assertEqual(self.manifesto["chamadas_api_tentadas"], 0)


if __name__ == "__main__":
    unittest.main()
