from datetime import datetime
from utili.config import *
from utili.logger import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utili.locators import (
    MENU_PROYECTOS,
    PROYECTOS_ACCION_VER,
    PROYECTOS_DETALLE_TITLE,
    PROYECTOS_ACCION_EDITAR,
    PROYECTOS_EDITAR_VOLVER,
    PROYECTOS_DETALLE_VOLVER_LISTADO,
    PROYECTOS_NUEVO_BUTTON,
    PROYECTOS_PAGE_TITLE,
    PROYECTOS_EDITAR_TITLE,
)
import pytest
import inspect
from utili.errores import manejar_error_test
from utili.waits import click_when_clickable, wait_text_in_element

@pytest.mark.dependency(name="modulo_proyectos_ok", depends=["login_ok"], scope="session")
def test_proyectos_flujo(driver_logueado):

    try:
        logger.info("========== INICIO TEST_PROYECTOS_FLUJO ==========")

        logger.info("Paso 1: Click en menú lateral - Proyectos")
        click_when_clickable(driver_logueado, MENU_PROYECTOS)
        wait_text_in_element(driver_logueado, PROYECTOS_PAGE_TITLE, "Proyectos de desarrollo")

        logger.info("Paso 2: Click en 'Ver' de la primera fila")
        click_when_clickable(driver_logueado, PROYECTOS_ACCION_VER)

        # El nombre del proyecto es variable, lo capturamos dinámicamente
        elemento_detalle = WebDriverWait(driver_logueado, TIMEOUT).until(
            EC.visibility_of_element_located((By.XPATH, PROYECTOS_DETALLE_TITLE))
        )
        nombre_proyecto = elemento_detalle.text.strip()
        logger.info(f"Proyecto detectado: '{nombre_proyecto}'")

        logger.info("Paso 3: Click en 'Editar'")
        click_when_clickable(driver_logueado, PROYECTOS_ACCION_EDITAR)
        wait_text_in_element(driver_logueado, PROYECTOS_EDITAR_TITLE, "Editar proyecto")

        logger.info("Paso 4: Click en 'Volver' del formulario")
        click_when_clickable(driver_logueado, PROYECTOS_EDITAR_VOLVER)
        wait_text_in_element(driver_logueado, PROYECTOS_DETALLE_TITLE, nombre_proyecto)

        logger.info("Paso 5: Click para volver al listado de proyectos")
        click_when_clickable(driver_logueado, PROYECTOS_DETALLE_VOLVER_LISTADO)
        wait_text_in_element(driver_logueado, PROYECTOS_PAGE_TITLE, "Proyectos de desarrollo")

        logger.info("Paso 6: Click en 'Nuevo proyecto'")
        click_when_clickable(driver_logueado, PROYECTOS_NUEVO_BUTTON)
        wait_text_in_element(driver_logueado, PROYECTOS_EDITAR_TITLE, "Nuevo proyecto")

        logger.info("TEST_PROYECTOS_FLUJO COMPLETADO")
        logger.info("========== FIN TEST_PROYECTOS_FLUJO ==========")

    except Exception as e:
        manejar_error_test(driver_logueado, e, inspect.currentframe().f_code.co_name)
        raise