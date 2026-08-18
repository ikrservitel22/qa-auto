from vncdotool import api
from utili.logger import logger

def capturar_pantalla_completa(ruta_destino, host="selenium-chrome", puerto=5900, password="secret"):
    """
    Captura la pantalla COMPLETA del contenedor Chrome vía VNC,
    incluyendo diálogos nativos del sistema (ej. 'Guardar como').
    """
    try:
        client = api.connect(f'{host}::{puerto}', password=password)
        client.captureScreen(ruta_destino)
        client.disconnect()
        logger.info(f"Captura de pantalla completa (VNC) guardada: {ruta_destino}")
        return True
    except Exception as e:
        logger.error(f"No se pudo capturar pantalla completa vía VNC: {e}")
        return False