from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    InvalidSelectorException,
    NoSuchWindowException,
    UnexpectedAlertPresentException,
    WebDriverException,
)
from utili.logger import logger

REINTENTABLES = {
    "TIEMPO_ESPERA",
    "ELEMENTO_DESACTUALIZADO",
    "ELEMENTO_INTERCEPTADO",
}


def tipificar_error(error):

    if isinstance(error, NoSuchElementException):
        return "ELEMENTO_NO_ENCONTRADO"

    elif isinstance(error, TimeoutException):
        return "TIEMPO_ESPERA"

    elif isinstance(error, StaleElementReferenceException):
        return "ELEMENTO_DESACTUALIZADO"

    elif isinstance(error, ElementNotInteractableException):
        return "ELEMENTO_NO_INTERACTUABLE"

    elif isinstance(error, ElementClickInterceptedException):
        return "ELEMENTO_INTERCEPTADO"

    elif isinstance(error, InvalidSelectorException):
        return "SELECTOR_INVALIDO"

    elif isinstance(error, NoSuchWindowException):
        return "VENTANA_NO_ENCONTRADA"

    elif isinstance(error, UnexpectedAlertPresentException):
        return "ALERT_INESPERADO"

    elif isinstance(error, WebDriverException):
        return "ERROR_DRIVER"

    else:
        return "ERROR_INESPERADO"


def es_reintentable(tipo_error):
    return tipo_error in REINTENTABLES

def guardar_texto_pagina_error(driver, ruta_txt):
    """
    Extrae todo el texto visible de la página actual y lo guarda en un .txt.
    Útil para páginas de error tipo Laravel/PHP donde el texto es más
    útil que una captura de pantalla (se puede copiar, buscar, leer fácil).
    """
    try:
        texto = driver.find_element("tag name", "body").text
        with open(ruta_txt, "w", encoding="utf-8") as f:
            f.write(f"URL: {driver.current_url}\n")
            f.write("=" * 60 + "\n\n")
            f.write(texto)
        logger.info(f"Texto de página de error guardado en: {ruta_txt}")
        return True
    except Exception as e:
        logger.error(f"No se pudo guardar el texto de la página: {e}")
        return False

def es_pagina_error_servidor(driver):
    """
    Detecta si la página actual es una pantalla de error del servidor
    (Laravel, PHP, 500, etc.) en vez de la app normal.
    """
    indicadores = [
        "Internal Server Error",
        "BindingResolutionException",
        "Exception trace",
        "Fatal error",
        "Whoops",
        "Illuminate\\",
    ]
    try:
        texto_pagina = driver.find_element("tag name", "body").text
        return any(ind in texto_pagina for ind in indicadores)
    except Exception:
        return False