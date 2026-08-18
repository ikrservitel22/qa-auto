from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import pytest
from utili.config import *
from utili.locators import *
from utili.logger import logger
from utili.errores import tipificar_error
from utili.waits import (
    click_when_clickable,
    wait_visible_xpath,
    wait_text_present,
    send_keys_when_visible,
    wait_clickable_xpath,
)

@pytest.mark.dependency(name="modulo_inventario_ok", depends=["login_ok"], scope="session")
def test_inventario_todos_y_nuevo_articulo(driver_logueado):
    try:
        logger.info("========== INICIO test_inventario_todos_y_nuevo_articulo ==========")

        # Abrir menú Inventario y seleccionar 'Todos'
        click_when_clickable(driver_logueado, SIDEBAR_INVENTARIO_BUTTON)
        click_when_clickable(driver_logueado, MENU_INVENTARIO_TODOS)

        # Verificar título de la página 'Inventario'
        wait_visible_xpath(driver_logueado, INVENTARIO_PAGE_TITLE)
        wait_text_present(driver_logueado, "Inventario")
        logger.info("Página Inventario visible")

        # Presionar 'Nuevo artículo'
        click_when_clickable(driver_logueado, INVENTARIO_NUEVO_ARTICULO_HEADER_BUTTON)

        # Validar que se muestra 'Nuevo Artículo'
        wait_visible_xpath(driver_logueado, INVENTARIO_NUEVO_ARTICULO_TITLE)
        wait_text_present(driver_logueado, "Nuevo Artículo")
        logger.info("Formulario Nuevo Artículo visible")

        logger.info("========== FIN test_inventario_todos_y_nuevo_articulo ==========")

    except Exception as e:
        tipo_error = tipificar_error(e)
        logger.exception(f"ERROR EN test_inventario_todos_y_nuevo_articulo: {e}")
        logger.info(f"URL al fallar: {driver_logueado.current_url}")
        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")
        driver_logueado.save_screenshot(f"reports/screen/inventario_{nombre}.png")
        raise

@pytest.mark.dependency(depends=["modulo_inventario_extra_ok"], scope="session")
def test_inventario_crear_articulo_flow(driver_logueado):
    """Flujo separado: crear un artículo nuevo desde el dashboard de inventario."""
    try:
        logger.info("--- INICIO flow crear artículo ---")

        # Abrir inventario desde dashboard (botón en el dashboard)
        click_when_clickable(driver_logueado, SIDEBAR_INVENTARIO_BUTTON)

        # Botón 'Nuevo artículo' del dashboard
        click_when_clickable(driver_logueado, MENU_INVENTARIO_NUEVO_ARTICULO)

        # Validar formulario
        wait_visible_xpath(driver_logueado, INVENTARIO_NUEVO_ARTICULO_TITLE)
        wait_text_present(driver_logueado, "Nuevo Artículo")

        # Helper para selects tipo select2 (soporta input-search o lista clickable)
        def select2_select_option(driver, container_xpath, option_text):
            click_when_clickable(driver, container_xpath)
            try:
                inp = WebDriverWait(driver, TIMEOUT).until(
                    EC.presence_of_element_located((By.XPATH, "//input[contains(@class,'select2-search__field')]"))
                )
                inp.clear()
                inp.send_keys(option_text)
                inp.send_keys(Keys.ENTER)
                return
            except Exception:
                pass
            # fallback: buscar opción en la lista y clicar
            opt_xpath = f"//li[contains(@class,'select2-results__option') and normalize-space(.)='{option_text}']"
            el_opt = WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, opt_xpath)))
            el_opt.click()

        # Seleccionar tipo (select2)
        select2_select_option(driver_logueado, INV_FORM_TYPE_SELECT, "Bodega 2026")

        # Producto
        send_keys_when_visible(driver_logueado, INV_FORM_PRODUCT_INPUT, "prueba")

        # Estado (select) — usar full XPATH proporcionado por el usuario
        select2_select_option(driver_logueado, INV_FORM_STATE_SELECT, "Disponible")

        # Empresa (select) — usar full XPATH proporcionado por el usuario
        select2_select_option(driver_logueado, INV_FORM_COMPANY_SELECT, "Servitel")

        # Enviar
        btn = wait_clickable_xpath(driver_logueado, INV_FORM_SUBMIT)
        driver_logueado.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        time.sleep(0.4)
        btn.click()

        # Esperar redirección y que el encabezado muestre Inventario
        WebDriverWait(driver_logueado, TIMEOUT).until(EC.url_contains('/inventario'))
        wait_visible_xpath(driver_logueado, INVENTARIO_PAGE_TITLE)
        wait_text_present(driver_logueado, "Inventario")

        logger.info("--- FIN flow crear artículo ---")

    except Exception as e:
        logger.exception(f"ERROR EN flow crear artículo: {e}")
        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")
        driver_logueado.save_screenshot(f"reports/screen/inventario_flow_{nombre}.png")
        raise
