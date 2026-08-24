import os
import requests
from utili.logger import logger

# Se puede sobreescribir con una variable de entorno en el docker-compose
# de qa-auto si algún día cambia el nombre del servicio o el puerto.
IA_HISTORIAS_URL = os.environ.get(
    "IA_HISTORIAS_URL", "http://ia-historias:8000/procesar-errores-adjuntos"
)


def enviar_resumen_a_ia(ruta_resumen: str, fallidos: list[dict]):
    """
    Envía el resumen_ia.txt, junto con las capturas de pantalla y los
    textos de error de cada prueba fallida, al servicio ia-historias para
    que genere automáticamente las historias de usuario a revisar.

    Si el servicio no está disponible (apagado, red caída, etc.) esto NO
    debe hacer fallar la corrida de tests: solo se registra un warning en
    el log. El resumen_ia.txt sigue quedando guardado localmente igual
    que antes, así que nunca se pierde información.
    """
    if not fallidos:
        logger.info("No hay pruebas fallidas: no se envía nada a ia-historias.")
        return

    try:
        with open(ruta_resumen, "r", encoding="utf-8") as f:
            texto_resumen = f.read()
    except Exception as e:
        logger.error(f"No se pudo leer {ruta_resumen} para enviarlo a ia-historias: {e}")
        return

    # Cada prueba fallida puede tener una captura (.png) y/o un texto de
    # error de servidor (.txt) asociados. Se adjuntan usando SOLO el
    # nombre de archivo (sin ruta), que es justo lo que ia-historias usa
    # para emparejar cada adjunto con su bloque de error correspondiente.
    archivos_abiertos = []
    archivos_multipart = []
    try:
        for r in fallidos:
            for clave in ("captura", "texto_error"):
                ruta = r.get(clave)
                if ruta and os.path.isfile(ruta):
                    fh = open(ruta, "rb")
                    archivos_abiertos.append(fh)
                    archivos_multipart.append(("archivos", (os.path.basename(ruta), fh)))

        resp = requests.post(
            IA_HISTORIAS_URL,
            data={"errores": texto_resumen},
            files=archivos_multipart if archivos_multipart else None,
            # ia-historias procesa cada error uno por uno con la IA, así que
            # con varios errores fallidos esto puede tardar varios minutos.
            # Como ahora corre en un hilo aparte (ver conftest.py), un
            # timeout generoso no bloquea la salida de resultados de pytest.
            timeout=1200,
        )
        resp.raise_for_status()
        logger.info(f"Resumen enviado a ia-historias correctamente: {resp.json()}")
    except requests.RequestException as e:
        logger.warning(
            f"No se pudo enviar el resumen a ia-historias ({IA_HISTORIAS_URL}): {e}. "
            "El resumen sigue disponible localmente en resumen_ia.txt."
        )
    finally:
        for fh in archivos_abiertos:
            fh.close()