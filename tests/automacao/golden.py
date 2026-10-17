"""Adapta o golden ao formato que o executor consome.
Confere fontes e pares e acrescenta os trechos oficiais usados na avaliação.
Não reescreve as mensagens nem usa respostas da Lia como resultado esperado.
"""

import copy
import hashlib
import json
import re

from .casos import arquivo_local


def digest(value):
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()


def secao(texto, titulo):
    linhas = texto.splitlines()
    for i, linha in enumerate(linhas):
        match = re.fullmatch(r"(#{1,6})\s+(.+?)\s*", linha)
        if match and match[2] == titulo:
            nivel = len(match[1])
            fim = next(
                (
                    j
                    for j in range(i + 1, len(linhas))
                    if re.match(r"^#{1," + str(nivel) + r"}\s", linhas[j])
                ),
                len(linhas),
            )
            return "\n".join(linhas[i:fim])
    raise ValueError(f"Seção de referência não encontrada: {titulo}")


def adaptar(original, raiz):
    from .casos import CATEGORIAS

    categorias_por_tarefa = dict(
        zip(
            ("T03", "T04", "T05", "T06", "T07", "T08", "T09", "T10"),
            (
                "catalogo",
                "alergenos_restricoes",
                "montagem_calculo",
                "consulta_privacidade",
                "cupons",
                "varios_turnos",
                "fora_escopo",
                "adversarial",
            ),
        )
    )
    fontes = original["base_referencia"]["fontes"]
    textos, auditoria = {}, {}
    for codigo, fonte in fontes.items():
        if "arquivo" not in fonte:
            continue
        caminho = arquivo_local(raiz, fonte["arquivo"])
        bruto = caminho.read_bytes()
        normalizado = bruto.replace(b"\r\n", b"\n")
        if fonte.get("sha256") not in (
            hashlib.sha256(bruto).hexdigest(),
            hashlib.sha256(normalizado).hexdigest(),
        ):
            raise ValueError(f"Fonte {codigo} difere do hash registrado no golden.")
        textos[codigo] = bruto.decode("utf-8-sig")
        auditoria[codigo] = {
            "arquivo": fonte["arquivo"],
            "sha256_lf": hashlib.sha256(normalizado).hexdigest(),
        }
    t12 = (
        arquivo_local(raiz, original["criterios_t12"]["arquivo"])
        .read_bytes()
        .replace(b"\r\n", b"\n")
    )
    if hashlib.sha256(t12).hexdigest() != original["criterios_t12"]["sha256"]:
        raise ValueError("Referência T12 difere do hash registrado no golden.")
    casos, ids = [], set()
    for caso in original["casos"]:
        identificador = caso["id"]
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", identificador) or identificador in ids:
            raise ValueError("ID inválido ou duplicado no golden.")
        ids.add(identificador)
        categoria = categorias_por_tarefa.get(caso["tarefa_origem"])
        if categoria not in CATEGORIAS or not caso["turnos"]:
            raise ValueError(f"Categoria/turnos inválidos: {identificador}")
        novo = copy.deepcopy(caso)
        novo["categoria"] = categoria
        novo["referencias"] = []
        novo["turnos"] = []
        for numero, turno in enumerate(caso["turnos"], 1):
            if (
                turno.get("turno") != numero
                or not isinstance(turno["entrada"], str)
                or not turno["entrada"].strip()
            ):
                raise ValueError(f"Entrada/ordem inválida em {identificador}")
            if not turno["criterios_esperados"] or any(
                not isinstance(x, str) or not x.strip() for x in turno["criterios_esperados"]
            ):
                raise ValueError(f"Critérios inválidos em {identificador}")
            if any(k in turno for k in ("sessao", "prompt_sistema", "resposta")):
                raise ValueError("O golden não pode conter estado de sessão ou resposta observada.")
            contexto, refs, ausentes = [], [], []
            if not turno["referencias"]:
                raise ValueError(f"Referências ausentes em {identificador}")
            for ref in turno["referencias"]:
                fonte = fontes[ref["fonte"]]
                if ref["fonte"] in textos:
                    trecho = secao(textos[ref["fonte"]], ref["secao"])
                    contexto.append(
                        {
                            "fonte": ref["fonte"],
                            "arquivo": fonte["arquivo"],
                            "secao": ref["secao"],
                            "texto": trecho,
                        }
                    )
                    refs.append({"arquivo": fonte["arquivo"], "secoes": [ref["secao"]]})
                else:
                    ausentes.append(ref)
            novo["turnos"].append(
                {
                    **copy.deepcopy(turno),
                    "caso_id": identificador,
                    "mensagem": turno["entrada"],
                    "criterio_esperado": "\n".join(turno["criterios_esperados"]),
                    "referencias": refs,
                    "contexto_oficial": contexto,
                    "referencias_nao_locais": ausentes,
                    "data_referencia": caso.get("data_referencia"),
                }
            )
            novo["referencias"].extend(r for r in refs if r not in novo["referencias"])
        casos.append(novo)
    if (
        len(casos) != original["total_casos"]
        or sum(len(caso["turnos"]) for caso in casos) != original["total_turnos"]
    ):
        raise ValueError("Contagens do golden inconsistentes.")
    pares = original.get("pares_metamorficos", [])
    if len({caminho["id"] for caminho in pares}) != len(pares):
        raise ValueError("Par duplicado.")
    por_id = {caso["id"]: caso for caso in casos}
    for par in pares:
        if len(par["casos"]) != 2 or len(set(par["casos"])) != 2 or not set(par["casos"]) <= ids:
            raise ValueError("Par precisa de dois casos distintos existentes.")
        for caso_id in par["casos"]:
            if par["id"] not in por_id[caso_id]["pares_metamorficos"]:
                raise ValueError("Vínculo do par ausente no caso.")
    for caso in casos:
        for par_id in caso["pares_metamorficos"]:
            if not any(
                caminho["id"] == par_id and caso["id"] in caminho["casos"] for caminho in pares
            ):
                raise ValueError("Vínculo de caso com par inexistente.")
    return {
        **copy.deepcopy(original),
        "casos": casos,
        "golden_sha256": digest(original),
        "fontes_conferidas": auditoria,
        "adaptador": "golden-lia-v1 -> executor-t15",
    }
