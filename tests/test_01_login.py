from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utili.config import *
from utili.locators import *


def log(mensaje):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {mensaje}")


def test_login(driver):

    try:

        log("Abriendo página de login")

        print(f"URL: {URL}")
        print(f"USUARIO: {USUARIO}")

        log("Escribiendo usuario")
        driver.find_element(
            By.XPATH,
            LOGIN_USUARIO
        ).send_keys(USUARIO)

        log("Escribiendo contraseña")
        driver.find_element(
            By.XPATH,
            LOGIN_PASSWORD
        ).send_keys(PASSWORD)

        log("Pulsando botón Ingresar")
        driver.find_element(
            By.XPATH,
            LOGIN_BOTON
        ).click()

        log("Esperando Dashboard")
        WebDriverWait(driver, 5).until(
            EC.url_contains("dashboard")
        )

        log(f"URL actual: {driver.current_url}")

        assert "dashboard" in driver.current_url

        log("LOGIN EXITOSO")

    except Exception as e:

        log(f"ERROR: {e}")
        log(f"URL al fallar: {driver.current_url}")

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        driver.save_screenshot(
            f"reports/screen/login_{nombre}.png"
        )

        log(f"Captura guardada: reports/screen/login_{nombre}.png")

        raise


def test_logout(driver_logueado):

    try:

        log("Abriendo menú lateral")

        driver_logueado.find_element(
            By.XPATH,
            SIDEBAR_BOTON
        ).click()

        log("Pulsando Cerrar sesión")

        driver_logueado.find_element(
            By.XPATH,
            LOGOUT_BOTON
        ).click()

        log("Esperando regresar al Login")

        WebDriverWait(driver_logueado, 5).until(
            lambda d: d.current_url == URL
        )

        log(f"URL actual: {driver_logueado.current_url}")

        assert driver_logueado.current_url == URL

        log("LOGOUT EXITOSO")

    except Exception as e:

        log(f"ERROR: {e}")
        log(f"URL al fallar: {driver_logueado.current_url}")

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        driver_logueado.save_screenshot(
            f"reports/screen/login_{nombre}.png"
        )

        log(f"Captura guardada: reports/screen/login_{nombre}.png")

        raise