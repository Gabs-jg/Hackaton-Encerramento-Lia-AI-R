"""Grava evidências e resumos locais da execução.
Salva primeiro em arquivo temporário e remove a chave conhecida dos registros.
O resumo de integração não substitui a avaliação funcional.
"""

import json
import os
from pathlib import Path


class Registros:
    def __init__(self, pasta: Path, segredo: str = ""):
        self.pasta, self.segredo = pasta, segredo
        pasta.mkdir(parents=True, exist_ok=False)

    def salvar(self, nome, dados):
        texto = json.dumps(dados, ensure_ascii=False, indent=2) + "\n"
        if self.segredo:
            texto = texto.replace(self.segredo, "[SEGREDO_REMOVIDO]")
        caminho = self.pasta / nome
        caminho.parent.mkdir(parents=True, exist_ok=True)
        temporario = caminho.with_suffix(caminho.suffix + ".tmp")
        temporario.write_text(texto, encoding="utf-8")
        os.replace(temporario, caminho)

    def resumo(self, manifesto, casos):
        dados = {
            "execucao": manifesto,
            "casos": casos,
            "avaliacao_funcional": "nao_avaliado",
            "observacao": "Integração T15; aprovação técnica não é aprovação funcional da Lia.",
        }
        self.salvar("resumo.json", dados)
        linhas = [
            "# T15 — Resultado da integração",
            "",
            f'**Modo:** {manifesto["modo"]} · **Versão solicitada:** {manifesto["versao_solicitada"]}',
            f'**Fase da base declarada:** {manifesto["fase_base"]}',
            "",
            "**Avaliação funcional: não realizada.** Os resultados abaixo são técnicos; não aprovam preços, privacidade ou uso correto das ferramentas.",
            "",
            "| Caso | Repetição | Execução | Tentativas registradas | Contrato DeepEval |",
            "|---|---:|---|---:|---|",
        ]
        for caso in casos:
            resultados = [
                t.get("deepeval", {}).get("resultado_contrato", "não avaliado")
                for t in caso["turnos"]
            ]
            linhas.append(
                f'| {caso["id"]} | {caso["repeticao"]} | {caso["resultado_execucao"]} | {len(caso["turnos"])} | {", ".join(resultados)} |'
            )
        linhas += [
            "",
            "## Leitura das evidências",
            "",
            "Cada JSON por turno preserva requisição, corpo integral decodificado da API (inclusive campos extras), ferramentas e todos os itens de métricas. Corpo não JSON também é preservado. A chave do cabeçalho não é registrada.",
            "",
            "`versao` ausente fica como aviso: versão solicitada não comprova versão retornada. `fase_base` é declaração da equipe, não detecção automática.",
            "",
            "Replay relê respostas históricas: não representa novas chamadas, estabilidade, latência atual nem repetições independentes.",
            "",
        ]
        for caso in casos:
            linhas += [f'## {caso["id"]} — repetição {caso["repeticao"]}', ""]
            for turno in caso["turnos"]:
                linhas += [
                    f'### Turno {turno["turno"]} tentativa {turno["tentativa"]}',
                    "",
                    f'[Registro completo]({turno["arquivo"]})',
                    "",
                    f'**Execução:** {turno["resultado_execucao"]} · **HTTP:** {turno["http_status"]}',
                    "",
                ]
                if turno.get("avisos"):
                    linhas += ["**Avisos:** " + "; ".join(turno["avisos"]), ""]
        texto = "\n".join(linhas)
        if self.segredo:
            texto = texto.replace(self.segredo, "[SEGREDO_REMOVIDO]")
        (self.pasta / "resumo.md").write_text(texto, encoding="utf-8")
