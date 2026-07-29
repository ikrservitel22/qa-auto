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

# def test_crear_novedad(driver_logueado):
#     try:

#         driver_logueado.find_element(
#             By.XPATH,
#             SIDEBAR_BOTON
#         ).click()

#         # Abrir módulo de novedades
#         driver_logueado.find_element(
#             By.XPATH,
#             MENU_NOVEDADES
#         ).click()

#         driver_logueado.find_element(
#             By.XPATH,
#             BOTON_VER_NOVEDADES
#         ).click()

#         # Nueva novedad
#         driver_logueado.find_element(
#             By.XPATH,
#             BOTON_NUEVA_NOVEDAD
#         ).click()

#         # Seleccionar tipo
#         driver_logueado.find_element(
#             By.XPATH,
#             SELECT_TIPO
#         ).click()

#         WebDriverWait(driver_logueado, 10).until(
#             EC.element_to_be_clickable(
#                 (By.XPATH, "//li[contains(text(),'Incapacidad')]")
#             )
#         ).click()

#         driver_logueado.find_element(
#             By.XPATH,
#             FECHA_INICIO
#         ).send_keys("07-06-2026")

#         #MM-DD-YYYY
#         driver_logueado.find_element(
#             By.XPATH,
#             FECHA_FIN
#         ).send_keys("07-07-2026")

#         driver_logueado.find_element(
#             By.XPATH,
#             HORA_INICIO
#         ).send_keys("08:00-AM")

#         driver_logueado.find_element(
#             By.XPATH,
#             HORA_FIN
#         ).send_keys("17:00")

#         # Escribir descripción
#         driver_logueado.find_element(
#             By.XPATH,
#             INPUT_DESCRIPCION
#         ).send_keys("Esta novedad fue creada para pruebas automatizadas.")

#         # Guardar
#         driver_logueado.find_element(
#             By.XPATH,
#             BOTON_GUARDAR
#         ).click()

#         # Validar creación
#         WebDriverWait(driver_logueado, 20).until(
#             EC.visibility_of_element_located(
#                 (By.XPATH, MENSAJE_EXITO)
#             )
#         )

#         driver_logueado.find_element(
#             By.XPATH,
#             BOTON_ACEPTAR
#         ).click()

#         assert driver_logueado.find_element(
#             By.XPATH,
#             MENSAJE_EXITO
#         ).is_displayed()

#     except Exception:

#         nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

#         driver_logueado.save_screenshot(
#             f"reports/screen/login_{nombre}.png"
#         )

#         raise

def test_btt_crear_novedad(driver_logueado):
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

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        driver_logueado.save_screenshot(
            f"reports/screen/login_{nombre}.png"
        )

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

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        driver_logueado.save_screenshot(
            f"reports/screen/login_{nombre}.png"
        )

        raise