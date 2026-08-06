import json
import os

BASE_DIR = os.path.dirname(__file__)

RUTA_CREDENCIALES = os.path.join(BASE_DIR, "credentials.json")

with open(RUTA_CREDENCIALES, "r", encoding="utf-8") as archivo:
    CONFIG = json.load(archivo)

URL = CONFIG["url"]
USUARIO = CONFIG["usuario"]
PASSWORD = CONFIG["password"]

# Valores y rutas adicionales (con defaults)
TIMEOUT = CONFIG.get("timeout", 10)

BASE_WORKSPACE = os.path.abspath(os.path.join(BASE_DIR, ".."))
REPORTS_DIR = CONFIG.get("reports_dir", os.path.abspath(os.path.join(BASE_WORKSPACE, "reports")))
LOGS_DIR = os.path.join(REPORTS_DIR, "logs")
SCREEN_DIR = os.path.join(REPORTS_DIR, "screen")
DOWNLOADS_DIR = CONFIG.get("downloads_dir", os.path.abspath(os.path.join(BASE_WORKSPACE, "descargas")))