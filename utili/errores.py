from datetime import datetime
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    InvalidSelectorException,
    NoSuchWindowException,
    UnexpectedAlertPresentException,
    NoAlertPresentException,
    SessionNotCreatedException,
    InvalidSessionIdException,
    JavascriptException,
    MoveTargetOutOfBoundsException,
    WebDriverException,
)
from utili.logger import logger

# Tipos que vale la pena reintentar automáticamente (son fallas
# transitorias de timing/render, no defectos reales de la app).
REINTENTABLES = {
    "TIEMPO_ESPERA",
    "ELEMENTO_DESACTUALIZADO",
    "ELEMENTO_INTERCEPTADO",
}

# Errores que indican un bug en el PROPIO script de automatización
# (locator mal escrito, variable inexistente, etc.), no un defecto de
# la aplicación bajo prueba. Vale la pena distinguirlos porque el
# arreglo va del lado del test, no de la app.
ERRORES_DE_SCRIPT = (KeyError, AttributeError, TypeError, IndexError, NameError, ValueError)


def tipificar_error(error):
    """
    Clasifica una excepción de Python/Selenium en una categoría legible.
    El orden de los `elif` importa: de más específico a más genérico,
    porque varias excepciones de Selenium heredan de WebDriverException.
    """

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

    elif isinstance(error, (UnexpectedAlertPresentException, NoAlertPresentException)):
        return "ALERT_INESPERADO"

    elif isinstance(error, MoveTargetOutOfBoundsException):
        return "ELEMENTO_FUERA_DE_VISTA"

    elif isinstance(error, JavascriptException):
        return "SCRIPT_JS_FALLIDO"

    elif isinstance(error, (SessionNotCreatedException, InvalidSessionIdException)):
        return "NAVEGADOR_DESCONECTADO"

    elif isinstance(error, WebDriverException):
        # Catch-all de Selenium: problemas de conexión con el navegador/grid
        # que no calzan en ninguna categoría más específica de arriba.
        return "ERROR_DRIVER"

    elif isinstance(error, AssertionError):
        # El test corrió sin problemas técnicos, pero lo que verificó
        # no se cumplió (la app hizo algo distinto a lo esperado).
        return "FALLO_ASERCION"

    elif isinstance(error, ERRORES_DE_SCRIPT):
        # Bug en el propio código del test (locator, variable, etc.),
        # no necesariamente un defecto de la aplicación.
        return "ERROR_EN_SCRIPT_TEST"

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
    Detecta si la página actual es una pantalla de error real (del
    framework/app, del servidor web, de la base de datos, de sesión, de
    permisos, o de mantenimiento) en vez de la app funcionando normal.

    Devuelve una tupla (es_error, tipo):
      - (True, 'ERROR_BASE_DATOS'):    la app no pudo conectar/consultar la BD
      - (True, 'MANTENIMIENTO'):       la app está en modo mantenimiento
      - (True, 'SESION_EXPIRADA'):     token CSRF vencido / sesión expirada (419, etc.)
      - (True, 'ERROR_PERMISOS'):      401 / acceso denegado / sin permisos para la acción
      - (True, 'ERROR_SERVIDOR_APP'):  excepción de Laravel/PHP con traza visible
      - (True, 'ERROR_HTTP'):          403/404/500/502/503/etc genérico (Nginx/Apache),
                                        sin la app de por medio
      - (False, None):                la página se ve normal

    El orden de chequeo va de lo más específico a lo más genérico, para
    que un error de base de datos no se quede clasificado solo como
    "ERROR_HTTP" por traer un 500 en el texto.

    La comparación es insensible a mayúsculas/minúsculas: la app muestra
    mensajes en español con distinta capitalización según el componente
    (ej. "Acceso denegado" vs "ACCESO DENEGADO"), y antes de esto un
    indicador solo calzaba si venía exactamente como estaba escrito aquí.
    """
    indicadores = {
        "ERROR_BASE_DATOS": [
            "SQLSTATE", "could not find driver", "Connection refused",
            "Access denied for user", "Unknown database", "PDOException",
            "SQLSTATE[HY000]", "Too many connections",
        ],
        "MANTENIMIENTO": [
            "Estamos en mantenimiento", "en mantenimiento", "Back soon",
            "Down for maintenance", "Service Unavailable",
        ],
        "SESION_EXPIRADA": [
            "419 | Page Expired", "Page Expired", "CSRF token mismatch",
            "TokenMismatchException", "su sesión ha expirado", "Session has expired",
        ],
        # Antes de esto, un 401 o un mensaje de "no tienes permisos" en español
        # no calzaba con ningún indicador (los de ERROR_HTTP eran genéricos en
        # inglés), así que la página se veía "normal" para esta función y el
        # test se quedaba con el TimeoutException crudo de Selenium (TIEMPO_ESPERA)
        # aunque la causa real fuera un error de permisos.
        "ERROR_PERMISOS": [
            "401", "Unauthorized", "No autorizado", "No autorizada",
            "No tiene permiso", "No tienes permiso", "No tiene permisos", "No tienes permisos",
            "No cuenta con permisos", "No cuentas con permisos",
            "Acceso denegado", "Sin autorización", "Sin permisos",
            "No tienes acceso", "No tienes autorización",
        ],
        "ERROR_SERVIDOR_APP": [
            "Internal Server Error", "BindingResolutionException", "Exception trace",
            "Fatal error", "Whoops", "Illuminate\\", "BadMethodCallException",
            "MethodNotAllowedHttpException", "NotFoundHttpException", "QueryException",
        ],
        "ERROR_HTTP": [
            "400", "403", "404", "500", "502", "503", "504",
            "Bad Request", "Forbidden", "Not Found", "Bad Gateway",
            "Service Unavailable", "Gateway Timeout",
        ],
    }

    try:
        texto_pagina = driver.find_element("tag name", "body").text
    except Exception:
        texto_pagina = ""

    try:
        titulo = driver.title or ""
    except Exception:
        titulo = ""

    texto_completo_lower = f"{texto_pagina}\n{titulo}".lower()

    for tipo in (
        "ERROR_BASE_DATOS", "MANTENIMIENTO", "SESION_EXPIRADA",
        "ERROR_PERMISOS", "ERROR_SERVIDOR_APP", "ERROR_HTTP",
    ):
        if any(ind.lower() in texto_completo_lower for ind in indicadores[tipo]):
            return True, tipo

    return False, None

def manejar_error_test(driver, error, nombre_test):
    """
    Manejo estándar de errores para todos los tests:
    - Detecta y cierra alertas nativas de JS ANTES de tocar el driver: muchos
      navegadores BLOQUEAN cualquier comando (incluido el screenshot) mientras
      hay una alerta nativa abierta, así que se cierra primero para no
      arriesgar que falle la captura. Su aspecto visual casi nunca queda en
      la imagen de todas formas (limitación del navegador, no de este código)
      — por eso el TEXTO de la alerta ('alerta_texto') es el respaldo confiable.
    - Loguea el error tipificado (o el error real de servidor si aplica)
    - Toma captura de pantalla del navegador (siempre, salvo que falle)
    - Si es una página de error de servidor (Laravel/PHP/BD/etc.), guarda el texto también
    """
    nombre_archivo = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = f"reports/screen/{nombre_test}_{nombre_archivo}.png"

    tipo_error = tipificar_error(error)
    mensaje_error = str(error).strip() or type(error).__name__

    # 0. Si la página muestra un error real (de la app o del servidor web),
    #    esa es la causa real — sobreescribimos el tipo/mensaje genérico de Selenium
    es_error_servidor = False
    try:
        es_error_servidor, tipo_detectado = es_pagina_error_servidor(driver)
        if es_error_servidor:
            tipo_error = tipo_detectado
            texto_pagina = driver.find_element("tag name", "body").text
            lineas = [l.strip() for l in texto_pagina.split("\n") if l.strip()]
            mensaje_error = " | ".join(lineas[:3]) if lineas else (driver.title or mensaje_error)
    except Exception:
        pass

    logger.error(f"========== ERROR: {nombre_test.upper()} ==========")
    logger.error(f"TIPO DE ERROR: {tipo_error}")
    logger.error(f"DETALLE: {mensaje_error}")

    # 1. Revisar y cerrar alerta nativa de JS ANTES de cualquier otra interacción
    alerta_texto = None
    try:
        alerta = driver.switch_to.alert
        alerta_texto = alerta.text
        logger.warning(f"ALERTA DETECTADA Y CERRADA: {alerta_texto}")
        alerta.accept()
    except Exception:
        pass  # no había alerta, seguimos normal

    # 2. Ahora ya es seguro pedir la URL
    try:
        logger.error(f"URL: {driver.current_url}")
    except Exception:
        logger.error("URL: (no se pudo obtener)")

    # 3. Y ahora sí, captura sin riesgo de congelarse
    try:
        driver.save_screenshot(ruta)
        logger.error(f"CAPTURA: {ruta}")
    except Exception as se:
        logger.error(f"No se pudo tomar captura: {se}")

    # 4. Si detectamos página de error de servidor, guardamos el texto también
    if es_error_servidor:
        ruta_txt = f"reports/screen/{nombre_test}_ERROR_{nombre_archivo}.txt"
        guardar_texto_pagina_error(driver, ruta_txt)
        logger.error(f"TEXTO DE ERROR GUARDADO: {ruta_txt}")

    logger.error(f"========== FIN {nombre_test.upper()} ==========\n")

    return {
        "tipo_error": tipo_error,
        "mensaje": mensaje_error,
        "es_error_servidor": es_error_servidor,
        # NUEVO: se capturaba pero antes nunca se devolvía, así que se
        # perdía para cualquier código que llamara a esta función.
        "alerta_texto": alerta_texto,
    }