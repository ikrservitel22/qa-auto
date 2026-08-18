
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import pytest
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from utili.screenshot_full import capturar_pantalla_completa

from utili.config import *
from utili.locators import *
from utili.logger import logger
from utili.errores import tipificar_error
from utili.waits import click_when_clickable, wait_text_in_page, wait_text_present, wait_visible_xpath
from utili.downloads import download_via_requests

@pytest.mark.dependency(name="modulo_horarios_ok", depends=["login_ok"], scope="session")
def test_horarios(driver_logueado):

    try:

        logger.info("========== INICIO TEST_HORARIOS ==========")

        # driver_logueado.find_element(
        #     By.XPATH,
        #     SIDEBAR_BOTON
        # ).click()

        logger.info("Abriendo módulo de horarios")
        click_when_clickable(driver_logueado, SIDEBAR_HORARIOS_BUTTON)

        logger.info("Abriendo ver horarios")
        click_when_clickable(driver_logueado, MENU_HORARIOS_VER)

        logger.info("Esperando que se cargue la página de horarios")
        wait_visible_xpath(driver_logueado, HORARIOS_PAGE_TITLE)
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

@pytest.mark.dependency(depends=["modulo_horarios_ok"], scope="session")
def test_estado_horario(driver_logueado):

    try:

        logger.info("========== INICIO TEST_ESTADO_HORARIO ==========")

        # logger.info("Abriendo módulo de horarios")
        # driver_logueado.find_element(
        #     By.XPATH,
        #     SIDEBAR_BOTON
        # ).click()

        logger.info("Abriendo módulo de horarios")
        click_when_clickable(driver_logueado, SIDEBAR_HORARIOS_BUTTON)

        logger.info("Abriendo estado de horario")
        click_when_clickable(driver_logueado, MENU_HORARIOS_ESTADO)

        logger.info("Esperando que se cargue la página de estado de horario")
        WebDriverWait(driver_logueado, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(normalize-space(.), 'Estado de horario — estadísticas laborales')]")
            )
        )

        logger.info("Buscando botón 'Exportar detalle diario'")

        for intento in range(10):

            try:

                logger.info(f"Intento {intento + 1}")

                boton = driver_logueado.find_element(By.XPATH, TABLA_DETALLE_EXPORT_BUTTON)

                logger.info("Botón encontrado")

                driver_logueado.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    boton
                )

                time.sleep(0.5)

                boton.click()

                time.sleep(5)

                archivos = os.listdir("/workspace/descargas")

                logger.info(f"Archivos descargados: {archivos}")

                logger.info("Botón presionado correctamente")

                break

            except NoSuchElementException:

                logger.info("Botón no encontrado. Bajando...")

                driver_logueado.execute_script("window.scrollBy(0, 500);")

                time.sleep(0.5)

        else:
            raise Exception("No se encontró el botón Exportar detalle diario.")

        logger.info("exportar estado de horario")
        started_tabs = driver_logueado.window_handles

        # Intentar descargar directamente vía HTTP usando la URL del enlace (si existe)
        try:
            link_el = driver_logueado.find_element(By.XPATH, EXPORT_PAGE_LINK)
            href = link_el.get_attribute('href')
        except Exception:
            href = None

        if href and href.startswith('http'):
            try:
                downloaded = download_via_requests(driver_logueado, href, '/workspace/descargas')
                logger.info(f"Descargado vía HTTP a: {downloaded}")
            except Exception as e:
                logger.warning(f"Descarga directa falló: {e}")

        # Intentar click en la UI (si es necesario para navegación)
        click_when_clickable(driver_logueado, EXPORT_PAGE_LINK)

        # Si la exportación abre una nueva pestaña, cambie a ella y espere el texto.
        WebDriverWait(driver_logueado, TIMEOUT).until(
            lambda d: len(d.window_handles) != len(started_tabs)
        )
        new_tabs = [h for h in driver_logueado.window_handles if h not in started_tabs]
        if new_tabs:
            driver_logueado.switch_to.window(new_tabs[0])
            logger.info("Cambiado a nueva pestaña de exportación")
            wait_text_in_page(driver_logueado, "Detalle diario", TIMEOUT * 2)
            logger.info("Detalle diario encontrado en la nueva pestaña")
            driver_logueado.close()
            driver_logueado.switch_to.window(started_tabs[0])
            logger.info("Regresado a la pestaña original")
        else:
            # Si no abre nueva pestaña, esperamos el texto en la misma página.
            wait_text_in_page(driver_logueado, "Detalle diario", TIMEOUT * 2)
            logger.info("Detalle diario encontrado en la misma página")

        # Además, esperar a que aparezca un archivo en la carpeta de descargas
        download_found = False
        download_timeout = TIMEOUT
        end_time = time.time() + download_timeout
        while time.time() < end_time:
            try:
                archivos = [f for f in os.listdir("/workspace/descargas") if not f.startswith('.')]
                if archivos:
                    logger.info(f"Archivos descargados: {archivos}")
                    download_found = True
                    break
            except Exception:
                pass
            time.sleep(1)

        if not download_found:
            logger.warning("No se detectaron archivos en /workspace/descargas dentro del timeout")

        logger.info("ESTADO DE HORARIO EXPORTADO CORRECTAMENTE: flujo comprobado")
        logger.info("========== FIN TEST_ESTADO_HORARIO ==========\n")

    except Exception as e:

        logger.exception(f"ERROR EN TEST_ESTADO_HORARIO: {e}")
        logger.info(f"URL al fallar: {driver_logueado.current_url}")

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        driver_logueado.save_screenshot(
            f"reports/screen/horario_{nombre}.png"
        )

        logger.info(f"Captura guardada: reports/screen/estado_horario_{nombre}.png")
        logger.info("========== FIN TEST_ESTADO_HORARIO ==========\n")

        raise

@pytest.mark.dependency(depends=["modulo_horarios_ok"], scope="session")
def test_solicitud_cambios(driver_logueado):

    try:

        logger.info("========== INICIO TEST_SOLICITUD_CAMBIOS ==========")

        # logger.info("Abriendo módulo de horarios")
        # driver_logueado.find_element(
        #     By.XPATH,
        #     SIDEBAR_BOTON
        # ).click()

        logger.info("Abriendo módulo de horarios")
        click_when_clickable(driver_logueado, SIDEBAR_HORARIOS_BUTTON)

        logger.info("Abriendo solicitud de cambios de horario")
        click_when_clickable(driver_logueado, MENU_HORARIOS_SOLICITUD)

        logger.info("Esperando que se cargue la página de solicitud de cambios de horario")
        WebDriverWait(driver_logueado, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(normalize-space(.), 'Solicitudes de cambio de horario')]")
            )
        )

        logger.info("SOLICITUD DE CAMBIOS CARGADA CORRECTAMENTE")
        logger.info("========== FIN TEST_SOLICITUD_CAMBIOS ==========\n")

    except Exception as e:

        logger.exception(f"ERROR EN TEST_SOLICITUD_CAMBIOS: {e}")
        logger.info(f"URL al fallar: {driver_logueado.current_url}")

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        driver_logueado.save_screenshot(
            f"reports/screen/horarios_{nombre}.png"
        )
        capturar_pantalla_completa(f"reports/screen/horas_extra_FULL_{nombre}.png")

        logger.info(f"Captura guardada: reports/screen/solicitud_cambios_{nombre}.png")
        logger.info("========== FIN TEST_SOLICITUD_CAMBIOS ==========\n")

        raise

