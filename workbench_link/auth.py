"""HMAC authenticates a transport peer; Hermes still authorizes commands."""

import hmac
import re
import secrets
import time

from .errors import Code, LinkError
from .protocol import VERSION, digest, identifier, slug

PATHS = frozenset("/v1/worker/" + p for p in
                  ("hello", "heartbeat", "poll", "accept", "running", "output", "result", "recover"))


def signing_input(method, path, timestamp, nonce, worker, instance, body_digest):
    return "\n".join(("WBL1", method, path, timestamp, nonce, worker, instance, body_digest)).encode("ascii")


def sign(key: bytes, path: str, worker: str, instance: str, body: bytes, *, now=None, nonce=None) -> dict:
    timestamp = str(int(time.time() if now is None else now))
    nonce = nonce or secrets.token_hex(16)
    body_digest = digest(body)
    signature = hmac.digest(key, signing_input("POST", path, timestamp, nonce, worker, instance, body_digest), "sha256").hex()
    return {"X-WBL-Version": str(VERSION), "X-WBL-Worker": worker, "X-WBL-Instance": instance,
            "X-WBL-Time": timestamp, "X-WBL-Nonce": nonce, "X-WBL-Body-SHA256": body_digest,
            "X-WBL-Signature": signature}


def verify(key: bytes, configured_worker: str, method: str, path: str, headers,
           body: bytes, consume_nonce, *, now=None) -> tuple[str, str]:
    # All metadata errors have one safe message; no headers/keys in exceptions.
    try:
        if method != "POST" or path not in PATHS:
            raise ValueError
        version = headers.get("X-WBL-Version")
        worker, instance = headers.get("X-WBL-Worker"), headers.get("X-WBL-Instance")
        timestamp, nonce = headers.get("X-WBL-Time"), headers.get("X-WBL-Nonce")
        body_digest, signature = headers.get("X-WBL-Body-SHA256"), headers.get("X-WBL-Signature")
        if version != "1" or worker != configured_worker:
            raise ValueError
        slug(worker); identifier(instance)
        if type(timestamp) is not str or not re.fullmatch(r"[0-9]{1,12}", timestamp):
            raise ValueError
        server_time = time.time() if now is None else now
        if abs(server_time - int(timestamp)) > 30:
            raise ValueError
        if type(nonce) is not str or not re.fullmatch(r"[0-9a-f]{32,64}", nonce):
            raise ValueError
        if type(signature) is not str or not re.fullmatch(r"[0-9a-f]{64}", signature):
            raise ValueError
        if body_digest != digest(body):
            raise ValueError
        expected = hmac.digest(key, signing_input(method, path, timestamp, nonce, worker, instance, body_digest), "sha256").hex()
        if not hmac.compare_digest(signature, expected):
            raise ValueError
    except (ValueError, TypeError, LinkError):
        raise LinkError(Code.AUTH_FAILED, "Invalid worker authentication; check key, identity and clock.") from None
    if not consume_nonce(worker, nonce, server_time):
        raise LinkError(Code.AUTH_FAILED, "Request nonce was already used or capacity was reached.")
    return worker, instance
