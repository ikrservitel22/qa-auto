# Contexto del proyecto

## Resumen general

Proyecto de automatización de pruebas end-to-end para una aplicación web usando Python, pytest y Selenium.

- Framework de pruebas: `pytest`
- Navegador: Chrome en un contenedor Selenium standalone
- Arquitectura de pruebas: fixtures en `tests/conftest.py`, localizadores en `utili/locators.py`, configuración sensible en `utili/config.py`
- Reportes y artefactos: capturas, logs y descargas almacenadas en `reports/` y `descargas/`

## Estructura del repositorio

- `/tests`
  - `test_01_login.py`: casos de login y logout
  - `test_02_novedades.py`: creación y navegación de novedades
  - `test_03_horarios.py`: validación de módulos de horarios y solicitudes
  - `test_04_horas_extra.py`: ver, crear y validar botones/modales para horas extra
  - `test_05_inventario.txt`: pruebas relacionadas con inventario (archivo con extensión `.txt`, contiene casos comentados y utilitarios)
  - `conftest.py`: fixtures `driver` y `driver_logueado`; limpia descargas previas, configura el driver remoto y hace login automático
- `/utili`
  - `config.py`: carga de `credentials.json` con URL, usuario y contraseña
  - `locators.py`: XPaths de elementos usados en las pruebas
  - `logger.py`: configuración de logger para `reports/logs/ejecucion.log`
- `/assets`: estilos CSS para reportes HTML
- `/reports`
  - `screen/`: capturas de pantalla en fallos
  - `logs/`: logs de ejecución
- `/descargas`: carpeta destinada a descargas del navegador
- `docker-compose.yml`: define servicios `qa-dev` y `chrome` (`container_name: selenium-chrome`)
- `dockerfile`: imagen base para el contenedor de desarrollo
- `pytest.ini`: configuración de pytest y marcadores
- `requirements.txt`: dependencias del proyecto

## Dependencias principales

- `selenium`
- `pytest`
- `webdriver-manager`
- `pytest-html`
- `pyautogui`

## Cómo se ejecuta

El proyecto está pensado para correr en Docker con un contenedor de pruebas y un contenedor de Selenium:

- `docker-compose up -d`
- Ejecutar tests dentro del contenedor `qa-dev` o en el workspace con el servidor de Selenium activo
- Fixture `driver` se conecta a `http://selenium-chrome:4444/wd/hub`

## Comando de ejecución

Usar el siguiente comando para correr todos los tests y generar el reporte HTML:

```bash
python -m pytest -s tests/ --html=reports/html/reporte.html --self-contained-html
```

## Rutas importantes

- Tests: `/workspace/tests/`
- Localizadores: `/workspace/utili/locators.py`
- Configuración: `/workspace/utili/config.py`
- Logs: `/workspace/reports/logs/`
- Capturas de pantalla: `/workspace/reports/screen/`
- Descargas: `/workspace/descargas/`
- Reporte HTML: `/workspace/reports/html/reporte.html`

## Flujo de pruebas

1. `tests/conftest.py` crea o asegura `/workspace/descargas`, elimina archivos de descargas anteriores y configura las preferencias de Chrome para descargas automáticas.
2. La fixture `driver` se conecta al Selenium remoto en `http://selenium-chrome:4444/wd/hub`, abre la URL de la app y devuelve el driver.
3. La fixture `driver_logueado` usa `logger` para registrar el inicio del test, escribe usuario y contraseña desde `utili/config.py`, pulsa el botón de login y espera la URL del dashboard.
4. Los tests usan XPaths definidos en `utili/locators.py` y, en algunos casos, selectores XPath en línea dentro del test.
5. Si ocurre un error en un test, se registra la excepción, se toma una captura en `reports/screen/`, se guarda la ruta en el log y se relanza la excepción con `raise`.

## Manejo de errores

- Todos los tests envuelven su flujo principal en `try/except`.
- En el `except` se llama a `logger.exception(...)` para volcar el stack trace en `reports/logs/ejecucion.log`.
- Se captura la URL actual en el momento del fallo para facilitar el diagnóstico.
- Se genera un nombre de archivo con fecha/hora y se guarda una captura en `reports/screen/`.
- Finalmente, el error se relanza para que pytest marque el caso como fallido.

## Cambios detectados recientemente

- `tests/test_04_horas_extra.py`: nuevo conjunto de tests para el módulo "Horas extra" que incluye:
  - `test_ver_horas_extra`: abre el módulo y valida navegación a `/horas-extras/create`.
  - `test_crear_horas_extra`: completa el formulario de registro (fechas, horas, razón, justificación) y valida el mensaje de éxito.
  - `test_btones_horas_extra`: interactúa con botones de previsualización y modales.
- `tests/test_05_inventario.txt`: archivo con código de pruebas de inventario — actualmente guardado con extensión `.txt` y contiene tests comentados y utilitarios.
- `utili/errores.py`: nuevo módulo de tipificación de excepciones (`tipificar_error`) y determinación de errores reintentables (`es_reintentable`).
- `tests/conftest.py`: contiene nueva fixture `reset_logger` que recrea/limpia handlers del `logger` y configura `reports/logs/ejecucion.log`; la fixture `driver` configura preferencias de Chrome para descargas automáticas y desactiva características (`FileSystemAccessAPI`, popup-blocking, etc.).
- `utili/logger.py`: inicializa `logger` global y garantiza la carpeta `reports/logs`.

Estos cambios están reflejados en los archivos del workspace y se han resumido aquí para mantener el `contexto-proyecto.md` como la fuente de verdad.

## Detalles importantes

- `utili/config.py` carga `credentials.json` y define `URL`, `USUARIO`, `PASSWORD`.
- `utili/locators.py` centraliza la mayoría de los selectores XPath.
- El contenedor Selenium se expone en el puerto `4444`.
- Los pasos de login guardan logs en `reports/logs/ejecucion.log`.

## Nota sobre contexto del proyecto

- Este archivo `/workspace/contexto-proyecto.md` es la única fuente de verdad para el contexto del proyecto.
- La IA debe usar siempre este documento visible del workspace como memoria del proyecto.
- No hay otra copia interna necesaria ni relevante.
- Si se borra el chat, mientras el archivo exista en el workspace puede consultarse de nuevo.

## Reglas obligatorias para generar código

- Nunca cambiar la estructura del proyecto sin solicitarlo.
- Nunca renombrar variables, funciones o archivos existentes.
- Nunca mover lógica entre archivos.
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

