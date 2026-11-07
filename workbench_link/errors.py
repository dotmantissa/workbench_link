"""Stable, safe errors shared by the broker, worker and native adapter."""

from enum import StrEnum


class Code(StrEnum):
    BAD_REQUEST = "BAD_REQUEST"
    AUTH_FAILED = "AUTH_FAILED"
    WORKER_UNAVAILABLE = "WORKER_UNAVAILABLE"
    WORKSPACE_BUSY = "WORKSPACE_BUSY"
    OUTCOME_UNKNOWN = "OUTCOME_UNKNOWN"
    CANCEL_PENDING = "CANCEL_PENDING"
    BINDING_STALE = "BINDING_STALE"
    PAYLOAD_CONFLICT = "PAYLOAD_CONFLICT"
    OUTPUT_CONFLICT = "OUTPUT_CONFLICT"
    OUTPUT_LIMIT = "OUTPUT_LIMIT"
    INTEGRITY_FAILURE = "INTEGRITY_FAILURE"
    STORAGE_UNAVAILABLE = "STORAGE_UNAVAILABLE"
    UNSUPPORTED_RUNTIME = "UNSUPPORTED_RUNTIME"
    NOT_STARTED = "NOT_STARTED"


class LinkError(RuntimeError):
    def __init__(self, code: Code, message: str, operation_id: str | None = None):
        self.code, self.message, self.operation_id = code, message, operation_id
        super().__init__(f"{code}: {message}")

    def as_dict(self) -> dict:
        return {"ok": False, "code": str(self.code), "message": self.message,
                "operation_id": self.operation_id}
