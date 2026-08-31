from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
import pytest
import inspect
from utili.config import *
from utili.logger import logger
from utili.locators import (
    MENU_SERVIDORES,
    SERVIDORES_PAGE_TITLE,
    SERVIDORES_PRIMER_ENLACE,
    SERVIDOR_DETAIL_TITLE,
)
from utili.errores import manejar_error_test
from utili.waits import click_when_clickable, click_por_texto_o_xpath, wait_text_in_element

@pytest.mark.dependency(name="modulo_servidores_ok", depends=["login_ok"], scope="session")
def test_servidores_flujo(driver_logueado):

    try:
        logger.info("========== INICIO TEST_SERVIDORES_FLUJO ==========")

        logger.info("Click en menú lateral - Servidores")
        click_por_texto_o_xpath(driver_logueado, "Servidores", MENU_SERVIDORES)

        logger.info("Esperando 'Inventario de Servidores'")
        wait_text_in_element(driver_logueado, SERVIDORES_PAGE_TITLE, 'Inventario de Servidores')

        logger.info("Click en primer servidor de la tabla")
        click_when_clickable(driver_logueado, SERVIDORES_PRIMER_ENLACE)

        # Ya no exigimos un ID fijo, solo que sí navegó a un detalle de servidor (cualquiera)
        logger.info("Esperando navegar a un detalle de servidor")
        WebDriverWait(driver_logueado, TIMEOUT).until(
            lambda d: "/servidores/" in d.current_url and d.current_url.rstrip("/") != f"{URL}servidores"
        )
        logger.info(f"URL de detalle alcanzada: {driver_logueado.current_url}")

        # Capturamos el nombre real del servidor, sea cual sea
        elemento_detalle = WebDriverWait(driver_logueado, TIMEOUT).until(
            EC.visibility_of_element_located((By.XPATH, SERVIDOR_DETAIL_TITLE))
        )
        nombre_servidor_real = elemento_detalle.text.strip()
        logger.info(f"Servidor detectado dinámicamente: '{nombre_servidor_real}'")

        # Validamos que el título no esté vacío (confirma que sí cargó contenido real)
        assert nombre_servidor_real, "El título del servidor está vacío"

        logger.info("TEST_SERVIDORES_FLUJO COMPLETADO")
        logger.info("========== FIN TEST_SERVIDORES_FLUJO ==========")

    except Exception as e:
        manejar_error_test(driver_logueado, e, inspect.currentframe().f_code.co_name)
        raise