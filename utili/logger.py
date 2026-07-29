import logging
import os

os.makedirs("reports/logs", exist_ok=True)

logger = logging.getLogger("automatizacion")
logger.setLevel(logging.INFO)

if not logger.handlers:

    archivo = logging.FileHandler(
        "reports/logs/ejecucion.log",
        encoding="utf-8"
    )

    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    archivo.setFormatter(formato)

    logger.addHandler(archivo)