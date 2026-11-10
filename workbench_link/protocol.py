"""Canonical v1 codec. Validate before allocating, persisting or executing."""

import base64
import binascii
import hashlib
import json
import re
import uuid

from .errors import Code, LinkError

VERSION = 1
SCRIPT_LIMIT = 256 * 1024
STDIN_LIMIT = 4 * 1024 * 1024
CHUNK_LIMIT = 64 * 1024
OUTPUT_LIMIT = 16 * 1024 * 1024
WIRE_LIMIT = 6 * 1024 * 1024
CONTROL_LIMIT = WIRE_LIMIT
TIMEOUT_LIMIT = 600
SLUG = re.compile(r"[A-Za-z0-9_-]{1,64}\Z")
HEX = re.compile(r"[0-9a-f]{64}\Z")
ENVELOPE_FIELDS = frozenset({"protocol_version", "profile_id", "binding_id", "generation",
    "environment_id", "operation_id", "worker_id", "worker_instance_id", "project_id",
    "script", "login", "stdin_b64", "timeout_seconds", "payload_sha256"})
RECEIPT_FIELDS = frozenset({"operation_id", "payload_sha256", "binding_id", "generation",
    "worker_instance_id", "start_grant_id", "terminal_kind", "exit_code", "output_bytes",
    "output_sha256", "last_sequence", "termination_confirmed", "termination_method",
    "output_complete", "error_code", "worker_elapsed_ms"})


def bad(message: str):
    raise LinkError(Code.BAD_REQUEST, message)


def canonical(value) -> bytes:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                          allow_nan=False).encode("utf-8")
    except (ValueError, TypeError, UnicodeError):
        bad("Value is not canonical UTF-8 JSON.")


def _pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            bad("Duplicate JSON field.")
        obj[key] = value
    return obj


def decode(data: bytes, limit: int = WIRE_LIMIT) -> dict:
    if len(data) > limit:
        bad("Request exceeds the wire limit.")
    try:
        result = json.loads(data.decode("utf-8"), object_pairs_hook=_pairs,
                            parse_constant=lambda _: bad("Nonfinite number."))
    except (ValueError, UnicodeError, RecursionError):
        bad("Malformed JSON.")
    if type(result) is not dict:
        bad("Expected a JSON object.")
    return result


def fields(obj: dict, required, optional=()):
    if type(obj) is not dict or not set(required) <= obj.keys() or obj.keys() - set(required) - set(optional):
        bad("Missing or unsupported fields.")


def integer(value, name: str, low: int = 0, high: int = 2**63 - 1) -> int:
    if type(value) is not int or not low <= value <= high:
        bad(f"Invalid {name}.")
    return value


def text(value, name: str, maximum: int = 256) -> str:
    if type(value) is not str or len(value) > maximum or any(c in value for c in "\r\n\x00"):
        bad(f"Invalid {name}.")
    return value


def identifier(value, name: str = "identifier") -> str:
    text(value, name, 36)
    try:
        if str(uuid.UUID(value)) != value:
            bad(f"Invalid {name}.")
    except ValueError:
        bad(f"Invalid {name}.")
    return value


def slug(value, name: str = "worker_id") -> str:
    if type(value) is not str or not SLUG.fullmatch(value):
        bad(f"Invalid {name}.")
    return value


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hash_field(value, name="digest") -> str:
    if type(value) is not str or not HEX.fullmatch(value):
        bad(f"Invalid {name}.")
    return value


def b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def unb64(value, limit: int) -> bytes:
    if type(value) is not str or len(value) > 4 * ((limit + 2) // 3):
        bad("Encoded bytes exceed the limit.")
    try:
        data = base64.b64decode(value, validate=True)
    except (ValueError, binascii.Error):
        bad("Invalid base64.")
    if len(data) > limit or b64(data) != value:
        bad("Invalid or oversized base64.")
    return data


def payload_hash(envelope: dict) -> str:
    return digest(canonical({k: v for k, v in envelope.items() if k != "payload_sha256"}))


def envelope(obj: dict) -> dict:
    fields(obj, ENVELOPE_FIELDS, {'lifecycle', 'terminate_process'})
    if obj.get('lifecycle', 'operation') not in ('operation', 'session'):
        bad('Invalid lifecycle scope.')
    if 'terminate_process' in obj:
        process_inventory([obj['terminate_process']])
        if obj.get('lifecycle') != 'session':
            bad('Process termination requires session ownership.')
    integer(obj["protocol_version"], "protocol_version", VERSION, VERSION)
    for name in ("profile_id", "binding_id", "environment_id", "operation_id",
                 "worker_instance_id", "project_id"):
        identifier(obj[name], name)
    slug(obj["worker_id"])
    integer(obj["generation"], "generation", 1)
    integer(obj["timeout_seconds"], "timeout_seconds", 1, TIMEOUT_LIMIT)
    if type(obj["login"]) is not bool:
        bad("Invalid login flag.")
    if type(obj["script"]) is not str or "\x00" in obj["script"]:
        bad("Invalid script.")
    try:
        if len(obj["script"].encode("utf-8")) > SCRIPT_LIMIT:
            bad("Script exceeds the limit.")
    except UnicodeError:
        bad("Script is not UTF-8.")
    unb64(obj["stdin_b64"], STDIN_LIMIT)
    hash_field(obj["payload_sha256"])
    if payload_hash(obj) != obj["payload_sha256"]:
        raise LinkError(Code.PAYLOAD_CONFLICT, "Payload digest does not match.", obj["operation_id"])
    return obj


def receipt(obj: dict) -> dict:
    fields(obj, RECEIPT_FIELDS, {'termination_scope', 'detached_processes'})
    scope = obj.get('termination_scope', 'environment')
    if scope not in ('foreground', 'environment'):
        bad('Invalid termination scope.')
    processes = process_inventory(obj.get('detached_processes', []))
    if scope == 'environment' and processes:
        bad('Environment termination cannot leave detached processes.')
    if scope == 'foreground' and (obj['terminal_kind'] != 'completed' or
                                  obj['termination_method'] != 'natural'):
        bad('Foreground receipts require natural completion.')
    if scope == 'foreground' and 'detached_processes' not in obj:
        bad('Foreground receipts require an explicit process inventory.')
    for name in ("operation_id", "binding_id", "worker_instance_id", "start_grant_id"):
        identifier(obj[name], name)
    for name in ("payload_sha256", "output_sha256"):
        hash_field(obj[name], name)
    integer(obj["generation"], "generation", 1)
    integer(obj["output_bytes"], "output_bytes", 0, OUTPUT_LIMIT)
    integer(obj["last_sequence"], "last_sequence", -1)
    integer(obj["worker_elapsed_ms"], "worker_elapsed_ms")
    for name in ("termination_confirmed", "output_complete"):
        if type(obj[name]) is not bool:
            bad(f"Invalid {name}.")
    if not obj["termination_confirmed"]:
        bad("A terminal receipt requires confirmed termination.")
    if obj["terminal_kind"] not in ("completed", "cancelled", "not_started"):
        bad("Invalid terminal kind.")
    if obj["terminal_kind"] == "completed":
        integer(obj["exit_code"], "exit_code", -255, 255)
    elif obj["exit_code"] is not None:
        bad("Cancellation/no-start cannot invent an exit code.")
    if obj["termination_method"] not in ("natural", "group_term", "group_kill", "container_stop", "never_started"):
        bad("Invalid termination method.")
    if obj["error_code"] is not None:
        try:
            Code(obj["error_code"])
        except (ValueError, TypeError):
            bad("Invalid error code.")
    if not obj["output_complete"] and obj["error_code"] is None:
        bad("Incomplete output requires an error.")
    if obj["output_bytes"] == 0 and (obj["last_sequence"] != -1 or obj["output_sha256"] != digest(b"")):
        bad("Invalid empty-output receipt.")
    return obj


def process_inventory(value):
    if type(value) is not list or len(value) > 128:
        bad('Invalid detached process inventory.')
    seen = set()
    for process in value:
        fields(process, {'pid', 'start_ticks'})
        integer(process['pid'], 'pid', 2, 2**31 - 1)
        integer(process['start_ticks'], 'start_ticks', 1)
        if process['pid'] in seen:
            bad('Duplicate process identity.')
        seen.add(process['pid'])
    return value
