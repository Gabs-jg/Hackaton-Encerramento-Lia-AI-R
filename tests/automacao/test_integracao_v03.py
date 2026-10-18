"""Verifica a migração do golden e respostas parciais usando exemplos locais.
Não chama a Lia nem modelos pagos; protege a compatibilidade com a v0.2.
"""

import copy
import unittest
from . import test_golden
from .casos import carregar
from .executar import RAIZ
from .avaliar import carregar_config
from .funcional import avaliar_turno


class IntegracaoV03Tests(unittest.TestCase):
    def setUp(self):
        self.dataset = carregar(RAIZ / "datasets/golden-v0.3.json", RAIZ)
        self.config = carregar_config(
            RAIZ / "tests/automacao/config/avaliacao-provisoria.json", self.dataset
        )

    def test_contagens_e_pm02(self):
        self.assertEqual(len(self.dataset["casos"]), 48)
        self.assertEqual(sum(len(c["turnos"]) for c in self.dataset["casos"]), 86)
        self.assertEqual(
            sum(len(t["criterios_esperados"]) for c in self.dataset["casos"] for t in c["turnos"]),
            112,
        )
        par = next(p for p in self.dataset["pares_metamorficos"] if p["id"] == "PM02")
        self.assertEqual(set(par["casos"]), {"T04-PM02A", "T04-PM02B"})
        lados = [c for c in self.dataset["casos"] if c["id"] in par["casos"]]
        self.assertEqual([len(c["turnos"]) for c in lados], [2, 2])
        self.assertEqual(lados[0]["turnos"][1]["mensagem"], lados[1]["turnos"][1]["mensagem"])
        self.assertTrue(all(len(t["criterios_esperados"]) == 3 for c in lados for t in c["turnos"]))

    def test_config_antiga_nao_serve_para_novo_golden(self):
        with self.assertRaises(ValueError):
            carregar_config(
                RAIZ / "tests/automacao/config/avaliacao-golden-v0.2.json", self.dataset
            )

    def registro(self):
        c = next(c for c in self.dataset["casos"] if c["id"] == "T05-EX01")
        t = copy.deepcopy(c["turnos"][2])
        return {
            **t,
            "caso_id": c["id"],
            "categoria": c["categoria"],
            "repeticao": 1,
            "turno": 3,
            "resultado_execucao": "concluida",
            "resposta_api": {"resposta": "Texto controlado"},
            "requisicao": {"mensagem": t["mensagem"]},
        }

    def test_falha_convencao_separada_de_regra_oficial(self):
        r = self.registro()
        humano = test_golden.GoldenTests.revisao(self, r)
        humano["criterios"][1]["resultado"] = "falhou"
        saida = avaliar_turno(r, self.config, humano=humano)
        self.assertEqual(saida["resultado_convencao"], "falhou")
        self.assertEqual(saida["resultado"], "inconclusivo")
        self.assertTrue(saida["revisao_humana"])
        humano["criterios"][0]["resultado"] = "falhou"
        self.assertEqual(avaliar_turno(r, self.config, humano=humano)["resultado"], "falhou")

    def test_texto_sem_ferramentas_ainda_revela_falha(self):
        r = self.registro()
        r.update(resultado_execucao="erro_contrato", http_status=200, erro_tecnico=None)
        humano = test_golden.GoldenTests.revisao(self, r, "falhou")
        saida = avaliar_turno(r, self.config, humano=humano)
        self.assertEqual(saida["resultado"], "falhou")
        self.assertTrue(saida["semantica"])

    def test_texto_parcial_correto_nao_aprova_contrato(self):
        r = self.registro()
        r.update(resultado_execucao="erro_contrato", http_status=200, erro_tecnico=None)
        saida = avaliar_turno(r, self.config, humano=test_golden.GoldenTests.revisao(self, r))
        self.assertEqual(saida["resultado"], "inconclusivo")
        self.assertTrue(saida["semantica"])

    def test_timeout_ou_sessao_divergente_nao_avaliados(self):
        for estado, http, avisos in [
            ("inconclusivo_ambiente", 504, []),
            ("erro_contrato", 200, ["sessao retornada mudou dentro do mesmo caso"]),
        ]:
            r = self.registro()
            r.update(resultado_execucao=estado, http_status=http, avisos=avisos)
            saida = avaliar_turno(
                r, self.config, humano=test_golden.GoldenTests.revisao(self, r, "falhou")
            )
            self.assertEqual(saida["resultado"], "inconclusivo")
            self.assertFalse(saida["semantica"])

    def test_convencao_corresponde_ao_golden(self):
        esperado = {
            f"{c['id']}:T{t['turno']}": t["criterios_convencao_equipe"]
            for c in self.dataset["casos"]
            for t in c["turnos"]
            if t.get("criterios_convencao_equipe")
        }
        self.assertEqual(self.config["criterios_convencao_por_turno"], esperado)

    def test_calculos_da_convencao(self):
        from decimal import Decimal, ROUND_HALF_UP

        for subtotal, frete, desconto, total in [
            ("61.70", "18", "3.09", "76.61"),
            ("32.70", "18", "1.64", "49.06"),
            ("149.70", "12", "7.49", "154.21"),
            ("219.90", "0", "11.00", "208.90"),
        ]:
            calculado = (Decimal(subtotal) * Decimal("0.05")).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            self.assertEqual(calculado, Decimal(desconto))
            self.assertEqual(Decimal(subtotal) - calculado + Decimal(frete), Decimal(total))
