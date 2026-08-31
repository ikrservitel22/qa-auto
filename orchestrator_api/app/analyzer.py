import re
from pathlib import Path

from orchestrator_api.app.models import CompareCounts, CompareResult, FailureRecord
from orchestrator_api.app.runner import RUNS_DIR

_BLOCK_SEP = re.compile(r"^-{10,}$", re.MULTILINE)
_FIELD_RE = re.compile(r"^(TEST|ARCHIVO|TIPO_ERROR|MENSAJE|URL): (.*)$")


def _parse_resumen_ia(path: Path) -> list[FailureRecord]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    records = []
    for block in _BLOCK_SEP.split(text):
        block = block.strip()
        if not block.startswith("TEST:"):
            continue
        fields = {}
        for line in block.splitlines():
            if line.startswith("LOG_PASOS_INICIO"):
                break
            m = _FIELD_RE.match(line)
            if m:
                fields[m.group(1)] = m.group(2)
        if "TEST" in fields:
            records.append(FailureRecord(
                test=fields.get("TEST", ""),
                archivo=fields.get("ARCHIVO", ""),
                tipo_error=fields.get("TIPO_ERROR", ""),
                mensaje=fields.get("MENSAJE", ""),
                url=fields.get("URL", ""),
            ))
    return records


def _signature(record: FailureRecord) -> tuple[str, str, str]:
    archivo_normalizado = record.archivo.split("/")[-1]
    return (archivo_normalizado, record.test, record.tipo_error)


def compare_runs(run_a: str, run_b: str) -> CompareResult:
    failures_a = _parse_resumen_ia(RUNS_DIR / run_a / "resumen_ia.txt")
    failures_b = _parse_resumen_ia(RUNS_DIR / run_b / "resumen_ia.txt")

    sigs_a = {_signature(f) for f in failures_a}
    sigs_b = {_signature(f) for f in failures_b}

    shared = [f for f in failures_a if _signature(f) in sigs_b]
    unique_a = [f for f in failures_a if _signature(f) not in sigs_b]
    unique_b = [f for f in failures_b if _signature(f) not in sigs_a]

    return CompareResult(
        run_a=run_a,
        run_b=run_b,
        shared_failures=shared,
        unique_to_a=unique_a,
        unique_to_b=unique_b,
        counts=CompareCounts(
            shared=len(shared),
            unique_to_a=len(unique_a),
            unique_to_b=len(unique_b),
        ),
    )
