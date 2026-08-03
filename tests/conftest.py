import logging
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import glob
from datetime import datetime
from utili.config import *
from utili.locators import *
from utili.logger import logger



@pytest.fixture(scope="session", autouse=True)
def reset_logger():
    os.makedirs("/workspace/reports/logs", exist_ok=True)

    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()

    archivo = logging.FileHandler(
        "/workspace/reports/logs/ejecucion.log",
        mode="w",
        encoding="utf-8"
    )

    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    archivo.setFormatter(formato)
    logger.addHandler(archivo)

    yield

    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()

@pytest.fixture
def driver():

    # Crear la carpeta si no existe
    os.makedirs("/workspace/descargas", exist_ok=True)

    # Eliminar archivos de descargas anteriores
    for archivo in glob.glob("/workspace/descargas/*"):
        os.remove(archivo)

    options = Options()

    prefs = {
        "download.default_directory": "/workspace/descargas",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }

    options.add_experimental_option("prefs", prefs)

    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-notifications")

    driver = webdriver.Remote(
        command_executor="http://selenium-chrome:4444/wd/hub",
        options=options
    )

    driver.get(URL)

    yield driver

    driver.quit()

@pytest.fixture
def driver_logueado(driver):

    logger.info("========== INICIO TEST ==========")

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
    logger.info("LOGIN EN FIXTURE driver_logueado EXITOSO")
    logger.info("========== FIN FIXTURE driver_logueado ==========")

    return driver