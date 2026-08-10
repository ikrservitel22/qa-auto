from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

from utili.config import *
from utili.logger import logger
from utili.errores import tipificar_error
from utili.locators import (
    SIDEBAR_ORGANIGRAMA_BUTTON,
    MENU_ORGANIGRAMA_COMPLETO,
    MENU_ORGANIGRAMA_AREAS_LIDERES,
    MENU_ORGANIGRAMA_MI_AREA,
    ORGANIGRAMA_PAGE_TITLE,
)
from utili.waits import click_when_clickable, wait_text_in_element


def test_organigrama_flujo(driver_logueado):

    try:

        logger.info("========== INICIO TEST_ORGANIGRAMA_FLUJO ==========")

        logger.info("Click en Organigrama")
        click_when_clickable(driver_logueado, SIDEBAR_ORGANIGRAMA_BUTTON)

        logger.info("Click en Completo")
        click_when_clickable(driver_logueado, MENU_ORGANIGRAMA_COMPLETO)

        logger.info("Esperando título 'Organigrama'")
        wait_text_in_element(driver_logueado, ORGANIGRAMA_PAGE_TITLE, 'Organigrama')

        logger.info("Click en segundo modo de organigrama")
        click_when_clickable(driver_logueado, MENU_ORGANIGRAMA_AREAS_LIDERES)

        logger.info("Esperando título 'Áreas y Líderes'")
        wait_text_in_element(driver_logueado, ORGANIGRAMA_PAGE_TITLE, 'Áreas y Líderes')

        logger.info("Click en tercer modo de organigrama")
        click_when_clickable(driver_logueado, MENU_ORGANIGRAMA_MI_AREA)

        logger.info("Esperando título 'Mi Área'")
        wait_text_in_element(driver_logueado, ORGANIGRAMA_PAGE_TITLE, 'Mi Área')

        logger.info("TEST_ORGANIGRAMA_FLUJO COMPLETADO")
        logger.info("========== FIN TEST_ORGANIGRAMA_FLUJO ==========")

    except Exception as e:

        tipo_error = tipificar_error(e)

        logger.error("========== ERROR: TEST_ORGANIGRAMA_FLUJO ==========")
        logger.error(f"TIPO DE ERROR: {tipo_error}")
        logger.error(f"DETALLE: {e}")
        logger.error(f"URL: {driver_logueado.current_url}")

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = f"reports/screen/organigrama_{nombre}.png"
        driver_logueado.save_screenshot(ruta)

        logger.error(f"CAPTURA: {ruta}")
        logger.error("========== FIN TEST_ORGANIGRAMA_FLUJO ==========")

        raise
