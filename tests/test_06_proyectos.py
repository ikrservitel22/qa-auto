from datetime import datetime

from utili.config import *
from utili.logger import logger
from utili.locators import (
    MENU_PROYECTOS,
    PROYECTOS_ACCION_VER,
    PROYECTOS_ACCION_EDITAR,
    PROYECTOS_EDITAR_VOLVER,
    PROYECTOS_NUEVO_BUTTON,
    PROYECTOS_PAGE_TITLE,
    PROYECTOS_EDITAR_TITLE,
)
from utili.errores import tipificar_error
from utili.waits import (
    click_when_clickable,
    wait_text_in_element,
    wait_text_present,
)


def test_proyectos_flujo(driver_logueado):

    try:

        logger.info("========== INICIO TEST_PROYECTOS_FLUJO ==========")

        # Abrir item del sidebar
        logger.info("Click en menú lateral - segunda opción")
        click_when_clickable(driver_logueado, MENU_PROYECTOS)

        # Pulsar primer enlace de la fila (VER / acciones)
        logger.info("Click en acción 1 de la primera fila")
        click_when_clickable(driver_logueado, PROYECTOS_ACCION_VER)

        # Esperar a que salga el texto VER en la página
        logger.info("Esperando texto 'VER'")
        wait_text_present(driver_logueado, "VER")

        # Click en devolver (dejado comentado porque la función aún no está)
        # logger.info("Click en devolver")
        # click_when_clickable(driver_logueado, '/html/body/div/.../a_devolver')

        # Esperar que aparezca "Proyectos de desarrollo"
        logger.info("Esperando 'Proyectos de desarrollo'")
        wait_text_in_element(driver_logueado, '/html/body/div/div[2]/div/div/div/div[1]/h5', 'Proyectos de desarrollo')

        # Click en la segunda acción (Editar)
        logger.info("Click en acción 2 (Editar) de la primera fila")
        click_when_clickable(driver_logueado, PROYECTOS_ACCION_EDITAR)

        # Esperar que diga "Editar proyecto"
        logger.info("Esperando 'Editar proyecto'")
        wait_text_in_element(driver_logueado, PROYECTOS_EDITAR_TITLE, 'Editar proyecto')

        # Click en el enlace dentro del formulario (div[7]/a)
        logger.info("Click en link del formulario (div[7]/a)")
        click_when_clickable(driver_logueado, PROYECTOS_EDITAR_VOLVER)

        # Esperar regresar a "Proyectos de desarrollo"
        logger.info("Esperando regresar a 'Proyectos de desarrollo'")
        wait_text_in_element(driver_logueado, PROYECTOS_PAGE_TITLE, 'Proyectos de desarrollo')

        # Click en crear nuevo proyecto
        logger.info("Click en 'Nuevo proyecto' (abrir formulario)")
        click_when_clickable(driver_logueado, PROYECTOS_NUEVO_BUTTON)

        # Esperar que diga "Nuevo proyecto"
        logger.info("Esperando 'Nuevo proyecto'")
        wait_text_in_element(driver_logueado, PROYECTOS_EDITAR_TITLE, 'Nuevo proyecto')

        logger.info("TEST_PROYECTOS_FLUJO COMPLETADO")
        logger.info("========== FIN TEST_PROYECTOS_FLUJO ==========")

    except Exception as e:

        tipo_error = tipificar_error(e)

        logger.error("========== ERROR: TEST_PROYECTOS_FLUJO ==========")
        logger.error(f"TIPO DE ERROR: {tipo_error}")
        logger.error(f"DETALLE: {e}")
        logger.error(f"URL: {driver_logueado.current_url}")

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")

        ruta = f"reports/screen/proyectos_{nombre}.png"

        driver_logueado.save_screenshot(ruta)

        logger.error(f"CAPTURA: {ruta}")
        logger.error("========== FIN TEST_PROYECTOS_FLUJO ==========")

        raise
