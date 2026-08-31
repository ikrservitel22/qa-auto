from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Suite(str, Enum):
    admin = "admin"
    desarrollo = "desarrollo"
    unit = "unit"


class RunStatus(str, Enum):
    queued = "queued"
    running = "running"
    passed = "passed"
    failed = "failed"
    timed_out = "timed_out"
    interrupted = "interrupted"
    error = "error"


class RunRequest(BaseModel):
    suite: Suite


class RunRecord(BaseModel):
    run_id: str
    suite: Suite
    status: RunStatus
    created_at: str
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    exit_code: Optional[int] = None
    error_message: Optional[str] = None


class FailureRecord(BaseModel):
    test: str
    archivo: str
    tipo_error: str
    mensaje: str
    url: str


class CompareCounts(BaseModel):
    shared: int
    unique_to_a: int
    unique_to_b: int


class CompareResult(BaseModel):
    run_a: str
    run_b: str
    shared_failures: list[FailureRecord]
    unique_to_a: list[FailureRecord]
    unique_to_b: list[FailureRecord]
    counts: CompareCounts


class DeleteResult(BaseModel):
    deleted_run_ids: list[str]
    skipped_active: list[str]
