import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime
import pytest
from utili.config import *
from utili.locators import *

@pytest.fixture
def driver():

    options = Options()

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