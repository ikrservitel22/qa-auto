from collections import OrderedDict
from threading import Lock
from typing import Optional

from orchestrator_api.app.models import RunRecord

MAX_RUNS = 50


class RunStore:
    def __init__(self) -> None:
        self._runs: "OrderedDict[str, RunRecord]" = OrderedDict()
        self._lock = Lock()

    def add(self, record: RunRecord) -> None:
        with self._lock:
            self._runs[record.run_id] = record
            while len(self._runs) > MAX_RUNS:
                self._runs.popitem(last=False)

    def get(self, run_id: str) -> Optional[RunRecord]:
        with self._lock:
            return self._runs.get(run_id)

    def update(self, run_id: str, **fields) -> Optional[RunRecord]:
        with self._lock:
            record = self._runs.get(run_id)
            if record is None:
                return None
            updated = record.model_copy(update=fields)
            self._runs[run_id] = updated
            return updated

    def list_recent(self, limit: int = MAX_RUNS) -> list[RunRecord]:
        with self._lock:
            return list(self._runs.values())[-limit:][::-1]

    def remove(self, run_id: str) -> bool:
        with self._lock:
            return self._runs.pop(run_id, None) is not None


store = RunStore()
