import asyncio
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import requests

from orchestrator_api.app.models import RunStatus, Suite
from orchestrator_api.app.store import store

WORKSPACE = Path("/workspace")
REPORTS_DIR = WORKSPACE / "reports"
RUNS_DIR = REPORTS_DIR / "runs"
FIXED_LOGS_DIR = REPORTS_DIR / "logs"
FIXED_SCREEN_DIR = REPORTS_DIR / "screen"

SUITE_PATHS = {
    Suite.admin: "tests/tests_intranet/test_usu_admin",
    Suite.desarrollo: "tests/tests_intranet/test_usu_desarrollo",
    Suite.unit: "tests/test_utili_errores.py",
}

GRID_STATUS_URL = "http://selenium-chrome:4444/wd/hub/status"
GRID_READY_TIMEOUT_S = 60
GRID_POLL_INTERVAL_S = 2
RUN_TIMEOUT_S = 45 * 60


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _grid_ready(timeout_s: int = GRID_READY_TIMEOUT_S) -> bool:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        try:
            resp = requests.get(GRID_STATUS_URL, timeout=5)
            if resp.status_code == 200 and resp.json().get("value", {}).get("ready"):
                return True
        except requests.RequestException:
            pass
        time.sleep(GRID_POLL_INTERVAL_S)
    return False


def _archive_fixed_artifacts(run_id: str) -> None:
    run_dir = RUNS_DIR / run_id

    ejecucion_log = FIXED_LOGS_DIR / "ejecucion.log"
    if ejecucion_log.exists():
        shutil.copy2(ejecucion_log, run_dir / "ejecucion.log")

    resumen_ia = FIXED_LOGS_DIR / "resumen_ia.txt"
    if resumen_ia.exists():
        shutil.copy2(resumen_ia, run_dir / "resumen_ia.txt")

    if FIXED_SCREEN_DIR.exists() and any(FIXED_SCREEN_DIR.iterdir()):
        screen_dest = run_dir / "screen"
        screen_dest.mkdir(exist_ok=True)
        for f in FIXED_SCREEN_DIR.iterdir():
            if f.is_file():
                shutil.copy2(f, screen_dest / f.name)


def _status_from_exit_code(exit_code: Optional[int], timed_out: bool) -> RunStatus:
    if timed_out:
        return RunStatus.timed_out
    if exit_code == 0:
        return RunStatus.passed
    if exit_code == 1:
        return RunStatus.failed
    return RunStatus.error


class RunQueue:
    def __init__(self) -> None:
        self._queue: "asyncio.Queue[str]" = asyncio.Queue()
        self._worker_task: Optional[asyncio.Task] = None
        self._current_proc: Optional[subprocess.Popen] = None

    def start(self) -> None:
        self._worker_task = asyncio.create_task(self._worker())

    async def stop(self) -> None:
        if self._current_proc is not None:
            self._current_proc.terminate()
            try:
                self._current_proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self._current_proc.kill()
        if self._worker_task is not None:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass

    async def enqueue(self, run_id: str) -> None:
        await self._queue.put(run_id)

    async def _worker(self) -> None:
        while True:
            run_id = await self._queue.get()
            await self._process(run_id)

    async def _process(self, run_id: str) -> None:
        record = store.get(run_id)
        if record is None:
            return
        suite = record.suite
        loop = asyncio.get_event_loop()

        ready = await loop.run_in_executor(None, _grid_ready)
        if not ready:
            store.update(
                run_id,
                status=RunStatus.error,
                started_at=_now(),
                finished_at=_now(),
                error_message="selenium grid not ready",
            )
            return

        store.update(run_id, status=RunStatus.running, started_at=_now())

        exit_code, timed_out = await loop.run_in_executor(
            None, self._run_pytest, suite, run_id
        )

        await loop.run_in_executor(None, _archive_fixed_artifacts, run_id)

        status = _status_from_exit_code(exit_code, timed_out)
        store.update(
            run_id,
            status=status,
            finished_at=_now(),
            exit_code=exit_code,
            error_message="pytest run timed out" if timed_out else None,
        )

    def _run_pytest(self, suite: Suite, run_id: str) -> tuple[Optional[int], bool]:
        run_dir = RUNS_DIR / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        suite_path = SUITE_PATHS[suite]
        report_path = run_dir / "reporte.html"
        stdout_path = run_dir / "stdout.log"

        cmd = [
            "python", "-m", "pytest", "-s", suite_path,
            f"--html={report_path}", "--self-contained-html",
        ]

        with open(stdout_path, "w", encoding="utf-8") as stdout_file:
            proc = subprocess.Popen(
                cmd, cwd=WORKSPACE, stdout=stdout_file, stderr=subprocess.STDOUT,
            )
            self._current_proc = proc
            try:
                returncode = proc.wait(timeout=RUN_TIMEOUT_S)
                return returncode, False
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
                return None, True
            finally:
                self._current_proc = None


queue = RunQueue()
