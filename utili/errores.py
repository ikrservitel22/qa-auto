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