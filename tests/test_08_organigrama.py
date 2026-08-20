from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pytest
import inspect
from utili.config import *
from utili.logger import logger
from utili.errores import manejar_error_test
from utili.locators import (
    SIDEBAR_ORGANIGRAMA_BUTTON,
    MENU_ORGANIGRAMA_COMPLETO,
    MENU_ORGANIGRAMA_AREAS_LIDERES,
    MENU_ORGANIGRAMA_MI_AREA,
    ORGANIGRAMA_PAGE_TITLE,
)
from utili.waits import click_sidebar_menu_item, wait_text_in_element

@pytest.mark.dependency(name="modulo_organigrama_ok", depends=["login_ok"], scope="session")
def test_organigrama_flujo(driver_logueado):

    try:
        logger.info("========== INICIO TEST_ORGANIGRAMA_FLUJO ==========")

        logger.info("Click en Organigrama > Completo")
        click_sidebar_menu_item(
            driver_logueado,
            "Organigrama", SIDEBAR_ORGANIGRAMA_BUTTON,
            "Completo", MENU_ORGANIGRAMA_COMPLETO,
        )

        logger.info("Esperando título 'Organigrama'")
        wait_text_in_element(driver_logueado, ORGANIGRAMA_PAGE_TITLE, 'Organigrama')

        logger.info("Click en Organigrama > Áreas y líderes")
        click_sidebar_menu_item(
            driver_logueado,
            "Organigrama", SIDEBAR_ORGANIGRAMA_BUTTON,
            "Áreas y líderes", MENU_ORGANIGRAMA_AREAS_LIDERES,
        )

        logger.info("Esperando título 'Áreas y Líderes'")
        wait_text_in_element(driver_logueado, ORGANIGRAMA_PAGE_TITLE, 'Áreas y Líderes')

        logger.info("Click en Organigrama > Mi área")
        click_sidebar_menu_item(
            driver_logueado,
            "Organigrama", SIDEBAR_ORGANIGRAMA_BUTTON,
            "Mi área", MENU_ORGANIGRAMA_MI_AREA,
        )

        logger.info("Esperando título 'Mi Área'")
        wait_text_in_element(driver_logueado, ORGANIGRAMA_PAGE_TITLE, 'Mi Área')

        logger.info("TEST_ORGANIGRAMA_FLUJO COMPLETADO")
        logger.info("========== FIN TEST_ORGANIGRAMA_FLUJO ==========")

    except Exception as e:
        manejar_error_test(driver_logueado, e, inspect.currentframe().f_code.co_name)
        raise