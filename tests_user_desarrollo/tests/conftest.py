import logging
import threading
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import glob
import pytest_html
from datetime import datetime
from utili.config import *
from utili.locators import *
from utili.logger import logger


@pytest.fixture(scope="session", autouse=True)
def reset_logger():
    os.makedirs("/workspace/reports/logs", exist_ok=True)
    os.makedirs("/workspace/reports/screen", exist_ok=True)

    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()

    archivo = logging.FileHandler(
        "/workspace/reports/logs/ejecucion.log",
        mode="w",
        encoding="utf-8"
    )

    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    archivo.setFormatter(formato)
    logger.addHandler(archivo)

    # limpiar capturas previas
    for archivo_scr in glob.glob("/workspace/reports/screen/*"):
        try:
            os.remove(archivo_scr)
        except Exception:
            pass

    # limpiar descargas previas, una sola vez por sesión
    os.makedirs("/workspace/descargas", exist_ok=True)
    for archivo_desc in glob.glob("/workspace/descargas/*"):
        try:
            os.remove(archivo_desc)
        except Exception:
            pass
            pass

    yield

    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()


@pytest.fixture
def driver():
    # Host directory where test runner expects downloads to appear
    host_download_dir = "/workspace/descargas"
    os.makedirs(host_download_dir, exist_ok=True)

    # Path inside the Selenium/browser container where Chrome will actually write downloads.
    # IMPORTANT: you must bind-mount the host `host_download_dir` to this container path
    # when launching the Selenium node (example below).
    container_download_dir = os.environ.get("SELENIUM_CONTAINER_DOWNLOAD_DIR", "/home/seluser/descargas")

    options = Options()

    prefs = {
        # Path inside the browser container
        "download.default_directory": container_download_dir,
        # No preguntar dónde guardar
        "download.prompt_for_download": False,
        # Crear/usar la carpeta automáticamente
        "download.directory_upgrade": True,
        # Evitar que Chrome intente abrir ciertos tipos (ej. PDF)
        "plugins.always_open_pdf_externally": True,
        # Evitar popup de descargas
        "profile.default_content_settings.popups": 0,
        # Relajar protecciones de safebrowsing para permitir descargas automáticas en CI
        "safebrowsing.enabled": True,
        "safebrowsing.disable_download_protection": True,
        # Desactivar servicios que guardan credenciales
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }

    options.add_argument("--disable-features=FileSystemAccessAPI")
    options.add_experimental_option("prefs", prefs)

    # Abrir Chrome maximizado
    options.add_argument("--start-maximized")

    # Evitar mensaje "Chrome está siendo controlado..."
    options.add_experimental_option(
        "excludeSwitches",
        ["enable-automation"]
    )

    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-notifications")

    driver = webdriver.Remote(
        command_executor="http://selenium-chrome:4444/wd/hub",
        options=options
    )

    # Forzar comportamiento de descargas vía CDP para Chromedriver/Chrome
    # Esto le indica al navegador la carpeta donde escribir descargas sin mostrar diálogos.
    try:
        driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": container_download_dir
        })
    except Exception:
        # Algunos drivers/remotes pueden no soportar CDP; en ese caso las prefs ayudan.
        pass

    driver.get(URL)

    # Nota para el usuario: asegúrate de montar la carpeta del host en el contenedor
    # por ejemplo, en `docker run` o `docker-compose` del nodo Chrome:
    # -v /workspace/descargas:/home/seluser/descargas
    # Si usas otra ruta dentro del contenedor cambia la variable de entorno
    # `SELENIUM_CONTAINER_DOWNLOAD_DIR` para que coincida.

    yield driver

    driver.quit()


@pytest.fixture
def driver_logueado(driver):
    logger.info(f"URL: {URL}")
    logger.info(f"USUARIO: {USUARIO}")

    # Esperar elementos de login
    WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, LOGIN_USUARIO))
    )
    driver.find_element(By.XPATH, LOGIN_USUARIO).send_keys(USUARIO)

    WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, LOGIN_PASSWORD))
    )
    driver.find_element(By.XPATH, LOGIN_PASSWORD).send_keys(PASSWORD)

    WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable((By.XPATH, LOGIN_BOTON))
    )
    driver.find_element(By.XPATH, LOGIN_BOTON).click()

    WebDriverWait(driver, TIMEOUT).until(
        EC.url_contains("dashboard")
    )

    logger.info(f"URL actual: {driver.current_url}")
    logger.info("LOGIN EN FIXTURE driver_logueado EXITOSO")

    yield driver

def pytest_html_report_title(report):
    report.title = "Reporte de Automatización — Servitel Intranet"


def pytest_configure(config):
    if not hasattr(config, "_metadata"):
        config._metadata = {}
    config._metadata.update({
        "Proyecto": "QA Automation - Intranet Servitel",
        "Entorno": "QA / Staging",
        "Navegador": "Chrome (Selenium Grid)",
    })

_resultados_sesion = []

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extras", [])

    if report.when == "call":
        entrada = {
            "test": item.name,
            "archivo": str(item.fspath).split("/tests/")[-1],
            "resultado": "FAILED" if report.failed else ("SKIPPED" if report.skipped else "PASSED"),
            "tipo_error": None,
            "mensaje": None,
            "url": None,
            "captura": None,
            "texto_error": None,
            "log_pasos": None,   # 👈 nuevo campo
        }

        if report.failed and call.excinfo is not None:
            from utili.errores import tipificar_error
            entrada["tipo_error"] = tipificar_error(call.excinfo.value)
            entrada["mensaje"] = str(call.excinfo.value).strip().split("\n")[0] or type(call.excinfo.value).__name__

            # 👇 NUEVO: extraer el log de pasos capturado durante el test
            log_call = next(
                (contenido for titulo, contenido in report.sections if "log call" in titulo.lower()),
                None
            )
            entrada["log_pasos"] = log_call

            driver_actual = item.funcargs.get("driver_logueado") or item.funcargs.get("driver")
            if driver_actual is not None:
                try:
                    entrada["url"] = driver_actual.current_url
                except Exception:
                    pass

            nombre_test = item.name
            capturas = sorted(
                glob.glob(f"/workspace/reports/screen/{nombre_test}_*.png"),
                key=os.path.getmtime, reverse=True
            )
            if capturas:
                entrada["captura"] = capturas[0]
                with open(capturas[0], "rb") as img_file:
                    import base64
                    img_b64 = base64.b64encode(img_file.read()).decode()
                extra.append(pytest_html.extras.image(img_b64, mime_type="image/png"))

            textos = sorted(
                glob.glob(f"/workspace/reports/screen/{nombre_test}_ERROR_*.txt"),
                key=os.path.getmtime, reverse=True
            )
            if textos:
                entrada["texto_error"] = textos[0]
                with open(textos[0], "r", encoding="utf-8") as f:
                    contenido = f.read()
                contenido_html = (
                    contenido.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                )
                extra.append(pytest_html.extras.html(
                    f"<details><summary><b>Texto del error (clic para expandir)</b></summary>"
                    f"<pre style='white-space:pre-wrap; background:#f6f6f6; padding:10px; "
                    f"border:1px solid #ddd; max-height:400px; overflow-y:auto;'>{contenido_html}</pre></details>"
                ))

        _resultados_sesion.append(entrada)

    report.extras = extra

def pytest_sessionfinish(session, exitstatus):
    ruta = "/workspace/reports/logs/resumen_ia.txt"

    fallidos = [r for r in _resultados_sesion if r["resultado"] == "FAILED"]
    pasados = [r for r in _resultados_sesion if r["resultado"] == "PASSED"]
    saltados = [r for r in _resultados_sesion if r["resultado"] == "SKIPPED"]

    with open(ruta, "w", encoding="utf-8") as f:
        f.write("RESUMEN DE EJECUCIÓN DE PRUEBAS AUTOMATIZADAS\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total: {len(_resultados_sesion)} | Pasaron: {len(pasados)} | Fallaron: {len(fallidos)} | Saltados: {len(saltados)}\n")
        f.write("=" * 70 + "\n\n")

        if fallidos:
            f.write("PRUEBAS FALLIDAS (requieren atención):\n\n")
            for r in fallidos:
                f.write("-" * 70 + "\n")
                f.write(f"TEST: {r['test']}\n")
                f.write(f"ARCHIVO: {r['archivo']}\n")
                f.write(f"TIPO_ERROR: {r['tipo_error']}\n")
                f.write(f"MENSAJE: {r['mensaje']}\n")
                f.write(f"URL: {r['url']}\n")
                f.write(f"CAPTURA: {r['captura']}\n")
                f.write(f"TEXTO_ERROR_DETALLADO: {r['texto_error']}\n\n")

        if saltados:
            f.write("PRUEBAS SALTADAS:\n")
            for r in saltados:
                f.write(f"  - {r['test']} ({r['archivo']})\n")
            f.write("\n")

    logger.info(f"Resumen para IA generado en: {ruta}")

    # Se envía en un hilo aparte para que el resumen final de pytest se
    # muestre de inmediato, sin esperar a que la IA termine de generar
    # las historias (puede tardar varios minutos si hay varios errores).
    # El hilo NO es "daemon" a propósito: así, aunque termine el resto
    # del proceso, Python espera a que el envío realmente concluya antes
    # de cerrar del todo, y no se pierde el reporte a medio camino.
    from utili.notificar_ia import enviar_resumen_a_ia
    threading.Thread(
        target=enviar_resumen_a_ia,
        args=(ruta, fallidos),
        name="enviar-resumen-ia",
        daemon=False,
    ).start()