
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from utili.config import *
from utili.locators import *
from utili.logger import logger
from utili.errores import tipificar_error

def test_horarios(driver_logueado):

    try:

        logger.info("========== INICIO TEST_HORARIOS ==========")

        driver_logueado.find_element(
            By.XPATH,
            SIDEBAR_BOTON
        ).click()

        logger.info("Abriendo módulo de horarios")
        driver_logueado.find_element(
            By.XPATH,
            '//*[@id="sidebarNav"]/div[4]/button'
        ).click()

        logger.info("Abriendo ver horarios")
        driver_logueado.find_element(
            By.XPATH,
            '//*[@id="sidebarNav"]/div[4]/div/a[1]'
        ).click()

        logger.info("Esperando que se cargue la página de horarios")
        WebDriverWait(driver_logueado, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(normalize-space(.), ' Horarios')]")
            )
        )
        logger.info("HORARIOS CARGADOS CORRECTAMENTE")
        logger.info("========== FIN TEST_HORARIOS ==========\n")
    except Exception as e:

        tipo_error = tipificar_error(e)

        logger.error("========== ERROR: TEST_HORARIOS ==========")
        logger.error(f"TIPO DE ERROR: {tipo_error}")
        logger.error(f"DETALLE: {e}")
        logger.error(f"URL: {driver_logueado.current_url}")


        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        driver_logueado.save_screenshot(
            f"reports/screen/horarios_{nombre}.png"
        )

        logger.error(f"CAPTURA: reports/screen/horarios_{nombre}.png")
        logger.info("========== FIN TEST_HORARIOS ==========\n")

        raise

# def test_estado_horario(driver_logueado):

#     try:

#         logger.info("========== INICIO TEST_ESTADO_HORARIO ==========")

#         logger.info("Abriendo módulo de horarios")
#         driver_logueado.find_element(
#             By.XPATH,
#             SIDEBAR_BOTON
#         ).click()

#         logger.info("Abriendo módulo de horarios")
#         driver_logueado.find_element(
#             By.XPATH,
#             '//*[@id="sidebarNav"]/div[4]/button'
#         ).click()

#         logger.info("Abriendo estado de horario")
#         WebDriverWait(driver_logueado, 10).until(
#             EC.element_to_be_clickable(
#                 (By.XPATH, '/html/body/div/div[1]/nav/div[4]/div/a[3]')
#             )
#         ).click()

#         logger.info("Esperando que se cargue la página de estado de horario")
#         WebDriverWait(driver_logueado, 10).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, "//*[contains(normalize-space(.), 'Estado de horario — estadísticas laborales')]")
#             )
#         )

#         logger.info("Buscando botón 'Exportar detalle diario'")

#         for intento in range(10):

#             try:

#                 logger.info(f"Intento {intento + 1}")

#                 boton = driver_logueado.find_element(
#                     By.XPATH,
#                     '//*[@id="tabla-detalle_wrapper"]/div[1]/div[2]/div/button[1]'
#                 )

#                 logger.info("Botón encontrado")

#                 driver_logueado.execute_script(
#                     "arguments[0].scrollIntoView({block:'center'});",
#                     boton
#                 )

#                 time.sleep(0.5)

#                 boton.click()

#                 time.sleep(5)

#                 archivos = os.listdir("/workspace/descargas")

#                 logger.info(f"Archivos descargados: {archivos}")

#                 logger.info("Botón presionado correctamente")

#                 break

#             except NoSuchElementException:

#                 logger.info("Botón no encontrado. Bajando...")

#                 driver_logueado.execute_script("window.scrollBy(0, 500);")

#                 time.sleep(0.5)

#         else:
#             raise Exception("No se encontró el botón Exportar detalle diario.")

#         logger.info("exportar estado de horario")
#         driver_logueado.find_element(
#             By.XPATH,
#             '/html/body/div/div[2]/div/div/div/div[1]/div[3]/a'
#         ).click()

#         logger.info("ESTADO DE HORARIO EXPORTADO CORRECTAMENTE")
#         logger.info("========== FIN TEST_ESTADO_HORARIO ==========\n")

#     except Exception as e:

#         logger.exception(f"ERROR EN TEST_ESTADO_HORARIO: {e}")
#         logger.info(f"URL al fallar: {driver_logueado.current_url}")

#         nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

#         driver_logueado.save_screenshot(
#             f"reports/screen/horario_{nombre}.png"
#         )

#         logger.info(f"Captura guardada: reports/screen/estado_horario_{nombre}.png")
#         logger.info("========== FIN TEST_ESTADO_HORARIO ==========\n")

#         raise

# def test_solicitud_cambios(driver_logueado):

#     try:

#         logger.info("========== INICIO TEST_SOLICITUD_CAMBIOS ==========")

#         logger.info("Abriendo módulo de horarios")
#         driver_logueado.find_element(
#             By.XPATH,
#             SIDEBAR_BOTON
#         ).click()

#         logger.info("Abriendo módulo de horarios")
#         driver_logueado.find_element(
#             By.XPATH,
#             '//*[@id="sidebarNav"]/div[4]/button'
#         ).click()

#         logger.info("Abriendo solicitud de cambios de horario")
#         WebDriverWait(driver_logueado, 10).until(
#             EC.element_to_be_clickable(
#                 (By.XPATH, '//*[@id="sidebarNav"]/div[4]/div/a[2]')
#             )
#         ).click()

#         logger.info("Esperando que se cargue la página de solicitud de cambios de horario")
#         WebDriverWait(driver_logueado, 10).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, "//*[contains(normalize-space(.), 'Solicitudes de cambio de horario')]")
#             )
#         )

#         logger.info("SOLICITUD DE CAMBIOS CARGADA CORRECTAMENTE")
#         logger.info("========== FIN TEST_SOLICITUD_CAMBIOS ==========\n")

#     except Exception as e:

#         logger.exception(f"ERROR EN TEST_SOLICITUD_CAMBIOS: {e}")
#         logger.info(f"URL al fallar: {driver_logueado.current_url}")

#         nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

#         driver_logueado.save_screenshot(
#             f"reports/screen/horarios_{nombre}.png"
#         )

#         logger.info(f"Captura guardada: reports/screen/solicitud_cambios_{nombre}.png")
#         logger.info("========== FIN TEST_SOLICITUD_CAMBIOS ==========\n")

#         raise

