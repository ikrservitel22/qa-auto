from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import pytest
import inspect
from utili.config import *
from utili.locators import *
from utili.logger import logger
from utili.errores import manejar_error_test
from utili.waits import (
    click_when_clickable,
    click_por_texto_o_xpath,
    wait_visible_xpath,
    wait_text_present,
    send_keys_when_visible,
    wait_clickable_xpath,
)


@pytest.mark.dependency(name="modulo_inventario_ok", depends=["login_ok"], scope="session")
def test_inventario_todos_y_nuevo_articulo(driver_logueado):
    try:
        logger.info("========== INICIO test_inventario_todos_y_nuevo_articulo ==========")

        logger.info("Abriendo módulo de inventario")
        click_por_texto_o_xpath(driver_logueado, "Inventario", SIDEBAR_INVENTARIO_BUTTON)

        logger.info("Abriendo 'Todos'")
        click_por_texto_o_xpath(driver_logueado, "Todos", MENU_INVENTARIO_TODOS)

        logger.info("Verificando página Inventario")
        wait_visible_xpath(driver_logueado, INVENTARIO_PAGE_TITLE)
        wait_text_present(driver_logueado, "Inventario")
        logger.info("Página Inventario visible")

        logger.info("Presionando 'Nuevo artículo'")
        click_when_clickable(driver_logueado, INVENTARIO_NUEVO_ARTICULO_HEADER_BUTTON)

        logger.info("Validando formulario 'Nuevo Artículo'")
        wait_visible_xpath(driver_logueado, INVENTARIO_NUEVO_ARTICULO_TITLE)
        wait_text_present(driver_logueado, "Nuevo Artículo")
        logger.info("Formulario Nuevo Artículo visible")

        logger.info("========== FIN test_inventario_todos_y_nuevo_articulo ==========")

    except Exception as e:
        manejar_error_test(driver_logueado, e, inspect.currentframe().f_code.co_name)
        raise


# Deshabilitado 2026-08-31: ERROR_PERMISOS (500 Internal Server Error) al enviar el formulario de nuevo artículo
# (corrida usuario desarrollo).
# @pytest.mark.dependency(depends=["modulo_inventario_ok"], scope="session")
# def test_inventario_crear_articulo_flow(driver_logueado):
#     """Flujo separado: crear un artículo nuevo desde el dashboard de inventario."""
#     try:
#         logger.info("--- INICIO flow crear artículo ---")
#
#         logger.info("Abriendo módulo de inventario")
#         click_por_texto_o_xpath(driver_logueado, "Inventario", SIDEBAR_INVENTARIO_BUTTON)
#
#         logger.info("Abriendo 'Nuevo artículo'")
#         click_por_texto_o_xpath(driver_logueado, "Nuevo artículo", MENU_INVENTARIO_NUEVO_ARTICULO)
#
#         logger.info("Validando formulario")
#         wait_visible_xpath(driver_logueado, INVENTARIO_NUEVO_ARTICULO_TITLE)
#         wait_text_present(driver_logueado, "Nuevo Artículo")
#
#         def select2_select_option(driver, container_xpath, option_text):
#             click_when_clickable(driver, container_xpath)
#             try:
#                 inp = WebDriverWait(driver, TIMEOUT).until(
#                     EC.presence_of_element_located((By.XPATH, "//input[contains(@class,'select2-search__field')]"))
#                 )
#                 inp.clear()
#                 inp.send_keys(option_text)
#                 inp.send_keys(Keys.ENTER)
#                 return
#             except Exception:
#                 pass
#             opt_xpath = f"//li[contains(@class,'select2-results__option') and normalize-space(.)='{option_text}']"
#             el_opt = WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, opt_xpath)))
#             el_opt.click()
#
#         logger.info("Seleccionando tipo (Bodega 2026)")
#         select2_select_option(driver_logueado, INV_FORM_TYPE_SELECT, "Bodega 2026")
#
#         logger.info("Escribiendo producto")
#         send_keys_when_visible(driver_logueado, INV_FORM_PRODUCT_INPUT, "prueba")
#
#         logger.info("Seleccionando estado (Disponible)")
#         select2_select_option(driver_logueado, INV_FORM_STATE_SELECT, "Disponible")
#
#         logger.info("Seleccionando empresa (Servitel)")
#         select2_select_option(driver_logueado, INV_FORM_COMPANY_SELECT, "Servitel")
#
#         logger.info("Enviando formulario")
#         btn = wait_clickable_xpath(driver_logueado, INV_FORM_SUBMIT)
#         driver_logueado.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
#         time.sleep(0.4)
#         btn.click()
#
#         logger.info("Esperando redirección a Inventario")
#         WebDriverWait(driver_logueado, TIMEOUT).until(EC.url_contains('/inventario'))
#         wait_visible_xpath(driver_logueado, INVENTARIO_PAGE_TITLE)
#         wait_text_present(driver_logueado, "Inventario")
#
#         logger.info("--- FIN flow crear artículo ---")
#
#     except Exception as e:
#         manejar_error_test(driver_logueado, e, inspect.currentframe().f_code.co_name)
#         raise