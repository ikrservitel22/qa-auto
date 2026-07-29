from datetime import datetime
import os

os.makedirs("reports/logs", exist_ok=True)


def escribir_log(nombre_test, mensaje):

    archivo = f"reports/logs/{nombre_test}.log"

    with open(archivo, "a", encoding="utf-8") as log:

        hora = datetime.now().strftime("%H:%M:%S")

        log.write(f"[{hora}] {mensaje}\n")