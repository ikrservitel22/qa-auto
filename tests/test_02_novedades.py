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
from utili.logger import logger
from utili.errores import tipificar_error
from utili.waits import click_when_clickable, wait_visible_xpath

timeout = 10  # Tiempo de espera en segundos para WebDriverWait

# def test_crear_novedad(driver_logueado):
#     try:
#
#         logger.info("========== INICIO TEST_CREAR_NOVEDAD ==========")
#         # driver_logueado.find_element(
#         #     By.XPATH,
#         #     SIDEBAR_BOTON
#         # ).click()
#
#         logger.info("Abriendo módulo de novedades")
#         driver_logueado.find_element(
#             By.XPATH,
#             MENU_NOVEDADES
#         ).click()
#
#         logger.info("Abriendo ver novedades")
#         driver_logueado.find_element(
#             By.XPATH,
#             BOTON_VER_NOVEDADES
#         ).click()
#
#         logger.info("Abriendo crear novedad")
#         driver_logueado.find_element(
#             By.XPATH,
#             BOTON_NUEVA_NOVEDAD
#         ).click()
#
#         logger.info("Seleccionando tipo de novedad")
#         driver_logueado.find_element(
#             By.XPATH,
#             SELECT_TIPO
#         ).click()


#         logger.info("Seleccionando Incapacidad")
#         # click_when_clickable(driver_logueado, "//li[contains(text(),'Incapacidad')]")

#         logger.info("Escribiendo fecha de inicio")
#         # send_keys_when_visible(driver_logueado, FECHA_INICIO, "07-06-2026")

#         #MM-DD-YYYY
#         logger.info("Escribiendo fecha de fin")
#         # send_keys_when_visible(driver_logueado, FECHA_FIN, "07-07-2026")

#         logger.info("Escribiendo hora de inicio")
#         # send_keys_when_visible(driver_logueado, HORA_INICIO, "08:00am")

#         logger.info("Escribiendo hora de fin")
#         # send_keys_when_visible(driver_logueado, HORA_FIN, "17:00pm")

#         logger.info("Escribiendo descripción")
#         # send_keys_when_visible(driver_logueado, INPUT_DESCRIPCION, "Esta novedad fue creada para pruebas automatizadas.")

#         logger.info("Guardando novedad")
#         # click_when_clickable(driver_logueado, BOTON_GUARDAR)

#         logger.info("Esperando mensaje de éxito")
#         # wait_visible_xpath(driver_logueado, MENSAJE_EXITO)

#         logger.info("Aceptando mensaje de éxito")
#         # click_when_clickable(driver_logueado, BOTON_ACEPTAR)

#         assert driver_logueado.find_element(
#             By.XPATH,
#             MENSAJE_EXITO
#         ).is_displayed()

#         logger.info("NOVEDAD CREADA EXITOSAMENTE")        
#         logger.info("========== FIN TEST_CREAR_NOVEDAD ==========\n")
#     except Exception as e:
#         tipo_error = tipificar_error(e)

#         logger.error("========== ERROR: TEST_BTT_CREAR_NOVEDAD ==========")
#         logger.error(f"TIPO DE ERROR: {tipo_error}")
#         logger.error(f"DETALLE: {e}")
#         logger.error(f"URL: {driver_logueado.current_url}")

#         nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

#         ruta = f"reports/screen/novedades_{nombre}.png"

#         driver_logueado.save_screenshot(ruta)

#         logger.info(f"Captura guardada: {ruta}")
#         logger.info("========== FIN TEST_CREAR_NOVEDAD ==========\n")

#         raise

@pytest.mark.dependency(name="modulo_novedades_ok", depends=["login_ok"], scope="session")
def test_btt_crear_novedad(driver_logueado):
    try:

        logger.info("========== INICIO TEST_BTT_CREAR_NOVEDAD ==========")
        # driver_logueado.find_element(
        #     By.XPATH,
        #     SIDEBAR_BOTON
        # ).click()

        logger.info("Abriendo módulo de novedades")
        driver_logueado.find_element(
            By.XPATH,
            MENU_NOVEDADES
        ).click()

        logger.info("Abriendo crear novedad")
        WebDriverWait(driver_logueado, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, MENU_NOVEDADES_NUEVA)
            )
        ).click()

        logger.info("Esperando que aparezca el formulario de novedad")
        WebDriverWait(driver_logueado, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(),'Registrar novedad')]")
            )
        )

        logger.info("FORMULARIO DE CREAR NOVEDAD VISIBLE")
        logger.info("========== FIN TEST_BTT_CREAR_NOVEDAD ==========\n")

    except Exception as e:

        tipo_error = tipificar_error(e)

        logger.error("========== ERROR: TEST_BTT_CREAR_NOVEDAD ==========")
        logger.error(f"TIPO DE ERROR: {tipo_error}")
        logger.error(f"DETALLE: {e}")
        logger.error(f"URL: {driver_logueado.current_url}")

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        ruta = f"reports/screen/novedades_{nombre}.png"

        driver_logueado.save_screenshot(ruta)

        logger.error(f"CAPTURA: {ruta}")
        logger.error("========== FIN TEST_BTT_CREAR_NOVEDAD ==========\n")

        raise

@pytest.mark.dependency(depends=["modulo_novedades_ok"], scope="session")
def test_btones_novedades(driver_logueado):
    try:

        logger.info("========== INICIO TEST_BTONES_NOVEDADES ==========")
        # driver_logueado.find_element(
        #     By.XPATH,
        #     SIDEBAR_BOTON
        # ).click()

        logger.info("Abriendo módulo de novedades")
        driver_logueado.find_element(
            By.XPATH,
            MENU_NOVEDADES
        ).click()

        logger.info("Abriendo ver novedades")
        WebDriverWait(driver_logueado, timeout).until(
            EC.element_to_be_clickable(
                (By.XPATH, MENU_NOVEDADES_VER)
            )
        ).click()

        logger.info("guardando la pestaña principal")
        pestana_principal = driver_logueado.current_window_handle

        logger.info("Abriendo PDF de la tercera novedad")
        click_when_clickable(driver_logueado, NOVEDADES_TABLA_MIAS_PDF_THIRD)

        logger.info("Esperando que aparezca la nueva pestaña")
        WebDriverWait(driver_logueado, 10).until(
            lambda driver: len(driver.window_handles) > 1
        )

        logger.info("Cambiando a la nueva pestaña (PDF)")
        for pestana in driver_logueado.window_handles:
            if pestana != pestana_principal:
                driver_logueado.switch_to.window(pestana)
                break

        logger.info("Esperando que el PDF cargue")
        # Aquí validas que el PDF abrió
        print("URL PDF:", driver_logueado.current_url)

        logger.info("Validando que se abrieron dos pestañas")
        assert len(driver_logueado.window_handles) == 2


        logger.info("Cerrando la pestaña del PDF")
        driver_logueado.close()

        logger.info("Volviendo a la pestaña principal")
        driver_logueado.switch_to.window(pestana_principal)

        logger.info("presionando el botón de editar de la tercera novedad")
        click_when_clickable(driver_logueado, NOVEDADES_TABLA_MIAS_EDIT_THIRD)

        logger.info("Esperando que aparezca el formulario de edición")
        WebDriverWait(driver_logueado, 15).until(
            EC.url_contains("/edit")
        )

        logger.info("Esperando que aparezca el mensaje de 'Editar novedad'")
        WebDriverWait(driver_logueado, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(normalize-space(.), 'Editar novedad')]")
            )
        )

        logger.info("Volviendo a la pestaña principal")
        click_when_clickable(driver_logueado, NOVEDADES_BACK_BUTTON)

        logger.info("presinando el botón de previsualizar de la tercera novedad")
        click_when_clickable(driver_logueado, NOVEDADES_TABLA_MIAS_PREVIEW_THIRD)

        logger.info("Esperando que aparezca el modal de previsualización")
        wait_visible_xpath(driver_logueado, NOVEDADES_MODAL_DETALLE)

        logger.info("MODAL DE PREVISUALIZACIÓN VISIBLE")
        logger.info("========== FIN TEST_BTONES_NOVEDADES ==========\n")

    except Exception as e:

        tipo_error = tipificar_error(e)

        logger.error("========== ERROR: TEST_BTONES_NOVEDADES ==========")
        logger.error(f"TIPO DE ERROR: {tipo_error}")
        logger.error(f"DETALLE: {e}")
        logger.error(f"URL: {driver_logueado.current_url}")

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        ruta = f"reports/screen/novedades_{nombre}.png"

        driver_logueado.save_screenshot(ruta)

        logger.error(f"CAPTURA: {ruta}")
        logger.error("========== FIN TEST_Btones_Novedades ==========\n")

        raise