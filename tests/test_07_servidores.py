from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

from utili.config import *
from utili.logger import logger
from utili.locators import (
    MENU_SERVIDORES,
    SERVIDORES_PAGE_TITLE,
    SERVIDORES_PRIMER_ENLACE,
    SERVIDOR_DETAIL_TITLE,
)
from utili.errores import tipificar_error
from utili.waits import (
    click_when_clickable,
    wait_for_url,
    wait_text_in_element,
)


def test_servidores_flujo(driver_logueado):

    try:

        logger.info("========== INICIO TEST_SERVIDORES_FLUJO ==========")

        logger.info("Click en menú lateral - tercera opción")
        click_when_clickable(driver_logueado, MENU_SERVIDORES)

        logger.info("Esperando 'Inventario de Servidores'")
        wait_text_in_element(driver_logueado, SERVIDORES_PAGE_TITLE, 'Inventario de Servidores')

        logger.info("Click en primer servidor de la tabla")
        click_when_clickable(driver_logueado, SERVIDORES_PRIMER_ENLACE)

        logger.info("Esperando la URL del servidor específico")
        wait_for_url(driver_logueado, 'https://intranet.servitel.co/servidores/87')

        logger.info("Esperando etiqueta de servidor 'ALBOPVAPLCMIALIANZA1'")
        wait_text_in_element(driver_logueado, SERVIDOR_DETAIL_TITLE, 'ALBOPVAPLCMIALIANZA1')

        logger.info("TEST_SERVIDORES_FLUJO COMPLETADO")
        logger.info("========== FIN TEST_SERVIDORES_FLUJO ==========")

    except Exception as e:

        tipo_error = tipificar_error(e)

        logger.error("========== ERROR: TEST_SERVIDORES_FLUJO ==========")
        logger.error(f"TIPO DE ERROR: {tipo_error}")
        logger.error(f"DETALLE: {e}")
        logger.error(f"URL: {driver_logueado.current_url}")

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = f"reports/screen/servidores_{nombre}.png"
        driver_logueado.save_screenshot(ruta)

        logger.error(f"CAPTURA: {ruta}")
        logger.error("========== FIN TEST_SERVIDORES_FLUJO ==========")

        raise
