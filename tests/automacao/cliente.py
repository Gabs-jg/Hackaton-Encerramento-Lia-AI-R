"""Faz a comunicação HTTP com a Lia ou relê respostas históricas.
Preserva o corpo recebido e registra erros de conexão, sem julgar o conteúdo.
O modo replay não envia requisições à API.
"""

import json
import re
import socket
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

ENDPOINT = "https://rm4naioqykxiti2srofnqz6hqa0ctlav.lambda-url.us-east-1.on.aws/"


def agora() -> str:
    return datetime.now(timezone.utc).isoformat()


class SemRedirecionamento(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class ClienteLia:
    def __init__(self, chave: str, timeout: float = 180):
        self.chave, self.timeout = chave, timeout
        self.opener = build_opener(SemRedirecionamento())

    def enviar(self, payload: dict, turno: dict) -> dict:
        inicio, relogio = agora(), time.perf_counter()
        status, corpo, erro, tipo = None, None, None, None
        req = Request(
            ENDPOINT,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json", "x-api-key": self.chave},
            method="POST",
        )
        try:
            with self.opener.open(req, timeout=self.timeout) as resposta:
                status, tipo, corpo = (
                    resposta.status,
                    resposta.headers.get("Content-Type"),
                    resposta.read(),
                )
        except HTTPError as exc:
            status, tipo, corpo = exc.code, exc.headers.get("Content-Type"), exc.read()
        except (TimeoutError, socket.timeout):
            erro = "timeout"
        except URLError as exc:
            erro = (
                "timeout" if isinstance(exc.reason, (TimeoutError, socket.timeout)) else "conexao"
            )
        except OSError:
            erro = "conexao"
        texto = corpo.decode("utf-8", errors="replace") if corpo is not None else None
        try:
            dados = json.loads(texto) if texto is not None else None
        except json.JSONDecodeError:
            dados = None
            erro = erro or "json_invalido"
        return {
            "inicio_utc": inicio,
            "fim_utc": agora(),
            "duracao_http_segundos": round(time.perf_counter() - relogio, 6),
            "http_status": status,
            "content_type": tipo,
            "erro_tecnico": erro,
            "resposta_api": dados,
            "corpo_nao_json": texto if dados is None else None,
        }


class ClienteReplay:
    """Relê evidência existente; nunca representa uma nova execução da Lia."""

    def __init__(self, raiz):
        self.raiz = raiz

    def enviar(self, payload: dict, turno: dict) -> dict:
        from .casos import arquivo_local

        evidencia = json.loads(
            arquivo_local(self.raiz, turno["evidencia_replay"]).read_text(encoding="utf-8-sig")
        )
        esperado = dict(evidencia["requisicao"])
        template = esperado.get("sessao")
        if isinstance(template, str) and re.fullmatch(r"\{\{[A-Za-z0-9_]+\}\}", template):
            if evidencia["resposta"].get("sessao") != payload.get("sessao"):
                raise ValueError("Sessão do replay difere da sessão preservada na evidência.")
            esperado["sessao"] = payload["sessao"]
        if esperado != payload:
            raise ValueError("O replay não corresponde à mensagem/sessão solicitada.")
        return {
            "inicio_utc": agora(),
            "fim_utc": agora(),
            "duracao_http_segundos": None,
            "http_status": evidencia["httpStatus"],
            "content_type": "application/json",
            "erro_tecnico": None,
            "resposta_api": evidencia["resposta"],
            "corpo_nao_json": None,
            "fonte_replay": turno["evidencia_replay"],
            "coleta_original_utc": evidencia["capturadoEm"],
            "sessao_template_na_fonte": template if template != esperado.get("sessao") else None,
        }


class ClienteReplayGolden:
    """Consolidado histórico T14; exige igualdade exata das requisições."""

    def __init__(self, caminho, dataset):
        import hashlib

        self.caminho = caminho
        self.hash = hashlib.sha256(caminho.read_bytes()).hexdigest()
        self.registros = {}
        for r in json.loads(caminho.read_text(encoding="utf-8-sig"))["registros"]:
            chave = (r["caso"], r["turno"])
            if chave in self.registros:
                raise ValueError("Replay ambíguo: mais de uma execução do mesmo turno.")
            self.registros[chave] = r
        for c in dataset["casos"]:
            for n, t in enumerate(c["turnos"], 1):
                r = self.registros.get((c["id"], n))
                if not r or r["requisicao"]["mensagem"] != t["mensagem"]:
                    raise ValueError(
                        f'Replay não cobre a entrada de {c["id"]} T{n}. Selecione somente casos presentes.'
                    )

    def enviar(self, payload, turno):
        r = self.registros[(turno["caso_id"], turno["turno"])]
        if r["requisicao"] != payload:
            raise ValueError("Replay não corresponde à mensagem/sessão solicitada.")
        return {
            "inicio_utc": agora(),
            "fim_utc": agora(),
            "duracao_http_segundos": None,
            "http_status": r["http_status"],
            "erro_tecnico": r["erro_transporte"],
            "resposta_api": r["resposta_api"],
            "fonte_replay": str(self.caminho),
            "fonte_replay_sha256": self.hash,
            "coleta_original_utc": r["inicio_utc"],
            "content_type": "application/json",
            "corpo_nao_json": None,
        }
