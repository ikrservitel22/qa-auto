import time

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utili.config import TIMEOUT
from utili.logger import logger
from utili.errores import es_pagina_error_servidor, ErrorPaginaServidorDetectado

# Después de este tiempo sin éxito, cada espera empieza a revisar si la página
# es en realidad una pantalla de error del servidor, para cortar la espera de
# inmediato en vez de agotar el timeout completo esperando un elemento que
# nunca va a aparecer porque la página no es la que se esperaba. Se deja un
# margen (en vez de revisar desde el primer poll) para no penalizar con
# comandos extra al camino feliz, donde el elemento normalmente aparece rápido.
GRACIA_DETECCION_ERROR_S = 2


def _esperar_con_deteccion_de_error(driver, condicion, timeout):
    inicio = time.monotonic()

    def _condicion_vigilada(d):
        if time.monotonic() - inicio >= GRACIA_DETECCION_ERROR_S:
            es_error, tipo = es_pagina_error_servidor(d)
            if es_error:
                raise ErrorPaginaServidorDetectado(
                    f"Se esperaba un elemento pero la página muestra un error de servidor ({tipo})"
                )
        return condicion(d)

    return WebDriverWait(driver, timeout).until(_condicion_vigilada)


def wait_visible_xpath(driver, xpath, timeout=None):
    t = timeout or TIMEOUT
    return _esperar_con_deteccion_de_error(
        driver, EC.visibility_of_element_located((By.XPATH, xpath)), t
    )


def wait_clickable_xpath(driver, xpath, timeout=None):
    t = timeout or TIMEOUT
    return _esperar_con_deteccion_de_error(
        driver, EC.element_to_be_clickable((By.XPATH, xpath)), t
    )


def click_when_clickable(driver, xpath, timeout=None):
    el = wait_clickable_xpath(driver, xpath, timeout)
    try:
        el.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        time.sleep(0.5)
        try:
            el.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", el)
    return el


def click_sidebar_menu_item(driver, texto_padre, xpath_padre_respaldo, texto_hijo, xpath_hijo_respaldo, timeout=None):
    """
    Abre un grupo del menú lateral (solo si no está ya abierto) y hace clic en el ítem hijo.
    Busca ambos por texto primero, usando el XPath de respaldo si no los encuentra.
    Evita cerrar el submenú si ya estaba abierto.
    """
    t = timeout or TIMEOUT

    # 1. Si el hijo ya es visible (submenú ya abierto), clic directo, sin tocar el padre
    try:
        texto_hijo_lower = texto_hijo.lower().strip()
        xpath_hijo_texto = (
            f"//*[self::button or self::a]"
            f"[contains(translate(normalize-space(.), "
            f"'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚ', "
            f"'abcdefghijklmnopqrstuvwxyzáéíóú'), '{texto_hijo_lower}')]"
        )
        hijo = driver.find_element(By.XPATH, xpath_hijo_texto)
        if hijo.is_displayed():
            logger.info(f"Submenú ya abierto, click directo en '{texto_hijo}'")
            hijo.click()
            return
    except Exception:
        pass

    # 2. No estaba visible: abrir el padre
    click_por_texto_o_xpath(driver, texto_padre, xpath_padre_respaldo, timeout=t)

    # 3. Ahora sí, clic en el hijo
    click_por_texto_o_xpath(driver, texto_hijo, xpath_hijo_respaldo, timeout=t)


def wait_for_url(driver, url, timeout=None):
    t = timeout or TIMEOUT
    return _esperar_con_deteccion_de_error(driver, EC.url_to_be(url), t)


def send_keys_when_visible(driver, xpath, text, timeout=None):
    el = wait_visible_xpath(driver, xpath, timeout)
    try:
        el.clear()
    except Exception:
        pass
    el.send_keys(text)
    return el


def wait_text_in_element(driver, xpath, text, timeout=None):
    t = timeout or TIMEOUT
    return _esperar_con_deteccion_de_error(
        driver, EC.text_to_be_present_in_element((By.XPATH, xpath), text), t
    )


def wait_text_present(driver, text, timeout=None):
    t = timeout or TIMEOUT
    xpath = f"//*[contains(normalize-space(.), '{text}') ]"
    # Permite buscar cualquier elemento cuyo texto contenga la cadena dada
    return _esperar_con_deteccion_de_error(
        driver, EC.visibility_of_element_located((By.XPATH, xpath)), t
    )


def wait_text_in_page(driver, text, timeout=None):
    t = timeout or TIMEOUT
    return _esperar_con_deteccion_de_error(driver, lambda d: text in d.page_source, t)

def click_por_texto_o_xpath(driver, texto, xpath_respaldo, timeout=None):
    """
    Busca un <button> o <a> cuyo texto visible contenga el texto indicado
    (sin importar mayúsculas/minúsculas). Si no lo encuentra, usa el XPath de respaldo.
    """
    t = timeout or TIMEOUT
    texto_lower = texto.lower().strip()

    xpath_texto = (
        f"//*[self::button or self::a]"
        f"[contains(translate(normalize-space(.), "
        f"'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚ', "
        f"'abcdefghijklmnopqrstuvwxyzáéíóú'), '{texto_lower}')]"
    )

    try:
        elemento = _esperar_con_deteccion_de_error(
            driver, EC.element_to_be_clickable((By.XPATH, xpath_texto)), t
        )
        logger.info(f"Elemento encontrado por texto: '{texto}'")
        elemento.click()
        return
    except Exception:
        logger.warning(f"No se encontró por texto '{texto}', usando XPath de respaldo")

    elemento = _esperar_con_deteccion_de_error(
        driver, EC.element_to_be_clickable((By.XPATH, xpath_respaldo)), t
    )
    elemento.click()