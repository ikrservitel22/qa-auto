"""
Tests unitarios para utili/errores.py.

A diferencia de los tests en tests/test_*.py, estos NO abren un navegador
real ni se conectan al Selenium Grid — corren en milisegundos usando un
"driver falso" (DriverFalso, más abajo) que imita solo los métodos que
utili/errores.py realmente usa.

Por qué existen: manejar_error_test() y tipificar_error() son llamados
desde los 8 archivos de test (son el manejo de errores COMPARTIDO de todo
el proyecto). Si tienen un bug, se entera uno solo cuando un test real
falla en producción — el peor momento, porque es justo la red de
seguridad que se supone que debe funcionar ahí. Estos tests atrapan esos
bugs antes, en segundos y sin depender de nada externo.

Correr solo estos tests (rápido, no toca el navegador):
    python -m pytest -s tests/test_utili_errores.py -v
"""
import pytest
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    InvalidSelectorException,
    NoSuchWindowException,
    UnexpectedAlertPresentException,
    SessionNotCreatedException,
    JavascriptException,
    WebDriverException,
)

from utili.errores import (
    tipificar_error,
    es_reintentable,
    es_pagina_error_servidor,
    manejar_error_test,
    REINTENTABLES,
)


# ---------------------------------------------------------------------------
# "Driver falso": un objeto plano de Python que imita los métodos de un
# WebDriver de Selenium que utili/errores.py realmente usa. No abre ningún
# navegador — solo devuelve lo que le configuremos en cada test.
# ---------------------------------------------------------------------------

class ElementoFalso:
    """Simula el resultado de driver.find_element(...)."""
    def __init__(self, texto):
        self.text = texto


class AlertaFalsa:
    """Simula driver.switch_to.alert."""
    def __init__(self, texto):
        self.text = texto
        self.aceptada = False

    def accept(self):
        self.aceptada = True


class SwitchToFalso:
    def __init__(self, alerta=None):
        self._alerta = alerta

    @property
    def alert(self):
        if self._alerta is None:
            # Selenium real lanza esto cuando NO hay alerta abierta
            raise NoAlertPresentExceptionLocal("no hay alerta")
        return self._alerta


class NoAlertPresentExceptionLocal(Exception):
    """Sustituto simple: no importa la excepción exacta, solo que algo
    se lance cuando no hay alerta — es lo que hace Selenium real."""
    pass


class DriverFalso:
    """
    Driver de mentira, configurable por test:
      - texto_pagina: lo que "ve" el body de la página
      - titulo: el <title> de la página
      - url: driver.current_url
      - alerta_texto: si no es None, simula una alerta nativa abierta
      - fallar_todo: si es True, CUALQUIER método lanza una excepción
        (para probar que manejar_error_test() nunca truena pase lo que pase)
    """
    def __init__(self, texto_pagina="", titulo="", url="http://x", alerta_texto=None, fallar_todo=False):
        self.texto_pagina = texto_pagina
        self.title = titulo
        self.current_url = url
        self.fallar_todo = fallar_todo
        self._alerta = AlertaFalsa(alerta_texto) if alerta_texto is not None else None
        self.switch_to = SwitchToFalso(self._alerta)
        self.capturas_tomadas = []

    def find_element(self, by, tag):
        if self.fallar_todo:
            raise WebDriverException("el driver falso está configurado para fallar todo")
        return ElementoFalso(self.texto_pagina)

    def save_screenshot(self, ruta):
        if self.fallar_todo:
            raise WebDriverException("el driver falso está configurado para fallar todo")
        self.capturas_tomadas.append(ruta)
        return True


# ---------------------------------------------------------------------------
# tipificar_error(): cada excepción de Selenium debe mapear a su categoría
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("excepcion,categoria_esperada", [
    (NoSuchElementException("x"), "ELEMENTO_NO_ENCONTRADO"),
    (TimeoutException("x"), "TIEMPO_ESPERA"),
    (StaleElementReferenceException("x"), "ELEMENTO_DESACTUALIZADO"),
    (ElementNotInteractableException("x"), "ELEMENTO_NO_INTERACTUABLE"),
    (ElementClickInterceptedException("x"), "ELEMENTO_INTERCEPTADO"),
    (InvalidSelectorException("x"), "SELECTOR_INVALIDO"),
    (NoSuchWindowException("x"), "VENTANA_NO_ENCONTRADA"),
    (UnexpectedAlertPresentException(), "ALERT_INESPERADO"),
    (SessionNotCreatedException("x"), "NAVEGADOR_DESCONECTADO"),
    (JavascriptException("x"), "SCRIPT_JS_FALLIDO"),
    (WebDriverException("x"), "ERROR_DRIVER"),
    (AssertionError("x"), "FALLO_ASERCION"),
    (KeyError("x"), "ERROR_EN_SCRIPT_TEST"),
    (AttributeError("x"), "ERROR_EN_SCRIPT_TEST"),
    (RuntimeError("x"), "ERROR_INESPERADO"),
])
def test_tipificar_error_mapea_cada_categoria(excepcion, categoria_esperada):
    assert tipificar_error(excepcion) == categoria_esperada


# ---------------------------------------------------------------------------
# es_reintentable(): solo los tipos declarados en REINTENTABLES deben serlo
# ---------------------------------------------------------------------------

def test_es_reintentable_reconoce_los_tipos_declarados():
    for tipo in REINTENTABLES:
        assert es_reintentable(tipo) is True


def test_es_reintentable_rechaza_lo_no_declarado():
    assert es_reintentable("ERROR_INESPERADO") is False
    assert es_reintentable("ALGO_QUE_NO_EXISTE") is False


# ---------------------------------------------------------------------------
# es_pagina_error_servidor(): detección por contenido real de la página
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("texto_pagina,titulo,categoria_esperada", [
    ("Bienvenido al inventario\nCrear artículo", "Inventario - Intranet", None),
    ("Internal Server Error\nBadMethodCallException", "", "ERROR_SERVIDOR_APP"),
    ("403 | Forbidden", "", "ERROR_HTTP"),
    ("SQLSTATE[HY000] Access denied for user 'root'", "", "ERROR_BASE_DATOS"),
    ("Estamos en mantenimiento, vuelve pronto", "", "MANTENIMIENTO"),
    ("419 | Page Expired", "", "SESION_EXPIRADA"),
    # El indicador puede venir solo en el título, no en el cuerpo
    ("", "403 Forbidden", "ERROR_HTTP"),
    # Mensajes de permisos en español (no calzaban antes: quedaban sin
    # clasificar y el test se veía con el TimeoutException crudo de Selenium)
    ("No tienes permisos para realizar esta acción", "", "ERROR_PERMISOS"),
    ("Acceso denegado", "", "ERROR_PERMISOS"),
    ("401 Unauthorized", "", "ERROR_PERMISOS"),
    # Insensible a mayúsculas/minúsculas
    ("ACCESO DENEGADO", "", "ERROR_PERMISOS"),
    ("estamos en MANTENIMIENTO, vuelve pronto", "", "MANTENIMIENTO"),
])
def test_es_pagina_error_servidor_clasifica_por_contenido(texto_pagina, titulo, categoria_esperada):
    driver = DriverFalso(texto_pagina=texto_pagina, titulo=titulo)
    es_error, tipo = es_pagina_error_servidor(driver)
    if categoria_esperada is None:
        assert es_error is False
        assert tipo is None
    else:
        assert es_error is True
        assert tipo == categoria_esperada


def test_es_pagina_error_servidor_no_truena_si_el_driver_falla():
    driver = DriverFalso(fallar_todo=True)
    es_error, tipo = es_pagina_error_servidor(driver)
    assert es_error is False
    assert tipo is None


# ---------------------------------------------------------------------------
# manejar_error_test(): el corazón de la robustez — no debe reventar NUNCA,
# sin importar qué tan mal se porte el driver que le pasen.
# ---------------------------------------------------------------------------

def test_manejar_error_test_caso_normal_selenium():
    """Un TimeoutException común, página normal (sin señales de error real)."""
    driver = DriverFalso(texto_pagina="Formulario de inventario", url="http://intranet.local/inventario")
    resultado = manejar_error_test(driver, TimeoutException("esperando botón"), "test_ejemplo")

    assert resultado["tipo_error"] == "TIEMPO_ESPERA"
    assert resultado["es_error_servidor"] is False
    assert len(driver.capturas_tomadas) == 1  # sí se tomó captura


def test_manejar_error_test_detecta_error_real_de_servidor():
    """Aunque Selenium haya lanzado un TimeoutException genérico, si la
    página muestra un 500 de Laravel, debe reclasificarse como tal."""
    driver = DriverFalso(
        texto_pagina="Internal Server Error\nBadMethodCallException\nMethod ... does not exist.",
        url="http://intranet.local/inventario",
    )
    resultado = manejar_error_test(driver, TimeoutException("esperando botón"), "test_ejemplo")

    assert resultado["tipo_error"] == "ERROR_SERVIDOR_APP"
    assert resultado["es_error_servidor"] is True
    assert "Internal Server Error" in resultado["mensaje"]


def test_manejar_error_test_captura_texto_de_alerta():
    driver = DriverFalso(
        texto_pagina="Formulario de inventario",
        alerta_texto="No tienes permisos para esta acción",
    )
    resultado = manejar_error_test(driver, ElementClickInterceptedException("x"), "test_ejemplo")

    assert resultado["alerta_texto"] == "No tienes permisos para esta acción"
    assert driver._alerta.aceptada is True  # se cerró la alerta


def test_manejar_error_test_sin_alerta_no_rompe_nada():
    driver = DriverFalso(texto_pagina="Formulario de inventario")
    resultado = manejar_error_test(driver, NoSuchElementException("x"), "test_ejemplo")
    assert resultado["alerta_texto"] is None


def test_manejar_error_test_nunca_lanza_excepcion_aunque_el_driver_falle_en_todo():
    """La prueba más importante de todas: si el driver falso está
    configurado para fallar en CUALQUIER método (screenshot, find_element,
    etc.), manejar_error_test() debe seguir devolviendo un resultado
    válido, sin propagar ninguna excepción hacia arriba."""
    driver = DriverFalso(fallar_todo=True)

    try:
        resultado = manejar_error_test(driver, TimeoutException("x"), "test_hostil")
    except Exception as e:
        pytest.fail(f"manejar_error_test() no debería lanzar excepciones, pero lanzó: {e!r}")

    assert resultado["tipo_error"] == "TIEMPO_ESPERA"
    assert isinstance(resultado["mensaje"], str)
    assert resultado["es_error_servidor"] is False


def test_manejar_error_test_devuelve_siempre_las_mismas_llaves():
    """Cualquier código que use el resultado (como conftest.py) confía en
    que estas llaves siempre existan, pase lo que pase."""
    driver = DriverFalso(texto_pagina="ok")
    resultado = manejar_error_test(driver, RuntimeError("algo raro"), "test_x")

    llaves_esperadas = {"tipo_error", "mensaje", "es_error_servidor", "alerta_texto"}
    assert llaves_esperadas.issubset(resultado.keys())
