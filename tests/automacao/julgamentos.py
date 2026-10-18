"""Reaproveita julgamentos compatíveis com a evidência e a rubrica atuais.
Pode combinar registros salvos com novas avaliações para os turnos restantes.
Tentativas inválidas preservadas não são cobradas de novo nem viram aprovação.
"""

import json
import os
from .golden import digest
from .juiz import RUBRICA, ErroFormatoJulgamento


class JuizSalvo:
    def __init__(self, caminho, config):
        self.dados = json.loads(caminho.read_text(encoding="utf-8-sig"))
        if self.dados.get("rubrica_sha256") != digest(RUBRICA):
            raise ValueError("Julgamentos salvos pertencem a outra rubrica.")
        self.config = config
        self.model_id = config.get("model_id") or os.environ.get("LIA_JUDGE_MODEL_ID")
        self.region = config.get("region") or os.environ.get("AWS_REGION")
        self.chamadas, self.custo_estimado, self.registros = 0, 0.0, []
        self.on_update = None
        self.fonte = str(caminho)

    def julgar(self, registro):
        hash_evidencia = digest(registro)
        julgamento = self.dados["julgamentos"].get(hash_evidencia)
        if (
            not julgamento
            or julgamento.get("modelo") != self.model_id
            or julgamento.get("regiao") != self.region
        ):
            raise ValueError("Sem julgamento compatível para esta evidência/modelo/região.")
        self.registros.append(
            {
                "caso": registro["caso_id"],
                "turno": registro["turno"],
                "reutilizado": True,
                "evidencia_sha256": hash_evidencia,
                "fonte": self.fonte,
            }
        )
        if julgamento.get("erro_julgamento"):
            self.registros[-1]["erro_preservado"] = julgamento["erro_julgamento"]
            raise ErroFormatoJulgamento(
                "Julgamento inválido preservado; nova chamada não realizada."
            )
        return {**julgamento, "reutilizado": True, "fonte_julgamento": self.fonte}


class JuizComCache:
    """Reusa pareceres compatíveis e cobra somente evidências ainda sem parecer."""

    def __init__(self, salvo, ativo):
        self.salvo, self.ativo = salvo, ativo
        self._on_update = None

    @property
    def chamadas(self):
        return self.ativo.chamadas

    @property
    def custo_estimado(self):
        return self.ativo.custo_estimado

    @property
    def registros(self):
        return self.salvo.registros + self.ativo.registros

    @property
    def on_update(self):
        return self._on_update

    @on_update.setter
    def on_update(self, callback):
        self._on_update = callback
        self.ativo.on_update = callback

    def julgar(self, registro):
        if digest(registro) in self.salvo.dados["julgamentos"]:
            try:
                return self.salvo.julgar(registro)
            finally:
                if self.on_update:
                    self.on_update()
        return self.ativo.julgar(registro)
