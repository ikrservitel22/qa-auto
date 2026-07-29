import json
import os

BASE_DIR = os.path.dirname(__file__)

RUTA_CREDENCIALES = os.path.join(BASE_DIR, "credentials.json")

with open(RUTA_CREDENCIALES, "r", encoding="utf-8") as archivo:
    CONFIG = json.load(archivo)

URL = CONFIG["url"]
USUARIO = CONFIG["usuario"]
PASSWORD = CONFIG["password"]