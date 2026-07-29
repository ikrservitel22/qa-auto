import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import glob
from datetime import datetime
import pytest
from utili.config import *
from utili.locators import *

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

    driver = webdriver.Remote(
        command_executor="http://selenium-chrome:4444/wd/hub",
        options=options
    )

    driver.get(URL)

    yield driver

    driver.quit()

@pytest.fixture
def driver_logueado(driver):

    driver.find_element(
        By.XPATH,
        LOGIN_USUARIO
    ).send_keys(USUARIO)

    driver.find_element(
        By.XPATH,
        LOGIN_PASSWORD
    ).send_keys(PASSWORD)

    driver.find_element(
        By.XPATH,
        LOGIN_BOTON
    ).click()

    WebDriverWait(driver, 5).until(
        EC.url_contains("dashboard")
    )

    return driver