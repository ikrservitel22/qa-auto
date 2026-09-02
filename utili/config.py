import json
import os

BASE_DIR = os.path.dirname(__file__)

RUTA_CREDENCIALES = os.path.join(BASE_DIR, "credentials.json")

with open(RUTA_CREDENCIALES, "r", encoding="utf-8") as archivo:
    CONFIG = json.load(archivo)

URL = CONFIG["url"]

# Credenciales separadas por rol: cada suite (test_usu_admin, test_usu_desarrollo)
# debe usar la suya explícita (USUARIO_ADMIN/PASSWORD_ADMIN o
# USUARIO_DESARROLLO/PASSWORD_DESARROLLO) en vez de USUARIO/PASSWORD a secas.
# Este módulo se importa una sola vez por proceso, así que si una corrida
# combinada (pytest tests/) ejecuta ambas suites en el mismo proceso, un
# único USUARIO/PASSWORD global no podría representar a las dos a la vez.
USUARIO_ADMIN = CONFIG["admin"]["usuario"]
PASSWORD_ADMIN = CONFIG["admin"]["password"]
USUARIO_DESARROLLO = CONFIG["desarrollo"]["usuario"]
PASSWORD_DESARROLLO = CONFIG["desarrollo"]["password"]

# Se mantienen por compatibilidad con cualquier código que aún no distinga por rol.
USUARIO = USUARIO_ADMIN
PASSWORD = PASSWORD_ADMIN

# Valores y rutas adicionales (con defaults)
TIMEOUT = CONFIG.get("timeout", 10)

BASE_WORKSPACE = os.path.abspath(os.path.join(BASE_DIR, ".."))
REPORTS_DIR = CONFIG.get("reports_dir", os.path.abspath(os.path.join(BASE_WORKSPACE, "reports")))
LOGS_DIR = os.path.join(REPORTS_DIR, "logs")
SCREEN_DIR = os.path.join(REPORTS_DIR, "screen")
DOWNLOADS_DIR = CONFIG.get("downloads_dir", os.path.abspath(os.path.join(BASE_WORKSPACE, "descargas")))