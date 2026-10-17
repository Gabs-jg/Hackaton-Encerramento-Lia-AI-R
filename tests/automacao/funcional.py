"""Verifica os critérios de cada turno e organiza o resultado funcional.
Compara valores em centavos, valida as citações do juiz e aplica revisão humana.
Uma falha demonstrada não é compensada por outros critérios aprovados.
"""

import re
import unicodedata
from decimal import Decimal

from .avaliacao import BaseMetric, LLMTestCase
from .golden import digest

RESULTADOS = {"passou", "falhou", "inconclusivo"}
ROTULOS = {
    "subtotal": r"subtotal(?: dos produtos)?",
    "desconto": r"desconto(?: (?:no |de )?pix| do cupom| \([^\n)]*\))?",
    "liquido": r"(?:produtos liquidos|liquido|subtotal (?:apos|com) desconto)",
    "frete": r"frete(?: (?:para|em) [a-z ]+)?",
    "total": r"total(?: (?:final|geral|do pedido|a pagar))?",
}


def normalizar(texto):
    return "".join(
        c for c in unicodedata.normalize("NFD", texto.lower()) if unicodedata.category(c) != "Mn"
    )


def extrair_centavos(texto, campo):
    """Conservador: não decide por mera presença do número esperado no texto."""
    texto = normalizar(texto).replace("**", "").replace("`", "")
    if campo == "preco_unico":
        valores = re.findall(r"r\$\s*(\d+(?:\.\d{3})*,\d{2})(?!\d)", texto)
    else:
        rotulo = ROTULOS[campo]
        sinal_desconto = r"(?:-\s*)?" if campo == "desconto" else ""
        valores = re.findall(
            r"(?:^|\n)\s*(?:[-*]\s*)?"
            + rotulo
            + r"\s*[:=–-]?\s*"
            + sinal_desconto
            + r"(?:r\$\s*)?(-?\d+(?:\.\d{3})*,\d{2})(?!\d)",
            texto,
        )
        if campo == "frete" and re.search(
            r"(?:^|\n)\s*(?:[-*]\s*)?frete\s*:?\s*(?:gratis|gratuito)\b", texto
        ):
            valores.append("0,00")
    numeros = {int(Decimal(v.replace(".", "").replace(",", ".")) * 100) for v in valores}
    if campo == "desconto":
        numeros = {abs(v) for v in numeros}
    return next(iter(numeros)) if len(numeros) == 1 else None


def verificar_numeros(texto, regras):
    saida = []
    for campo, esperado in regras.items():
        obtido = extrair_centavos(texto, campo)
        status = "inconclusivo" if obtido is None else "passou" if obtido == esperado else "falhou"
        saida.append(
            {
                "campo": campo,
                "esperado_centavos": esperado,
                "obtido_centavos": obtido,
                "resultado": status,
                "descricao": (
                    "Campo ausente/ambíguo: revisar a redação."
                    if obtido is None
                    else f"Comparação exata em centavos: esperado {esperado}; obtido {obtido}."
                ),
                "revisao_humana": status == "falhou",
            }
        )
    return saida


# Aceitar representação equivalente, sem alterar palavras, números, acentos ou negações.
def normalizar_formatacao_citacao(texto):
    texto = unicodedata.normalize("NFC", texto)
    texto = re.sub(r"\*\*(\S(?:.*?\S)?)\*\*", r"\1", texto)
    texto = re.sub(r"`([^`\n]+)`", r"\1", texto)
    return " ".join(texto.split())


def validar_julgamento(julgamento, criterios, resposta):
    if not isinstance(julgamento, dict):
        raise ValueError("Julgamento deve ser objeto JSON.")
    itens = julgamento.get("criterios")
    if not isinstance(itens, list) or len(itens) != len(criterios):
        raise ValueError("Juiz/revisão deve avaliar todos os critérios, uma vez cada.")
    if any(not isinstance(i, dict) or type(i.get("id")) is not int for i in itens):
        raise ValueError("Cada critério precisa de objeto e ID inteiro.")
    if {i.get("id") for i in itens} != set(range(1, len(criterios) + 1)):
        raise ValueError("IDs de critérios inválidos/duplicados.")
    validados = []
    for item in itens:
        if (
            item.get("resultado") not in RESULTADOS
            or not isinstance(item.get("motivo"), str)
            or not item["motivo"].strip()
        ):
            raise ValueError("Julgamento sem resultado/motivo válido.")
        citacoes = item.get("trechos_resposta", [])
        if not isinstance(citacoes, list) or any(
            not isinstance(t, str) or not t.strip() for t in citacoes
        ):
            raise ValueError("Lista de citações inválida.")
        if any(
            t not in resposta
            and normalizar_formatacao_citacao(t) not in normalizar_formatacao_citacao(resposta)
            for t in citacoes
        ):
            raise ValueError("Citação do juiz não existe na resposta avaliada.")
        if item["resultado"] == "passou" and not citacoes:
            raise ValueError("Aprovação exige trecho verificável da resposta.")
        validados.append(
            {
                **item,
                "validacao_citacoes": [
                    "literal" if t in resposta else "equivalente_formatacao_espacos"
                    for t in citacoes
                ],
            }
        )
    return sorted(validados, key=lambda i: i["id"])


def status_conjunto(status):
    if "falhou" in status:
        return "falhou"
    return "passou" if status and all(s == "passou" for s in status) else "inconclusivo"


class CriteriosGoldenMetric(BaseMetric):
    """Sem média entre regras: uma violação não é compensada por outros acertos."""

    def __init__(self, resultados):
        self.resultados = resultados
        self.threshold, self.async_mode, self.strict_mode = 1, False, True
        self.error = None

    def measure(self, test_case, *args, **kwargs):
        self.resultado = status_conjunto(self.resultados)
        self.score = 1.0 if self.resultado == "passou" else 0.0
        self.success = self.resultado == "passou"
        self.reason = (
            "Todos os critérios atendidos."
            if self.success
            else (
                "Há violação registrada."
                if self.resultado == "falhou"
                else "Cobertura/avaliação incompleta; score técnico zero não é defeito da Lia."
            )
        )
        return self.score

    async def a_measure(self, test_case, *args, **kwargs):
        return self.measure(test_case)

    def is_successful(self):
        return self.success

    @property
    def __name__(self):
        return "Critérios funcionais do golden"


def avaliar_turno(registro, config, humano=None, juiz=None):
    corpo = registro.get("resposta_api") or {}
    resposta = corpo.get("resposta", "") if isinstance(corpo, dict) else ""
    criterios = registro.get("criterios_esperados", [registro["criterio_esperado"]])
    vinculo = digest(registro)
    chave = f'{registro["caso_id"]}/r{registro["repeticao"]:02}/t{registro["turno"]:02}'
    saida = {
        "chave": chave,
        "evidencia_sha256": vinculo,
        "caso_id": registro["caso_id"],
        "turno": registro["turno"],
        "repeticao": registro["repeticao"],
        "categoria": registro["categoria"],
        "criterios_esperados": criterios,
        "severidade_sugerida": config["severidades_por_categoria"].get(
            registro["categoria"], "alto"
        ),
        "resultado": "inconclusivo",
        "numeros": [],
        "semantica": [],
        "pendencias": [],
        "revisao_humana": True,
        "origem_julgamento": "pendente",
    }
    if registro["resultado_execucao"] != "concluida":
        saida["pendencias"] = [
            "Sem resposta tecnicamente utilizável: " + registro["resultado_execucao"]
        ]
        return saida
    regras = config["numeros_por_turno"].get(f'{registro["caso_id"]}:T{registro["turno"]}', {})
    saida["numeros"] = verificar_numeros(resposta, regras)
    julgamento = None
    if humano:
        if (
            humano.get("evidencia_sha256") != vinculo
            or not humano.get("revisor")
            or humano.get("confirmado") is not True
        ):
            raise ValueError(f"Revisão não confirmada ou de outra evidência: {chave}")
        julgamento = humano
        saida["origem_julgamento"] = "humano"
        saida["revisor"] = humano["revisor"]
    elif juiz:
        try:
            julgamento = juiz.julgar(registro)
            saida["juiz"] = julgamento
            saida["origem_julgamento"] = "modelo_provisorio"
        except Exception as exc:
            saida["pendencias"].append("Falha/limite do juiz: " + type(exc).__name__)
    if julgamento:
        try:
            saida["semantica"] = validar_julgamento(julgamento, criterios, resposta)
        except ValueError:
            if humano:
                raise
            saida["pendencias"].append("Saída do juiz inválida; não aprovar automaticamente.")
    if not saida["semantica"]:
        saida["semantica"] = [
            {
                "id": n,
                "resultado": "inconclusivo",
                "motivo": "Aguardando avaliação semântica.",
                "trechos_resposta": [],
            }
            for n in range(1, len(criterios) + 1)
        ]
    if registro.get("pontos_de_revisao"):
        saida["pendencias"].extend(registro["pontos_de_revisao"])
    if registro.get("referencias_nao_locais") and not humano:
        saida["pendencias"].append("Há referência do enunciado não disponível localmente ao juiz.")
    status = [i["resultado"] for i in saida["semantica"]]
    # Extração incompleta pede interpretação humana; não impõe redação fixa à Lia.
    if not humano:
        status += [i["resultado"] for i in saida["numeros"]]
    else:
        saida["numeros_revisados_por_humano"] = True
    if not humano and (saida["pendencias"] or saida["severidade_sugerida"] == "crítico"):
        status.append("inconclusivo")
    metrica = CriteriosGoldenMetric(status)
    metrica.measure(
        LLMTestCase(
            input=registro["requisicao"]["mensagem"],
            actual_output=resposta,
            expected_output="\n".join(criterios),
            context=[c["texto"] for c in registro.get("contexto_oficial", [])],
        )
    )
    saida["resultado"] = metrica.resultado
    saida["deepeval"] = {
        "metrica": metrica.__name__,
        "score": metrica.score,
        "threshold": 1,
        "motivo": metrica.reason,
        "inconclusivo_nao_e_falha": True,
    }
    saida["revisao_humana"] = not bool(humano) and (
        not config["juiz"].get("calibracao_aprovada", False)
        or saida["resultado"] != "passou"
        or saida["severidade_sugerida"] == "crítico"
    )
    return saida
