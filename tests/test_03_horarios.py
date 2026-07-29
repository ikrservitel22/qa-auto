
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

def test_horarios(driver_logueado):

    try:

        driver_logueado.find_element(
            By.XPATH,
            SIDEBAR_BOTON
        ).click()

        # Abrir módulo de horarios
        driver_logueado.find_element(
            By.XPATH,
            '//*[@id="sidebarNav"]/div[4]/button'
        ).click()

        driver_logueado.find_element(
            By.XPATH,
            '//*[@id="sidebarNav"]/div[4]/div/a[1]'
        ).click()

        WebDriverWait(driver_logueado, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(normalize-space(.), ' Horarios')]")
            )
        )

    except Exception:

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        driver_logueado.save_screenshot(
            f"reports/screen/login_{nombre}.png"
        )

        raise

def test_estado_horario(driver_logueado):

    try:

        driver_logueado.find_element(
            By.XPATH,
            SIDEBAR_BOTON
        ).click()

        # Abrir módulo de horarios
        driver_logueado.find_element(
            By.XPATH,
            '//*[@id="sidebarNav"]/div[4]/button'
        ).click()

        WebDriverWait(driver_logueado, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div/div[1]/nav/div[4]/div/a[3]')
            )
        ).click()

        WebDriverWait(driver_logueado, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(normalize-space(.), 'Estado de horario — estadísticas laborales')]")
            )
        )

        driver_logueado.find_element(
            By.XPATH,
            '/html/body/div/div[2]/div/div/div/div[1]/div[3]/a'
        ).click()

        driver_logueado.find_element(
            By.XPATH,
            '//*[@id="tabla-detalle_wrapper"]/div[1]/div[2]/div/button[1]/span'
        ).click()

    except Exception:

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        driver_logueado.save_screenshot(
            f"reports/screen/login_{nombre}.png"
        )

        raise

def test_solicitud_cambios(driver_logueado):

    try:

        driver_logueado.find_element(
            By.XPATH,
            SIDEBAR_BOTON
        ).click()

        # Abrir módulo de horarios
        driver_logueado.find_element(
            By.XPATH,
            '//*[@id="sidebarNav"]/div[4]/button'
        ).click()

        WebDriverWait(driver_logueado, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="sidebarNav"]/div[4]/div/a[2]')
            )
        ).click()

        WebDriverWait(driver_logueado, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(normalize-space(.), 'Solicitudes de cambio de horario')]")
            )
        )

    except Exception:

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        driver_logueado.save_screenshot(
            f"reports/screen/login_{nombre}.png"
        )

        raise

