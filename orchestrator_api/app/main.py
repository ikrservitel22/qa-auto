import shutil
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from orchestrator_api.app.analyzer import compare_runs
from orchestrator_api.app.models import (
    CompareResult,
    DeleteResult,
    RunRecord,
    RunRequest,
    RunStatus,
    Suite,
)
from orchestrator_api.app.runner import RUNS_DIR, queue
from orchestrator_api.app.store import store

ACTIVE_STATUSES = {RunStatus.queued, RunStatus.running}


@asynccontextmanager
async def lifespan(app: FastAPI):
    queue.start()
    yield
    await queue.stop()


app = FastAPI(title="orchestrator-api", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/runs", status_code=202)
async def create_run(request: RunRequest) -> RunRecord:
    run_id = uuid.uuid4().hex
    record = RunRecord(
        run_id=run_id,
        suite=request.suite,
        status=RunStatus.queued,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    store.add(record)
    await queue.enqueue(run_id)
    return record


@app.get("/runs")
async def list_runs(limit: int = 50) -> list[RunRecord]:
    return store.list_recent(limit)


@app.get("/runs/compare")
async def get_runs_compare(run_a: str, run_b: str) -> CompareResult:
    if not (RUNS_DIR / run_a).exists():
        raise HTTPException(status_code=404, detail=f"run {run_a} not found")
    if not (RUNS_DIR / run_b).exists():
        raise HTTPException(status_code=404, detail=f"run {run_b} not found")
    return compare_runs(run_a, run_b)


@app.get("/runs/{run_id}")
async def get_run(run_id: str) -> RunRecord:
    record = store.get(run_id)
    if record is None:
        raise HTTPException(status_code=404, detail="run not found")
    return record


@app.get("/runs/{run_id}/report")
async def get_run_report(run_id: str):
    report_path = RUNS_DIR / run_id / "reporte.html"
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="report not available for this run")
    return FileResponse(report_path, media_type="text/html")


@app.get("/runs/{run_id}/logs")
async def get_run_logs(run_id: str):
    log_path = RUNS_DIR / run_id / "stdout.log"
    if not log_path.exists():
        raise HTTPException(status_code=404, detail="log not available for this run")
    return FileResponse(log_path, media_type="text/plain")


@app.get("/runs/{run_id}/resumen")
async def get_run_resumen(run_id: str):
    resumen_path = RUNS_DIR / run_id / "resumen_ia.txt"
    if not resumen_path.exists():
        raise HTTPException(status_code=404, detail="resumen_ia.txt not available for this run")
    return FileResponse(resumen_path, media_type="text/plain")


@app.delete("/runs/{run_id}")
async def delete_run(run_id: str) -> DeleteResult:
    record = store.get(run_id)
    if record is not None and record.status in ACTIVE_STATUSES:
        raise HTTPException(status_code=409, detail="cannot delete an active run")
    run_dir = RUNS_DIR / run_id
    if record is None and not run_dir.exists():
        raise HTTPException(status_code=404, detail="run not found")
    if run_dir.exists():
        shutil.rmtree(run_dir)
    store.remove(run_id)
    return DeleteResult(deleted_run_ids=[run_id], skipped_active=[])


@app.delete("/runs")
async def delete_runs(
    suite: Optional[Suite] = None, status: Optional[RunStatus] = None
) -> DeleteResult:
    active_ids = {r.run_id for r in store.list_recent(limit=1000) if r.status in ACTIVE_STATUSES}
    deleted = []
    skipped = []
    if not RUNS_DIR.exists():
        return DeleteResult(deleted_run_ids=[], skipped_active=[])

    for entry in sorted(RUNS_DIR.iterdir()):
        if not entry.is_dir():
            continue
        run_id = entry.name
        if run_id in active_ids:
            skipped.append(run_id)
            continue
        record = store.get(run_id)
        if suite is not None and (record is None or record.suite != suite):
            continue
        if status is not None and (record is None or record.status != status):
            continue
        shutil.rmtree(entry)
        store.remove(run_id)
        deleted.append(run_id)

    return DeleteResult(deleted_run_ids=deleted, skipped_active=skipped)
