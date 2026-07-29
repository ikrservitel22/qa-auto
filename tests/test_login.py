from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utili.config import *
from utili.locators import *

def test_login(driver):

    try:

        print(f"URL: {URL}")
        print(f"USUARIO: {USUARIO}")

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

        assert "dashboard" in driver.current_url

    except Exception:

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        driver.save_screenshot(
            f"reports/screen/login_{nombre}.png"
        )

        raise

def test_logout(driver_logueado):

    try:

        driver_logueado.find_element(
            By.XPATH,
            SIDEBAR_BOTON
        ).click()

        driver_logueado.find_element(
            By.XPATH,
            LOGOUT_BOTON
        ).click()

        WebDriverWait(driver_logueado, 5).until(
            lambda d: d.current_url == URL
        )

        assert driver_logueado.current_url == URL

    except Exception:

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        driver_logueado.save_screenshot(
            f"reports/screen/login_{nombre}.png"
        )

        raise


