from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utili.config import *
from utili.locators import *
from utili.logger import logger
from utili.errores import tipificar_error


def test_login(driver):

    try:

        logger.info("========== INICIO TEST_LOGIN ==========")

        logger.info(f"URL: {URL}")
        logger.info(f"USUARIO: {USUARIO}")

        logger.info("Escribiendo usuario")
        driver.find_element(
            By.XPATH,
            LOGIN_USUARIO
        ).send_keys(USUARIO)

        logger.info("Escribiendo contraseña")
        driver.find_element(
            By.XPATH,
            LOGIN_PASSWORD
        ).send_keys(PASSWORD)

        logger.info("Pulsando botón Ingresar")
        driver.find_element(
            By.XPATH,
            LOGIN_BOTON
        ).click()

        logger.info("Esperando Dashboard")

        WebDriverWait(driver, 5).until(
            EC.url_contains("dashboard")
        )

        logger.info(f"URL actual: {driver.current_url}")

        assert "dashboard" in driver.current_url

        logger.info("LOGIN EXITOSO")
        logger.info("========== FIN TEST_LOGIN ==========\n")

    except Exception as e:

        tipo_error = tipificar_error(e)

        logger.error("========== ERROR: TEST_LOGIN ==========")
        logger.error(f"TIPO DE ERROR: {tipo_error}")
        logger.error(f"DETALLE: {e}")
        logger.error(f"URL: {driver.current_url}")

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        ruta = f"reports/screen/login_{nombre}.png"

        driver.save_screenshot(ruta)

        logger.error(f"CAPTURA: {ruta}")
        logger.error("========== FIN TEST_LOGIN ==========\n")

        raise


def test_logout(driver_logueado):

    try:

        logger.info("========== INICIO TEST_LOGOUT ==========")

        logger.info("Abriendo menú lateral")

        # driver_logueado.find_element(
        #     By.XPATH,
        #     SIDEBAR_BOTON
        # ).click()

        logger.info("Pulsando Cerrar sesión")

        driver_logueado.find_element(
            By.XPATH,
            LOGOUT_BOTON
        ).click()

        logger.info("Esperando regresar al Login")

        WebDriverWait(driver_logueado, 5).until(
            lambda d: d.current_url == URL
        )

        logger.info(f"URL actual: {driver_logueado.current_url}")

        assert driver_logueado.current_url == URL

        logger.info("LOGOUT EXITOSO")
        logger.info("========== FIN TEST_LOGOUT ==========\n")

    except Exception as e:

        tipo_error = tipificar_error(e)

        logger.error("========== ERROR: TEST_LOGOUT ==========")
        logger.error(f"TIPO DE ERROR: {tipo_error}")
        logger.error(f"DETALLE: {e}")
        logger.error(f"URL: {driver_logueado.current_url}")

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        ruta = f"reports/screen/login_{nombre}.png"

        driver_logueado.save_screenshot(ruta)

        logger.error(f"CAPTURA: {ruta}")
        logger.error("========== FIN TEST_LOGOUT ==========\n")

        raise