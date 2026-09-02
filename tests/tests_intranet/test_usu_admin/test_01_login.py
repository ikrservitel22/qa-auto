from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import inspect
from utili.config import *
from utili.locators import *
from utili.logger import logger
from utili.errores import tipificar_error, es_pagina_error_servidor, guardar_texto_pagina_error, manejar_error_test
from utili.waits import send_keys_when_visible, click_when_clickable, wait_visible_xpath
from utili.screenshot_full import capturar_pantalla_completa

@pytest.mark.dependency(name="login_ok", scope="session")
def test_login(driver):

    try:

        logger.info("========== INICIO TEST_LOGIN ==========")

        logger.info(f"URL: {URL}")
        logger.info(f"USUARIO: {USUARIO_ADMIN}")

        logger.info("Escribiendo usuario")
        send_keys_when_visible(driver, LOGIN_USUARIO, USUARIO_ADMIN)

        logger.info("Escribiendo contraseña")
        send_keys_when_visible(driver, LOGIN_PASSWORD, PASSWORD_ADMIN)

        logger.info("Pulsando botón Ingresar")
        click_when_clickable(driver, LOGIN_BOTON)

        logger.info("Esperando Dashboard")
        wait_visible_xpath(driver, "//*[contains(normalize-space(.), 'dashboard')]")

        logger.info(f"URL actual: {driver.current_url}")

        assert "dashboard" in driver.current_url

        logger.info("LOGIN EXITOSO")
        logger.info("========== FIN TEST_LOGIN ==========\n")

    except Exception as e:

        manejar_error_test(driver_logueado, e, inspect.currentframe().f_code.co_name)

        raise

@pytest.mark.dependency(depends=["login_ok"], scope="session")
def test_logout(driver_logueado):

    try:

        logger.info("========== INICIO TEST_LOGOUT ==========")

        logger.info("Abriendo menú lateral")

        # driver_logueado.find_element(
        #     By.XPATH,
        #     SIDEBAR_BOTON
        # ).click()

        logger.info("Pulsando Cerrar sesión")

        click_when_clickable(driver_logueado, LOGOUT_BOTON)

        logger.info("Esperando regresar al Login")
        WebDriverWait(driver_logueado, TIMEOUT).until(
            lambda d: d.current_url == URL
        )

        logger.info(f"URL actual: {driver_logueado.current_url}")

        assert driver_logueado.current_url == URL

        logger.info("LOGOUT EXITOSO")
        logger.info("========== FIN TEST_LOGOUT ==========\n")

    except Exception as e:

        manejar_error_test(driver_logueado, e, inspect.currentframe().f_code.co_name)

        raise