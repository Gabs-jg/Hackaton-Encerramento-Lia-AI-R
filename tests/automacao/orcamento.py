"""Controla as reservas e o custo estimado de cada lote e da conta.
Mantém o saldo entre execuções e protege a escrita simultânea do registro.
Este controle local não consulta nem substitui a fatura AWS.
"""

from contextlib import contextmanager
import json
import math
import os
from pathlib import Path


@contextmanager
def reservar(config, valor):
    gasto_externo = config.get("gasto_externo_usd")
    if (
        type(gasto_externo) not in (int, float)
        or not math.isfinite(gasto_externo)
        or gasto_externo < 0
    ):
        raise ValueError(
            "Informar gasto_externo_usd da conta, fora deste registro, antes do piloto pago."
        )
    if not config.get("conta_orcamento") or not config.get("arquivo_orcamento"):
        raise ValueError(
            "Informar identificador local da conta e arquivo persistente de orçamento."
        )
    caminho = Path(config["arquivo_orcamento"]).resolve()
    caminho.parent.mkdir(parents=True, exist_ok=True)
    trava = caminho.with_suffix(caminho.suffix + ".lock")
    descritor_trava = os.open(trava, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    os.close(descritor_trava)
    try:
        dados = (
            json.loads(caminho.read_text(encoding="utf-8"))
            if caminho.exists()
            else {"conta": config["conta_orcamento"], "estimado_usd": 0.0, "chamadas_reservadas": 0}
        )
        if dados["conta"] != config["conta_orcamento"]:
            raise ValueError("Arquivo de orçamento pertence a outra conta.")
        if (
            type(dados["estimado_usd"]) not in (int, float)
            or not math.isfinite(dados["estimado_usd"])
            or dados["estimado_usd"] < 0
        ):
            raise ValueError("Registro de orçamento inválido.")
        if dados["estimado_usd"] + gasto_externo + valor > 16:
            raise ValueError(
                "Reserva excede teto operacional de US$ 16; margem de US$ 4 preservada."
            )
        lote_id = config.get("lote_id", "piloto")
        limite_chamadas = config.get("max_chamadas_lote", config["max_chamadas"])
        limite_lote = config.get("limite_usd_lote", config["limite_usd"])
        lote = dados.setdefault("lotes", {}).setdefault(
            lote_id, {"estimado_usd": 0.0, "chamadas": 0}
        )
        if lote["chamadas"] >= limite_chamadas or lote["estimado_usd"] + valor > limite_lote:
            raise ValueError(
                "Limite acumulado do lote atingido; reiniciar o processo não libera chamadas."
            )
        lote["estimado_usd"] += valor
        lote["chamadas"] += 1
        dados["estimado_usd"] += valor
        total_reservado = dados["estimado_usd"]
        dados["chamadas_reservadas"] += 1
        dados["gasto_externo_informado_usd"] = gasto_externo

        def salvar():
            temporario = caminho.with_suffix(caminho.suffix + ".tmp")
            temporario.write_text(json.dumps(dados, indent=2), encoding="utf-8")
            os.replace(temporario, caminho)

        salvar()  # Interrupção mantém a reserva; não supor custo zero.
        try:
            yield dados
        finally:
            lote["estimado_usd"] += dados["estimado_usd"] - total_reservado
            salvar()
    finally:
        trava.unlink()
