from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException,
    ElementClickInterceptedException
)


def tipificar_error(error):

    if isinstance(error, NoSuchElementException):
        return "ELEMENTO_NO_ENCONTRADO"

    elif isinstance(error, TimeoutException):
        return "TIEMPO_ESPERA"

    elif isinstance(error, ElementNotInteractableException):
        return "ELEMENTO_NO_INTERACTUABLE"

    elif isinstance(error, ElementClickInterceptedException):
        return "ELEMENTO_INTERCEPTADO"

    else:
        return "ERROR_INESPERADO"