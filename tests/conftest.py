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
    os.makedirs("/workspace/reports/screen", exist_ok=True)

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

    # limpiar capturas previas
    for archivo_scr in glob.glob("/workspace/reports/screen/*"):
        try:
            os.remove(archivo_scr)
        except Exception:
            pass

    yield

    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()


@pytest.fixture
def driver():
    # Host directory where test runner expects downloads to appear
    host_download_dir = "/workspace/descargas"
    os.makedirs(host_download_dir, exist_ok=True)

    # Clean previous downloads on the host side
    for archivo in glob.glob(f"{host_download_dir}/*"):
        try:
            os.remove(archivo)
        except Exception:
            pass

    # Path inside the Selenium/browser container where Chrome will actually write downloads.
    # IMPORTANT: you must bind-mount the host `host_download_dir` to this container path
    # when launching the Selenium node (example below).
    container_download_dir = os.environ.get("SELENIUM_CONTAINER_DOWNLOAD_DIR", "/home/seluser/descargas")

    options = Options()

    prefs = {
        # Path inside the browser container
        "download.default_directory": container_download_dir,
        # No preguntar dónde guardar
        "download.prompt_for_download": False,
        # Crear/usar la carpeta automáticamente
        "download.directory_upgrade": True,
        # Evitar que Chrome intente abrir ciertos tipos (ej. PDF)
        "plugins.always_open_pdf_externally": True,
        # Evitar popup de descargas
        "profile.default_content_settings.popups": 0,
        # Relajar protecciones de safebrowsing para permitir descargas automáticas en CI
        "safebrowsing.enabled": True,
        "safebrowsing.disable_download_protection": True,
        # Desactivar servicios que guardan credenciales
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }

    options.add_argument("--disable-features=FileSystemAccessAPI")
    options.add_experimental_option("prefs", prefs)

    # Abrir Chrome maximizado
    options.add_argument("--start-maximized")

    # Evitar mensaje "Chrome está siendo controlado..."
    options.add_experimental_option(
        "excludeSwitches",
        ["enable-automation"]
    )

    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-notifications")

    driver = webdriver.Remote(
        command_executor="http://selenium-chrome:4444/wd/hub",
        options=options
    )

    # Forzar comportamiento de descargas vía CDP para Chromedriver/Chrome
    # Esto le indica al navegador la carpeta donde escribir descargas sin mostrar diálogos.
    try:
        driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": container_download_dir
        })
    except Exception:
        # Algunos drivers/remotes pueden no soportar CDP; en ese caso las prefs ayudan.
        pass

    driver.get(URL)

    # Nota para el usuario: asegúrate de montar la carpeta del host en el contenedor
    # por ejemplo, en `docker run` o `docker-compose` del nodo Chrome:
    # -v /workspace/descargas:/home/seluser/descargas
    # Si usas otra ruta dentro del contenedor cambia la variable de entorno
    # `SELENIUM_CONTAINER_DOWNLOAD_DIR` para que coincida.

    yield driver

    driver.quit()


@pytest.fixture
def driver_logueado(driver):
    logger.info(f"URL: {URL}")
    logger.info(f"USUARIO: {USUARIO}")

    # Esperar elementos de login
    WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, LOGIN_USUARIO))
    )
    driver.find_element(By.XPATH, LOGIN_USUARIO).send_keys(USUARIO)

    WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, LOGIN_PASSWORD))
    )
    driver.find_element(By.XPATH, LOGIN_PASSWORD).send_keys(PASSWORD)

    WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, LOGIN_BOTON))
    )
    driver.find_element(By.XPATH, LOGIN_BOTON).click()

    WebDriverWait(driver, TIMEOUT).until(
        EC.url_contains("dashboard")
    )

    logger.info(f"URL actual: {driver.current_url}")
    logger.info("LOGIN EN FIXTURE driver_logueado EXITOSO")

    yield driver