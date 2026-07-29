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

def test_crear_novedad(driver_logueado):
    try:

        logger.info("========== INICIO TEST_CREAR_NOVEDAD ==========")
        driver_logueado.find_element(
            By.XPATH,
            SIDEBAR_BOTON
        ).click()

        logger.info("Abriendo módulo de novedades")
        driver_logueado.find_element(
            By.XPATH,
            MENU_NOVEDADES
        ).click()

        logger.info("Abriendo ver novedades")
        driver_logueado.find_element(
            By.XPATH,
            BOTON_VER_NOVEDADES
        ).click()

        logger.info("Abriendo crear novedad")
        driver_logueado.find_element(
            By.XPATH,
            BOTON_NUEVA_NOVEDAD
        ).click()

        logger.info("Seleccionando tipo de novedad")
        driver_logueado.find_element(
            By.XPATH,
            SELECT_TIPO
        ).click()


        logger.info("Seleccionando Incapacidad")
        WebDriverWait(driver_logueado, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[contains(text(),'Incapacidad')]")
            )
        ).click()

        logger.info("Escribiendo fecha de inicio")
        driver_logueado.find_element(
            By.XPATH,
            FECHA_INICIO
        ).send_keys("07-06-2026")

        #MM-DD-YYYY
        logger.info("Escribiendo fecha de fin")
        driver_logueado.find_element(
            By.XPATH,
            FECHA_FIN
        ).send_keys("07-07-2026")

        logger.info("Escribiendo hora de inicio")
        driver_logueado.find_element(
            By.XPATH,
            HORA_INICIO
        ).send_keys("08:00-AM")

        logger.info("Escribiendo hora de fin")
        driver_logueado.find_element(
            By.XPATH,
            HORA_FIN
        ).send_keys("17:00")

        logger.info("Escribiendo descripción")
        driver_logueado.find_element(
            By.XPATH,
            INPUT_DESCRIPCION
        ).send_keys("Esta novedad fue creada para pruebas automatizadas.")

        logger.info("Guardando novedad")
        driver_logueado.find_element(
            By.XPATH,
            BOTON_GUARDAR
        ).click()

        logger.info("Esperando mensaje de éxito")
        WebDriverWait(driver_logueado, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, MENSAJE_EXITO)
            )
        )

        logger.info("Aceptando mensaje de éxito")
        driver_logueado.find_element(
            By.XPATH,
            BOTON_ACEPTAR
        ).click()

        assert driver_logueado.find_element(
            By.XPATH,
            MENSAJE_EXITO
        ).is_displayed()

        logger.info("NOVEDAD CREADA EXITOSAMENTE")

    except Exception:

        logger.exception(f"ERROR EN TEST_CREAR_NOVEDAD: {e}")
        logger.info(f"URL al fallar: {driver_logueado.current_url}")

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        ruta = f"reports/screen/novedades_{nombre}.png"

        driver_logueado.save_screenshot(ruta)

        logger.info(f"Captura guardada: {ruta}")
        logger.info("========== FIN TEST_CREAR_NOVEDAD ==========\n")

        raise

def test_btt_crear_novedad(driver_logueado):
    try:

        logger.info("========== INICIO TEST_BTT_CREAR_NOVEDAD ==========")
        driver_logueado.find_element(
            By.XPATH,
            SIDEBAR_BOTON
        ).click()

        logger.info("Abriendo módulo de novedades")
        driver_logueado.find_element(
            By.XPATH,
            MENU_NOVEDADES
        ).click()

        WebDriverWait(driver_logueado, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, BOTON_CREAR_NOVEDAD)
            )
        ).click()

        WebDriverWait(driver_logueado, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(),'Registrar novedad')]")
            )
        )

    except Exception:

        logger.exception(f"ERROR EN TEST_BTT_CREAR_NOVEDAD: {e}")
        logger.info(f"URL al fallar: {driver_logueado.current_url}")

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        ruta = f"reports/screen/novedades_{nombre}.png"

        driver_logueado.save_screenshot(ruta)

        logger.info(f"Captura guardada: {ruta}")
        logger.info("========== FIN TEST_BTT_CREAR_NOVEDAD ==========\n")

        raise
    
def test_btones_novedades(driver_logueado):
    try:

        driver_logueado.find_element(
            By.XPATH,
            SIDEBAR_BOTON
        ).click()

        # Abrir módulo de novedades
        driver_logueado.find_element(
            By.XPATH,
            MENU_NOVEDADES
        ).click()

        driver_logueado.find_element(
            By.XPATH,
            BOTON_VER_NOVEDADES
        ).click()

        # Guardar la pestaña principal
        pestana_principal = driver_logueado.current_window_handle

        # Clic en botón de previsualizar PDF
        driver_logueado.find_element(
            By.XPATH,
            '//*[@id="tabla-mias"]/tbody/tr[3]/td[9]/div/a[1]'
        ).click()

        # Esperar que aparezca la nueva pestaña
        WebDriverWait(driver_logueado, 10).until(
            lambda driver: len(driver.window_handles) > 1
        )

        # Cambiar a la nueva pestaña (PDF)
        for pestana in driver_logueado.window_handles:
            if pestana != pestana_principal:
                driver_logueado.switch_to.window(pestana)
                break

        # Aquí validas que el PDF abrió
        print("URL PDF:", driver_logueado.current_url)

        assert len(driver_logueado.window_handles) == 2


        # Cerrar pestaña del PDF
        driver_logueado.close()


        # Volver a la pestaña principal
        driver_logueado.switch_to.window(pestana_principal)

        #editar
        driver_logueado.find_element(
            By.XPATH,
            '//*[@id="tabla-mias"]/tbody/tr[3]/td[9]/div/a[2]'
        ).click()

        WebDriverWait(driver_logueado, 15).until(
            EC.url_contains("/edit")
        )

        WebDriverWait(driver_logueado, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(normalize-space(.), 'Editar novedad')]")
            )
        )

        driver_logueado.find_element(
            By.XPATH,
            '/html/body/div/div[2]/div/div/div/div/div[1]/a'
        ).click()

        #previsualizar
        driver_logueado.find_element(
            By.XPATH,
            '//*[@id="tabla-mias"]/tbody/tr[3]/td[9]/div/button'
        ).click()

        WebDriverWait(driver_logueado, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="modal-detalle"]/div/div')
            )
        )

    except Exception:

        logger.exception(f"ERROR EN TEST_Btones_Novedades: {e}")
        logger.info(f"URL al fallar: {driver_logueado.current_url}")

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        ruta = f"reports/screen/novedades_{nombre}.png"

        driver_logueado.save_screenshot(ruta)

        logger.info(f"Captura guardada: {ruta}")
        logger.info("========== FIN TEST_Btones_Novedades ==========\n")

        raise