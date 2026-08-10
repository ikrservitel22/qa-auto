# Contexto del proyecto

## Resumen general

Este proyecto es una suite de automatización end-to-end para una aplicación web.
Utiliza Python, `pytest` y Selenium WebDriver con un servidor de Selenium remoto en contenedores Docker.

- Framework de pruebas: `pytest`
- Navegador: Google Chrome en Selenium Grid remoto
- Arquitectura: fixtures en `tests/conftest.py`, localizadores centralizados en `utili/locators.py`, configuración en `utili/config.py`
- Artefactos: logs en `reports/logs/`, capturas en `reports/screen/`, reportes HTML en `reports/html/`, descargas en `descargas/`

## Estructura del repositorio

- `/tests`
  - `test_01_login.py`: login y logout
  - `test_02_novedades.py`: creación y navegación de novedades
  - `test_03_horarios.py`: validación de horarios y solicitudes, incluye descarga de archivos
  - `test_04_horas_extra.py`: pruebas del módulo Horas extra y validación de modales
  - `test_05_inventario.py`: pruebas de inventario y creación de artículos
  - `test_06_proyectos.py`: flujo de proyectos con ver, editar, volver y nuevo proyecto
  - `test_07_servidores.py`: flujo de servidores con inventario y detalle de servidor
  - `test_08_organigrama.py`: flujo de organigrama con opciones Completo, Áreas, Líderes y Mi Área
  - `conftest.py`: fixtures `driver`, `driver_logueado` y `reset_logger`
- `/utili`
  - `config.py`: carga de `credentials.json`, URL base, credenciales y constantes de timeout/ruta
  - `locators.py`: localizadores XPATH centralizados
  - `logger.py`: configuración del logger global
  - `downloads.py`: helper de descargas con cookies del navegador
  - `errores.py`: tipificación de excepciones Selenium y manejo de errores reintentables
  - `waits.py`: helpers de espera y clic seguro para Selenium
- `/reports`
  - `screen/`: capturas en caso de fallo
  - `logs/`: archivos de log de la ejecución
  - `html/`: reporte HTML final
- `/descargas`: carpeta de descargas del navegador
- `/assets`: CSS y estilos para reportes
- `docker-compose.yml`: servicios `qa-dev` y `chrome`
- `dockerfile`: imagen base para el contenedor de desarrollo
- `pytest.ini`: configuración de pytest
- `requirements.txt`: dependencias del proyecto

## Dependencias principales

- `selenium==4.11.2`
- `pytest==7.3.1`
- `webdriver-manager==3.8.6`
- `pytest-html==3.1.1`
- `requests==2.31.0`

## Cómo se ejecuta

1. Levantar los servicios Docker:

```bash
docker-compose up -d
```

2. Ejecutar los tests:

```bash
python -m pytest -s tests/ --html=reports/html/reporte.html --self-contained-html
```

### Notas de ejecución

- El fixture `driver` se conecta a `http://selenium-chrome:4444/wd/hub`.
- Ejecutar los tests desde el contenedor `qa-dev` o desde el workspace local con el servicio Selenium activo.
- Si se desea, usar `pytest` directamente para generar los reportes HTML en `reports/html/reporte.html`.

## Rutas importantes

- Tests: `/workspace/tests/`
- Localizadores: `/workspace/utili/locators.py`
- Configuración: `/workspace/utili/config.py`
- Logs: `/workspace/reports/logs/`
- Capturas: `/workspace/reports/screen/`
- Descargas: `/workspace/descargas/`
- Reporte HTML: `/workspace/reports/html/reporte.html`

## Flujo de pruebas y fixtures

- `tests/conftest.py` crea y asegura la existencia de `/workspace/descargas/`.
- Se limpian artefactos previos cuando corresponde.
- `driver` se inicializa con `webdriver.Remote` hacia `http://selenium-chrome:4444/wd/hub`.
- `driver_logueado` realiza login usando los localizadores y credenciales definidos en `utili/config.py`.
- `reset_logger` prepara el archivo de log antes de cada ejecución.

## Manejo de errores

- Los tests deben envolver la lógica principal en `try/except`.
- En caso de excepción se tipifica el error con `tipificar_error(e)`.
- Se registra la excepción y la URL actual.
- Se toma captura de pantalla en `reports/screen/`.
- Se relanza la excepción con `raise` tras la gestión.

## Helpers y utilidades

### utili/waits.py

- `wait_visible_xpath(driver, xpath, timeout=None)`
- `wait_clickable_xpath(driver, xpath, timeout=None)`
- `click_when_clickable(driver, xpath, timeout=None)`
- `click_sidebar_menu_item(driver, sidebar_button_xpath, menu_item_xpath, timeout=None)`
- `wait_for_url(driver, url, timeout=None)`
- `send_keys_when_visible(driver, xpath, text, timeout=None)`
- `wait_text_in_element(driver, xpath, text, timeout=None)`
- `wait_text_present(driver, text, timeout=None)`
- `wait_text_in_page(driver, text, timeout=None)`

### utili/locators.py

- Centraliza los XPATHs en constantes reutilizables.
- Usa prefijos claros para identificar módulos, páginas y campos.
- Mantiene los localizadores separados del código de prueba.

### utili/errores.py

- Tipifica excepciones Selenium en códigos legibles.
- Permite clasificar errores reintentables.

### utili/downloads.py

- Facilita descargas mediante cookies del browser.
- Detecta el nombre del archivo a partir de `Content-Disposition` o de la URL.

## Tests nuevos y actualizados

- `tests/test_06_proyectos.py`: flujo de proyectos con ver, editar, volver y nuevo proyecto.
- `tests/test_07_servidores.py`: flujo de servidores con inventario y detalle de servidor.
- `tests/test_08_organigrama.py`: flujo de organigrama con opciones Completo, Áreas, Líderes y Mi Área.

## Buenas prácticas y convenciones

- Importar constantes explícitas desde `utili.locators` cuando sea posible.
- Usar helpers de `utili/waits.py` en lugar de `time.sleep`.
- Mantener `try/except` en los tests para capturas y logging.
- Evitar XPATHs inline en los tests nuevos.
- Usar constantes de ruta y timeout definidas en `utili/config.py`.

## Mejoras aplicadas

- Centralización de localizadores en `utili/locators.py`
- Nuevos helpers de espera y clic en `utili/waits.py`
- Uso de constantes de localizadores en tests recientes
- Eliminación de dependencias no usadas en `requirements.txt`
- Actualización de `.gitignore` para ignorar `descargas/`

## Reglas para cambios de código

- No cambiar la estructura de carpetas sin autorización.
- No renombrar variables, funciones o archivos existentes sin aprobación.
- No mover lógica entre archivos sin autorización.
- No agregar librerías nuevas sin autorización.
- No modificar código no solicitado.
- No inventar XPATHs.
- No inventar nombres de métodos.
- No crear Page Object Model sin solicitud explícita.
- Mantener el estilo existente del proyecto.

## Plantilla recomendada para tests nuevos

```py
from datetime import datetime

from utili.config import *
from utili.locators import *
from utili.logger import logger
from utili.errores import tipificar_error
from utili.waits import click_when_clickable, wait_visible_xpath, wait_text_present


def test_mi_nuevo_flujo(driver_logueado):
    try:
        logger.info("========== INICIO test_mi_nuevo_flujo ==========")

        click_when_clickable(driver_logueado, SIDEBAR_MI_MODULO_BUTTON)
        click_when_clickable(driver_logueado, MENU_MI_MODULO_OPCION)

        wait_visible_xpath(driver_logueado, MI_MODULO_PAGE_TITLE)
        wait_text_present(driver_logueado, "Texto esperado")

        logger.info("========== FIN test_mi_nuevo_flujo ==========")

    except Exception as e:
        tipo_error = tipificar_error(e)
        logger.exception(f"ERROR EN test_mi_nuevo_flujo: {e}")
        logger.info(f"URL al fallar: {driver_logueado.current_url}")
        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")
        driver_logueado.save_screenshot(f"reports/screen/mi_nuevo_flujo_{nombre}.png")
        raise
```

Notas:
- Definir XPATHs en `utili/locators.py` y usar constantes en los tests.
- Evitar XPATHs inline en los tests nuevos.
- Usar helpers de `utili/waits.py`.
- Para descargas, validar `/workspace/descargas/`.
- Para modales o ventanas nuevas, usar `wait_text_in_page` y `window_handles` según sea necesario.

## Nota sobre contexto del proyecto

- Este archivo `/workspace/contexto-proyecto.md` es la fuente de verdad del contexto del proyecto.
- La IA debe usar siempre este documento visible en el workspace como memoria del proyecto.
- No hay otra copia interna necesaria ni relevante.
- Si se borra el chat, mientras el archivo exista en el workspace puede consultarse de nuevo.

## Reglas obligatorias para generar código

- Nunca cambiar la estructura del proyecto sin solicitarlo.
- Nunca renombrar variables, funciones o archivos existentes.
- Nunca mover lógica entre archivos sin autorización.
- No agregar librerías nuevas sin autorización.
- No modificar código que no haya sido solicitado.
- Si falta información, preguntar antes de asumir.
- No inventar XPATH.
- No inventar nombres de métodos.
- No generar Page Object Model a menos que se solicite explícitamente.
- Mantener el mismo estilo de programación utilizado en el proyecto.

## Convenciones del proyecto

- Todos los tests utilizan `try/except`.
- Ante un error siempre:
  - registrar el error en el logger
  - tomar captura
  - relanzar la excepción con `raise`
- Todos los XPATH se almacenan en `utili/locators.py`.
- Todas las credenciales se leen desde `utili/config.py`.
- Las capturas se guardan en `reports/screen/`.
- Los logs se guardan en `reports/logs/`.
- Las descargas van en `descargas/`.

## Convenciones de nombres para localizadores

- Los nombres de constantes deben estar en mayúsculas y usar guiones bajos.
- Usar prefijos según el tipo de elemento:
  - `SIDEBAR_<MODULO>_BUTTON` para el botón principal del módulo en la barra lateral.
  - `MENU_<MODULO>_<OPCION>` para entradas de menú o submenú.
  - `<MODULO>_PAGE_TITLE` para títulos de página.
  - `<MODULO>_FORM_<CAMPO>_<TIPO>` para campos de formulario, por ejemplo `INV_FORM_PRODUCT_INPUT`.
  - `<MODULO>_<ACTION>_BUTTON` para botones de acción.
  - `TABLA_<MODULO>_...` para tablas y acciones de tabla.
- Evitar sufijos ambiguos como `_ALT` en los nombres de localizadores.
- Para inventario, usar:
  - `MENU_INVENTARIO_NUEVO_ARTICULO` para la opción del menú.
  - `INVENTARIO_NUEVO_ARTICULO_HEADER_BUTTON` para el botón de nuevo artículo dentro de la página.
  - `INVENTARIO_NUEVO_ARTICULO_TITLE` para el título del formulario.
  - `INV_FORM_*` para los campos del formulario.
- Para novedades, usar `MENU_NOVEDADES_NUEVA` para la opción de crear una novedad y `MENU_NOVEDADES_VER` para ver novedades.
- Mantener la misma estructura de nombres en todo el proyecto para facilitar el mantenimiento.

## Convenciones añadidas (implementadas)

- **Nombres de tests y logs:** Los nombres de test se registran automáticamente en los logs usando el nombre del nodo de pytest (`request.node.name`).
- **Selectores:** Todos los XPATHs se centralizan en `utili/locators.py`. Evitar XPATHs inline en los tests nuevos.
- **Timeouts y rutas:** `utili/config.py` expone `TIMEOUT`, `REPORTS_DIR`, `LOGS_DIR`, `SCREEN_DIR` y `DOWNLOADS_DIR`.
- **Waits compartidos:** Se añadió `utili/waits.py` con helpers `wait_visible_xpath`, `click_when_clickable` y `send_keys_when_visible` para estandarizar esperas y reducir `time.sleep`.
- **Login robusto:** La fixture `driver_logueado` usa esperas explícitas antes de interactuar con los campos de login y espera la URL del dashboard con `TIMEOUT`.
- **Limpieza de artefactos:** Al inicio de la ejecución se limpian `reports/screen/` y `descargas/`.
- **Dependencias:** Se fijaron versiones en `requirements.txt` para mejorar reproducibilidad.

Si quieres que aplique estas convenciones a todos los tests existentes (mover XPATHs y reemplazar llamadas), lo hago por lotes empezando por los tests que más fallan. ¿Por cuál empiezo? (recomiendo `tests/test_01_login.py` y `tests/test_04_horas_extra.py`).

## Cómo responder

Cuando se solicite código:

1. Explicar primero el motivo del cambio.
2. Mostrar únicamente el código necesario.
3. No modificar partes que no fueron solicitadas.
4. Conservar el formato del proyecto.
5. Si existe una mejor práctica, mencionarla pero no implementarla automáticamente.

## Qué NO hacer

- No cambiar imports.
- No cambiar nombres de variables.
- No cambiar nombres de funciones.
- No cambiar la estructura de carpetas.
- No refactorizar código existente.
- No optimizar código si no fue solicitado.
- No reemplazar XPATH por CSS Selectors sin autorización.

## Plantilla recomendada para nuevos tests

Usa esta plantilla como base cuando pidas crear un nuevo test: tú me das el flujo (acciones y XPATHs/constantes en `utili/locators.py`) y yo devuelvo el archivo listo.

- Requisitos:
  - Importar fixtures `driver` o `driver_logueado` según necesites sesión autenticada.
  - Usar los helpers de `utili/waits.py` (ej.: `click_when_clickable`, `wait_visible_xpath`, `wait_text_present`).
  - Registrar con `logger` las acciones principales.
  - Envolver flujo principal en `try/except` para capturar pantalla, log y relanzar.

Ejemplo (cambia nombres y XPATHs según el caso):

```py
from selenium.webdriver.common.by import By
from datetime import datetime
import time

from utili.config import *
from utili.locators import *
from utili.logger import logger
from utili.errores import tipificar_error
from utili.waits import click_when_clickable, wait_visible_xpath, wait_text_present

def test_mi_nuevo_flujo(driver_logueado):
    try:
        logger.info("========== INICIO test_mi_nuevo_flujo ==========")

        # Ejemplo de navegación: abrir módulo
        click_when_clickable(driver_logueado, SIDEBAR_MI_MODULO)
        click_when_clickable(driver_logueado, MENU_MI_OPCION)

        # Esperar un título de página usando locators centralizados
        wait_visible_xpath(driver_logueado, MI_MODULO_PAGE_TITLE)

        # Ejecutar la acción principal (usa locators desde utili/locators.py)
        click_when_clickable(driver_logueado, MI_BOTON_ACCION)

        # Validación: esperar texto o elemento que confirme la acción
        wait_text_present(driver_logueado, "Texto esperado")

        logger.info("Acción completada correctamente")
        logger.info("========== FIN test_mi_nuevo_flujo ==========")

    except Exception as e:
        tipo_error = tipificar_error(e)
        logger.exception(f"ERROR EN test_mi_nuevo_flujo: {e}")
        logger.info(f"URL al fallar: {driver_logueado.current_url}")
        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")
        driver_logueado.save_screenshot(f"reports/screen/mi_nuevo_flujo_{nombre}.png")
        raise
```

Notas de uso:
- No incluyas XPATHs literales en el test: define constantes en `utili/locators.py` y referencia esas constantes.
- Si el flujo descarga archivos, valida la descarga comprobando `/workspace/descargas` o usando `utili/downloads.py`.
- Para operaciones que abren nuevas pestañas o modales, usar los helpers y controles de `window_handles` y esperar por texto en la página completa (`wait_text_in_page`).

Si quieres, añado esta plantilla como un archivo ejemplo en `/workspace/tests/template_test_example.py`.

