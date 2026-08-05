from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

#importar local
from utili.config import *
from utili.locators import *
from utili.logger import logger
from utili.errores import tipificar_error

timeout = 10  # Tiempo de espera en segundos para WebDriverWait

def test_ver_horas_extra(driver_logueado):
    try:

        logger.info("========== INICIO TEST_VER_HORAS_EXTRA ==========")
        # driver_logueado.find_element(
        #     By.XPATH,
        #     SIDEBAR_BOTON
        # ).click()

        logger.info("Abriendo módulo de horas extra")
        driver_logueado.find_element(
            By.XPATH,
            '//*[@id="sidebarNav"]/div[5]/button'
        ).click()

        logger.info("Abriendo ver horas extra")
        driver_logueado.find_element(
            By.XPATH,
            '//*[@id="sidebarNav"]/div[5]/div/a[1]'
        ).click()

        logger.info("Esperando que cargue la página Horas extra")
        WebDriverWait(driver_logueado, timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(normalize-space(.), 'Horas extra')]")
            )
        )

        logger.info("presionar boton registar horas extra")
        driver_logueado.find_element(
            By.XPATH,
            '/html/body/div/div[2]/div/div/div/div/div[1]/a'
        ).click()

        logger.info("Esperando que cargue registrar Horas extra")
        WebDriverWait(driver_logueado, timeout).until(
            lambda driver: "/horas-extras/create" in driver.current_url
        )

        logger.info("HORAS EXTRA EXITOSAMENTE")        
        logger.info("========== FIN TEST_VER_HORAS_EXTRA ==========\n")

    except Exception as e:

        tipo_error = tipificar_error(e)

        logger.error("========== ERROR: TEST_VER_HORAS_EXTRA ==========")
        logger.error(f"TIPO DE ERROR: {tipo_error}")
        logger.error(f"DETALLE: {e}")
        logger.error(f"URL: {driver_logueado.current_url}")

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        ruta = f"reports/screen/horas_extra_{nombre}.png"

        driver_logueado.save_screenshot(ruta)

        logger.error(f"CAPTURA: {ruta}")

        logger.error("========== FIN TEST_VER_HORAS_EXTRA ==========\n")

        raise

def test_crear_horas_extra(driver_logueado):
    try:

        # logger.info("========== INICIO TEST_CREAR_HORAS_EXTRA ==========")
        # driver_logueado.find_element(
        #     By.XPATH,
        #     SIDEBAR_BOTON
        # ).click()

        logger.info("Abriendo módulo de horas extra")
        driver_logueado.find_element(
            By.XPATH,
            '//*[@id="sidebarNav"]/div[5]/button'
        ).click()

        logger.info("Abriendo crear horas extra")
        WebDriverWait(driver_logueado, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="sidebarNav"]/div[5]/div/a[2]')
            )
        ).click()

        logger.info("Esperando que aparezca el formulario de horas extra")
        WebDriverWait(driver_logueado, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(),'Registrar horas extra')]")
            )
        )

        logger.info("FORMULARIO DE CREAR HORAS EXTRA VISIBLE")

        logger.info("Seleccionando fecha") 
        driver_logueado.find_element(
            By.XPATH,
            '//*[@id="hex_fecha_inicio"]'
        ).send_keys("2026-06-15")

        logger.info("Seleccionando hora inicio")
        driver_logueado.find_element(
            By.XPATH,
            '//*[@id="hex_hora_inicio"]'
        ).send_keys("08:00am")

        logger.info("Seleccionando hora fin")
        driver_logueado.find_element(
            By.XPATH,
            '//*[@id="hex_fecha_fin"]'
        ).send_keys("2026-06-15")

        logger.info("Seleccionando hora fin")
        driver_logueado.find_element(
            By.XPATH,
            '//*[@id="hex_hora_fin"]'
        ).send_keys("17:00 PM")

        logger.info("introduciendo razon")
        driver_logueado.find_element(
            By.XPATH,
            '/html/body/div/div[2]/div/div/div/div/div[2]/form/div/div[5]/input'
        ).send_keys("pruebas")

        logger.info("introduciendo justificacion")
        driver_logueado.find_element(
            By.XPATH,
            '/html/body/div/div[2]/div/div/div/div/div[2]/form/div/div[6]/textarea'
        ).send_keys("pruebas")

        logger.info("presionando boton guardar")
        driver_logueado.find_element(
            By.XPATH,
            '/html/body/div/div[2]/div/div/div/div/div[2]/form/div/div[8]/button'
        ).click()

        logger.info("Esperando mensaje de éxito")
        WebDriverWait(driver_logueado, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[2]/div')
            )
        )

        logger.info("cerrando notificacion de éxito")
        driver_logueado.find_element(
            By.XPATH,
            '/html/body/div[2]/div/div[6]/button[1]'
        ).click()

        logger.info("========== FIN TEST_CREAR_HORAS_EXTRA ==========\n")

    except Exception as e:

        tipo_error = tipificar_error(e)

        logger.error("========== ERROR: TEST_CREAR_HORAS_EXTRA ==========")
        logger.error(f"TIPO DE ERROR: {tipo_error}")
        logger.error(f"DETALLE: {e}")
        logger.error(f"URL: {driver_logueado.current_url}")

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        ruta = f"reports/screen/horas_extra_{nombre}.png"

        driver_logueado.save_screenshot(ruta)

        logger.error(f"CAPTURA: {ruta}")

        logger.error("========== FIN TEST_CREAR_HORAS_EXTRA ==========\n")

        raise
    
def test_btones_horas_extra(driver_logueado):
    try:

        logger.info("========== INICIO TEST_BTONES_HORAS_EXTRA ==========")
        # driver_logueado.find_element(
        #     By.XPATH,
        #     SIDEBAR_BOTON
        # ).click()

        logger.info("Abriendo módulo de horas extra")
        driver_logueado.find_element(
            By.XPATH,
            '//*[@id="sidebarNav"]/div[5]/button'
        ).click()

        logger.info("Abriendo ver horas extra")
        driver_logueado.find_element(
            By.XPATH,
            '//*[@id="sidebarNav"]/div[5]/div/a[1]'
        ).click()

        logger.info("presinando el botón de previsualizar horas extra")
        #previsualizar
        driver_logueado.find_element(
            By.XPATH,
            '//*[@id="tabla-extras"]/tbody/tr[1]/td[8]/div/button'
        ).click()

        logger.info("Esperando que aparezca el modal de previsualización")
        WebDriverWait(driver_logueado, timeout).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[2]/div')
            )
        )

        logger.info("MODAL DE PREVISUALIZACIÓN VISIBLE")
        logger.info("========== FIN TEST_BTONES_HORAS_EXTRA ==========\n")

    except Exception as e:

        tipo_error = tipificar_error(e)

        logger.error("========== ERROR: TEST_BTONES_HORAS_EXTRA ==========")
        logger.error(f"TIPO DE ERROR: {tipo_error}")
        logger.error(f"DETALLE: {e}")
        logger.error(f"URL: {driver_logueado.current_url}")

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        ruta = f"reports/screen/horas_extra_{nombre}.png"

        driver_logueado.save_screenshot(ruta)

        logger.error(f"CAPTURA: {ruta}")

        logger.error("========== FIN TEST_BTONES_HORAS_EXTRA ==========\n")

        raise