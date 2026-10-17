"""Confere o formato técnico das respostas e cria os casos do DeepEval.
Verifica campos, sessões e registros de ferramentas, sem julgar regras da loja.
"""

import os
import re

# O piloto usa apenas measure() local, sem login, evaluate() remoto ou modelo juiz.
os.environ["DEEPEVAL_TELEMETRY_OPT_OUT"] = "1"
os.environ["DEEPEVAL_FILE_SYSTEM"] = "READ_ONLY"

from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase, ToolCall


def problemas_contrato(corpo) -> list[str]:
    if not isinstance(corpo, dict):
        return ["A resposta não é um objeto JSON."]
    erros = []
    if not isinstance(corpo.get("resposta"), str) or not corpo["resposta"].strip():
        erros.append("Texto resposta ausente ou vazio.")
    if not isinstance(corpo.get("sessao"), str) or not re.fullmatch(
        r"[A-Za-z0-9-]{33,100}", corpo["sessao"]
    ):
        erros.append("Sessão ausente ou fora do formato documentado.")
    if not isinstance(corpo.get("ferramentas"), list):
        erros.append("ferramentas ausente ou não é lista; não foi convertido para [].")
    elif any(
        not isinstance(f, dict)
        or not isinstance(f.get("ferramenta"), str)
        or not isinstance(f.get("entrada"), dict)
        for f in corpo["ferramentas"]
    ):
        erros.append("Registro de ferramenta sem nome/argumentos válidos.")
    if not isinstance(corpo.get("metricas"), list) or any(
        not isinstance(m, dict) for m in corpo["metricas"]
    ):
        erros.append("metricas ausente ou com formato inválido.")
    return erros


class ContratoRespostaMetric(BaseMetric):
    def __init__(self, problemas):
        self.problemas = problemas
        self.threshold, self.async_mode, self.strict_mode = 1, False, True
        self.error = None

    def measure(self, test_case: LLMTestCase, *args, **kwargs):
        self.score = 0.0 if self.problemas else 1.0
        self.success = self.score == 1.0
        self.reason = (
            "; ".join(self.problemas) or "Envelope técnico válido; conteúdo funcional não julgado."
        )
        return self.score

    async def a_measure(self, test_case, *args, **kwargs):
        return self.measure(test_case)

    def is_successful(self):
        return self.success

    @property
    def __name__(self):
        return "Contrato técnico da resposta API"


def avaliar_registro(registro, historico):
    corpo = registro["resposta_api"]
    erros = problemas_contrato(corpo)
    corpo_dict = corpo if isinstance(corpo, dict) else {}
    # Histórico da Lia não vira contexto de referência nem resposta esperada.
    teste = LLMTestCase(
        input=registro["requisicao"]["mensagem"],
        actual_output=(
            corpo_dict.get("resposta") if isinstance(corpo_dict.get("resposta"), str) else ""
        ),
        name=f'{registro["caso_id"]}-r{registro["repeticao"]}-t{registro["turno"]}',
        completion_time=registro.get("duracao_http_segundos"),
        metadata={
            "criterio_esperado": registro["criterio_esperado"],
            "referencias": registro["referencias"],
            "historico_conversa": list(historico),
            "resultado_funcional": "nao_avaliado",
            "modo": registro["modo"],
        },
        tools_called=(
            [
                ToolCall(name=f["ferramenta"], input_parameters=f["entrada"])
                for f in corpo_dict.get("ferramentas", [])
                if isinstance(f, dict)
                and isinstance(f.get("ferramenta"), str)
                and isinstance(f.get("entrada"), dict)
            ]
            if isinstance(corpo_dict.get("ferramentas"), list)
            else None
        ),
    )
    metrica = ContratoRespostaMetric(erros)
    metrica.measure(teste)
    return {
        "metrica": metrica.__name__,
        "score": metrica.score,
        "resultado_contrato": "passou" if metrica.is_successful() else "falhou",
        "descricao": metrica.reason,
        "test_case": {
            "input": teste.input,
            "actual_output": teste.actual_output,
            "context": teste.context,
            "metadata": teste.metadata,
            "completion_time": teste.completion_time,
            "tools_called": (
                [f.model_dump(mode="json", exclude_none=True) for f in teste.tools_called]
                if teste.tools_called is not None
                else None
            ),
        },
    }
