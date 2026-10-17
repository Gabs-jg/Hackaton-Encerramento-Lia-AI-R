"""Lê o dataset e confere o formato das entradas do executor.
Aceita o piloto inicial e encaminha o golden ao adaptador próprio.
Verifica IDs, categorias e referências antes de qualquer chamada.
"""

import json
import re
from pathlib import Path

CATEGORIAS = {
    "catalogo",
    "alergenos_restricoes",
    "montagem_calculo",
    "consulta_privacidade",
    "cupons",
    "varios_turnos",
    "fora_escopo",
    "adversarial",
}


def arquivo_local(raiz: Path, nome: str) -> Path:
    caminho = (raiz / nome).resolve()
    if not caminho.is_relative_to(raiz.resolve()) or not caminho.is_file():
        raise ValueError(f"Arquivo de referência inválido: {nome}")
    return caminho


def carregar(caminho: Path, raiz: Path) -> dict:
    dataset = json.loads(caminho.read_text(encoding="utf-8-sig"))
    if isinstance(dataset, dict) and dataset.get("formato") == "golden-lia-v1":
        from .golden import adaptar

        return adaptar(dataset, raiz)
    if not isinstance(dataset, dict) or dataset.get("formato") != "lia-piloto-v1":
        raise ValueError("Formato esperado: lia-piloto-v1; adaptar após o acordo da T13.")
    casos = dataset.get("casos")
    if not isinstance(casos, list) or not casos:
        raise ValueError("O dataset precisa de pelo menos um caso.")
    ids = set()
    for caso in casos:
        if not isinstance(caso, dict):
            raise ValueError("Cada caso deve ser um objeto JSON.")
        identificador = caso.get("id", "")
        if not isinstance(identificador, str) or not re.fullmatch(
            r"[A-Za-z0-9_-]{1,80}", identificador
        ):
            raise ValueError("ID inválido; usar letras, números, hífen ou sublinhado.")
        if identificador in ids:
            raise ValueError(f"ID duplicado: {identificador}")
        ids.add(identificador)
        if caso.get("categoria") not in CATEGORIAS:
            raise ValueError(f"Categoria inválida em {identificador}.")
        turnos, referencias = caso.get("turnos"), caso.get("referencias")
        if (
            not isinstance(turnos, list)
            or not turnos
            or not isinstance(referencias, list)
            or not referencias
        ):
            raise ValueError(f"Faltam turnos ou referências em {identificador}.")
        for turno in turnos:
            if not isinstance(turno, dict):
                raise ValueError("Cada turno deve ser um objeto JSON.")
            for campo in ("mensagem", "criterio_esperado"):
                if not isinstance(turno.get(campo), str) or not turno[campo].strip():
                    raise ValueError(f"{campo} obrigatório em {identificador}.")
            if any(campo in turno for campo in ("sessao", "prompt_sistema", "resposta")):
                raise ValueError(
                    "Sessão, prompt e resposta observada não pertencem à entrada do caso."
                )
            if "evidencia_replay" in turno:
                arquivo_local(raiz, turno["evidencia_replay"])
        for referencia in referencias:
            if not isinstance(referencia, dict) or not isinstance(referencia.get("arquivo"), str):
                raise ValueError("Referência deve indicar arquivo e seções.")
            fonte = arquivo_local(raiz, referencia["arquivo"]).read_text(encoding="utf-8-sig")
            secoes = referencia.get("secoes")
            if not isinstance(secoes, list) or not secoes:
                raise ValueError(f"Indicar seção exata da referência em {identificador}.")
            for secao in secoes:
                if not isinstance(secao, str) or not re.search(
                    r"^#{1,6}\s+" + re.escape(secao) + r"\s*$", fonte, re.M
                ):
                    raise ValueError(f"Seção não encontrada em {referencia['arquivo']}: {secao}")
    return dataset
