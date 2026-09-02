# Contexto del proyecto

## Resumen general

Este proyecto es una suite de automatización end-to-end para una aplicación web (la intranet de Servitel).
Utiliza Python, `pytest` y Selenium WebDriver con un servidor de Selenium remoto en contenedores Docker.

Desde 2026-08-28 el proyecto empezó a moverse hacia una arquitectura de microservicios: la ejecución de la
suite ya no depende únicamente de entrar por SSH al contenedor `qa-dev` — existe un servicio HTTP nuevo,
`orchestrator-api`, que dispara corridas, expone reportes/logs y permite limpiar artefactos, todo por API.
El reporte histórico agregado (a través del tiempo, entre corridas) se maneja en **otra plataforma externa**,
no en este repo — `orchestrator-api` solo expone los datos crudos por corrida para que esa plataforma los consuma.

- Framework de pruebas: `pytest`
- Navegador: Google Chrome en Selenium Grid remoto
- Arquitectura: fixtures en `tests/tests_intranet/conftest.py` (compartido por `test_usu_admin/` y
  `test_usu_desarrollo/`), localizadores centralizados en `utili/locators.py`,
  configuración en `utili/config.py`
- Microservicio nuevo: `orchestrator_api/` — API HTTP para disparar/consultar/borrar corridas (ver sección dedicada)
- Artefactos por corrida manual: logs en `reports/logs/`, capturas en `reports/screen/`, reportes HTML en `reports/html/`, descargas en `descargas/`
- Artefactos por corrida vía API: archivados en `reports/runs/{run_id}/` (report, logs, capturas, resumen_ia.txt, stdout.log)

## Estructura del repositorio

- `/tests`
  - `test_utili_errores.py`: unit tests puros de `utili/errores.py` (sin Selenium, sin conftest, usa un `DriverFalso`)
  - `tests_intranet/conftest.py`: **Fix 2026-09-02** — fixtures `driver`, `driver_logueado`, `reset_logger`; hooks de pytest-html y notificación a `ia-historias`. Antes vivía duplicado byte a byte en `test_usu_admin/conftest.py` y `test_usu_desarrollo/conftest.py`; se unificó en este único archivo (pytest lo aplica a ambas subcarpetas por jerarquía de directorios). `driver_logueado` resuelve el rol (`admin`/`desarrollo`) inspeccionando `request.node.fspath` en tiempo de ejecución de cada test — no un global fijado al importar el módulo — para que ambas suites usen sus propias credenciales incluso en una corrida combinada (`pytest tests/`) donde el conftest se importa una sola vez por proceso.
  - `tests_intranet/test_usu_admin/`: suite E2E con el usuario admin
    - `test_01_login.py` … `test_08_organigrama.py`: login/logout, novedades, horarios, horas extra, inventario, proyectos, servidores, organigrama
  - `tests_intranet/test_usu_desarrollo/`: la misma suite, pensada para el rol de desarrollo. **Fix 2026-09-02**: ya no comparte credenciales con `test_usu_admin` — ver nota de `utili/credentials.json` abajo
  - `__init__.py` en `tests/`, `tests/tests_intranet/`, `test_usu_admin/` y `test_usu_desarrollo/`: agregados el 2026-08-28 para que pytest genere nombres de módulo únicos (`tests.tests_intranet.test_usu_admin.test_01_login` vs `...test_usu_desarrollo.test_01_login`). Antes de esto, `pytest tests/` fallaba con "import file mismatch" porque ambas carpetas tienen archivos con el mismo nombre y no había `__init__.py`.
  - ⚠️ No existe ya un `tests/conftest.py` plano ni `tests/test_01_login.py` sueltos — esa estructura vieja fue reemplazada por la de `tests_intranet/`. Los `.zip` en la raíz (`tests.zip`, `tests_actualizado.zip`, `tests_user_desarrollo.zip`) son snapshots/backups manuales, no código vivo.
- `/utili`
  - `config.py`: carga de `credentials.json`, URL base, credenciales y constantes de timeout/ruta (sin overrides por variable de entorno). **Fix 2026-09-02**: `credentials.json` ahora tiene un bloque `admin` y un bloque `desarrollo` (URL sigue siendo compartida). `config.py` expone `USUARIO_ADMIN`/`PASSWORD_ADMIN` y `USUARIO_DESARROLLO`/`PASSWORD_DESARROLLO` como constantes simultáneas (no un solo `USUARIO`/`PASSWORD` conmutado por rol), porque el módulo se importa una sola vez por proceso y una corrida combinada (`pytest tests/`) ejecuta ambas suites en el mismo proceso — un singleton "activo" se habría pisado entre suites. `test_usu_admin/test_01_login.py` usa el par `_ADMIN`; `test_usu_desarrollo/test_01_login.py` usa el par `_DESARROLLO`. El `driver_logueado` compartido en `tests_intranet/conftest.py` elige el par correcto en tiempo de ejecución (ver fix 2026-09-02 de arriba) en vez de tener una copia fija por archivo. `USUARIO`/`PASSWORD` genéricos se mantienen como alias de `_ADMIN` solo por compatibilidad. **Pendiente**: el bloque `admin` de `credentials.json` es un placeholder (duplica el usuario `pruebas.dersarrollo` de desarrollo) hasta que se provean las credenciales reales de admin.
  - `locators.py`: localizadores XPATH centralizados
  - `logger.py`: configuración del logger global
  - `downloads.py`: helper de descargas con cookies del navegador
  - `errores.py`: tipificación de excepciones Selenium (`TIPO_ERROR`: MANTENIMIENTO, TIEMPO_ESPERA, ERROR_HTTP, **ERROR_PERMISOS** (nuevo, 2026-08-28), ALERT_INESPERADO, ERROR_EN_SCRIPT_TEST, etc.) y manejo de errores reintentables. `es_pagina_error_servidor()` reclasifica un `TimeoutException`/error genérico de Selenium si el **contenido real de la página** (body + título, comparación insensible a mayúsculas desde 2026-08-28) muestra un error de servidor/permisos — antes de esto, un 401 o un mensaje de permisos en español ("No tienes permisos", "Acceso denegado") no calzaba con ningún indicador y el test se quedaba clasificado solo como `TIEMPO_ESPERA`. **Fix 2026-09-01**: el listado de `ERROR_HTTP` ya no es una lista corta armada a mano — ahora se genera desde `HTTP_STATUS_REASONS`, un catálogo con todos los códigos 4xx/5xx estándar de IANA (antes faltaba, por ejemplo, el 501, que se quedaba mal clasificado como `TIEMPO_ESPERA`). También se agregó la excepción `ErrorPaginaServidorDetectado`, usada por `waits.py` (ver abajo) para cortar una espera en cuanto detecta una página de error, en vez de esperar el timeout completo.
  - `notificar_ia.py`: envía `resumen_ia.txt` + capturas/textos de error al servicio externo `ia-historias` (proyecto hermano `ia-usuario`) vía `POST http://ia-historias:8000/procesar-errores-adjuntos`; si no está disponible, solo loguea un warning y no rompe la corrida
  - `waits.py`: helpers de espera y clic seguro para Selenium. **Fix 2026-09-01**: todos los `wait_*` (`wait_visible_xpath`, `wait_clickable_xpath`, `wait_for_url`, `wait_text_in_element`, `wait_text_present`, `wait_text_in_page`, y las esperas internas de `click_por_texto_o_xpath`) pasan ahora por `_esperar_con_deteccion_de_error()`: si pasan 2s (`GRACIA_DETECCION_ERROR_S`) sin que aparezca el elemento esperado, en cada poll revisan además si la página es en realidad una pantalla de error del servidor (`es_pagina_error_servidor`) y, de serlo, lanzan `ErrorPaginaServidorDetectado` de inmediato en vez de seguir esperando hasta agotar el `TIMEOUT` completo (10s por defecto, y se acumulaba con cada wait encadenado dentro de un mismo test). Antes de este fix, un 403/501/etc. en la página hacía que el test esperara el timeout completo de cada wait antes de fallar, y en el caso del 501 ni siquiera se reclasificaba bien al final (ver fix de `errores.py` arriba). El margen de 2s evita penalizar con comandos extra el camino feliz, donde el elemento normalmente aparece de inmediato.
- `/orchestrator_api` — **microservicio nuevo**, ver sección dedicada más abajo
- `/reports`
  - `screen/`: capturas en caso de fallo (rutas fijas `/workspace/reports/screen`, compartidas entre corridas manuales)
  - `logs/`: `ejecucion.log` y `resumen_ia.txt` de la corrida manual más reciente (rutas fijas, se pisan en cada sesión de pytest)
  - `html/`: reporte HTML de la corrida manual más reciente
  - `runs/{run_id}/`: artefactos archivados por el `orchestrator-api`, uno por corrida disparada vía API (no se pisan entre sí)
- `/descargas`: carpeta de descargas del navegador
- `/assets`: CSS y estilos para reportes
- `.gitignore`: ya tenía la regla `reports/`, pero `reports/html/reporte.html` había quedado trackeado desde antes de que existiera esa regla (`.gitignore` no retroactúa) — **fix 2026-09-02**: se destrackeó con `git rm --cached` (el archivo local se conserva, solo dejó de generar diffs ruidosos en cada corrida).
- `docker-compose.yml`: servicios `qa-dev`, `chrome` y **`orchestrator-api`** (nuevo). El servicio `chrome` usaba `selenium/standalone-chrome:latest` (imagen flotante); desde el **fix 2026-09-01** está pinneado por digest (`selenium/standalone-chrome@sha256:cd778b6f38d9...`) a la build exacta que corresponde a `selenium==4.47.0`/Chrome 151 en `requirements.txt`, para que un futuro `docker pull`/rebuild no vuelva a driftear el grid por su cuenta mientras el cliente Python queda fijo.
- `dockerfile`: imagen base para el contenedor de desarrollo (`qa-dev`)
- `pytest.ini`: configuración de pytest (sin `testpaths`/`addopts`; solo markers `id` y `dependency`, sin selección por marker)
- `requirements.txt`: dependencias del proyecto (suite de tests)

## Dependencias principales

`requirements.txt` (raíz, usado por `qa-dev` y por `orchestrator-api`):
- `selenium==4.47.0`
- `pytest==9.1.1`
- `webdriver-manager==4.1.2`
- `pytest-html==4.2.0`
- `requests==2.34.2`
- `vncdotool==1.3.0`

**Fix 2026-09-01 (drift de dependencias resuelto)**: entre el 18-ago (commit que despinneó `requirements.txt`) y
el 31-ago (commit que lo re-pinneó a versiones viejas) hubo una ventana en la que `qa-dev` se reconstruyó con
versiones "latest" del momento; el 31-ago se repinnearon versiones antiguas en el repo pero **`qa-dev` nunca se
reconstruyó**, así que corría `selenium 4.47.0`/`pytest 9.1.1` mientras `requirements.txt` decía
`selenium==4.11.2`/`pytest==7.3.1`. Además `orchestrator-api` (reconstruido después del re-pin) sí tenía las
versiones viejas — es decir, **qa-dev y orchestrator-api corrían pytest/selenium en versiones distintas entre sí**,
pudiendo dar resultados distintos para la misma suite según por dónde se ejecutara. Se resolvió actualizando
`requirements.txt` a las versiones que ya estaban probadas y funcionando contra el grid actual (ver nota de
`docker-compose.yml` sobre el pin de la imagen de Chrome), y reconstruyendo ambas imágenes
(`docker compose build qa-dev orchestrator-api && docker compose up -d qa-dev orchestrator-api chrome`) para que
las dos coincidan exactamente. Verificado: `pip show` idéntico en ambos contenedores y `tests/test_utili_errores.py`
(36 tests) sigue pasando con pytest 9.1.1.

`orchestrator_api/requirements.txt` (solo dentro de la imagen de `orchestrator-api`, no toca el raíz):
- `fastapi==0.115.0`
- `uvicorn[standard]==0.30.6`

## Cómo se ejecuta

### Opción A: manual (SSH a `qa-dev`)

1. Levantar los servicios Docker:

```bash
docker-compose up -d
```

2. Ejecutar los tests (ya funciona combinado desde que se agregaron los `__init__.py` el 2026-08-28):

```bash
python -m pytest -s tests/ --html=reports/html/reporte.html --self-contained-html
```

   O por suite individual:
   ```bash
   python -m pytest -s tests/tests_intranet/test_usu_admin/ --html=reports/html/reporte.html --self-contained-html
   python -m pytest -s tests/tests_intranet/test_usu_desarrollo/ --html=reports/html/reporte.html --self-contained-html
   python -m pytest -s tests/test_utili_errores.py
   ```

### Opción B: vía `orchestrator-api` (recomendado para consumo externo)

```bash
docker-compose up -d chrome orchestrator-api
curl -X POST http://127.0.0.1:8080/runs -H 'Content-Type: application/json' -d '{"suite":"admin"}'
```

Ver la sección **Microservicio: orchestrator-api** más abajo para el detalle completo de endpoints.

### Notas de ejecución

- El fixture `driver` se conecta a `http://selenium-chrome:4444/wd/hub`.
- Ejecutar los tests desde el contenedor `qa-dev` (o `orchestrator-api`) o desde el workspace local con el servicio Selenium activo.
- Si se desea, usar `pytest` directamente para generar los reportes HTML en `reports/html/reporte.html`.
- **No correr `admin` y `desarrollo` en paralelo manualmente**: ambos conftest.py comparten las mismas rutas fijas (`reports/screen/`, `descargas/`) y se pisarían entre sí. El `orchestrator-api` ya serializa esto automáticamente.

## Rutas importantes

- Tests: `/workspace/tests/`
- Localizadores: `/workspace/utili/locators.py`
- Configuración: `/workspace/utili/config.py`
- Logs: `/workspace/reports/logs/`
- Capturas: `/workspace/reports/screen/`
- Descargas: `/workspace/descargas/`
- Reporte HTML: `/workspace/reports/html/reporte.html`
- Artefactos por corrida de API: `/workspace/reports/runs/{run_id}/`

## Flujo de pruebas y fixtures

- Ambas suites (`test_usu_admin/`, `test_usu_desarrollo/`) comparten `tests_intranet/conftest.py` (fix 2026-09-02, ver arriba), que crea y asegura la existencia de `/workspace/descargas/`.
- Se limpian artefactos previos (`reports/screen/*`, `descargas/*`) al inicio de cada sesión de pytest — rutas fijas, no parametrizadas por corrida.
- `driver` se inicializa con `webdriver.Remote` hacia `http://selenium-chrome:4444/wd/hub`.
- **Fix 2026-09-01**: la creación de la sesión remota y el `driver.get(URL)` inicial dentro del fixture `driver` están envueltos en `try/except` que llama `driver.quit()` y relanza si algo falla antes del `yield`. Antes de este fix, si `driver.get(URL)` fallaba (p. ej. la app bajo prueba caída o lenta), la excepción se propagaba antes del `yield` y `driver.quit()` (que está después del `yield`) nunca se ejecutaba — la sesión de Chrome quedaba huérfana en el grid. Como `selenium-chrome` solo admite una sesión simultánea (`maxSessions: 1`, default de la imagen), esa sesión huérfana bloqueaba cualquier corrida siguiente hasta que el grid la expiraba sola (`sessionTimeout` ~5 min), causando fallos en cascada de varios minutos cada uno. Este fix vivía duplicado en ambos `conftest.py`; desde el fix 2026-09-02 vive una sola vez en `tests_intranet/conftest.py`, compartido por las dos suites.
- `driver_logueado` realiza login usando los localizadores y credenciales definidos en `utili/config.py`.
- `reset_logger` prepara el archivo de log antes de cada ejecución.
- Al finalizar la sesión (`pytest_sessionfinish`), se escribe `resumen_ia.txt` y se lanza un hilo (no-daemon) que envía ese resumen a `ia-historias` — el proceso de pytest no termina del todo hasta que ese hilo acaba (hasta 1200s de timeout si `ia-historias` estuviera lento).
- `tests/test_utili_errores.py` no usa ninguno de estos fixtures (no tiene conftest en su ruta): es unit testing puro de `utili/errores.py`.

## Manejo de errores

- Los tests deben envolver la lógica principal en `try/except`.
- En caso de excepción se tipifica el error con `tipificar_error(e)`.
- Se registra la excepción y la URL actual.
- Se toma captura de pantalla en `reports/screen/`.
- Se relanza la excepción con `raise` tras la gestión.

## Microservicio: `orchestrator-api`

Agregado el 2026-08-28. Es un servicio HTTP independiente (contenedor propio) que dispara y gestiona corridas de
la suite sin necesidad de SSH manual a `qa-dev`. Es **aditivo**: no reemplaza `qa-dev` ni cambia `tests/`/`utili/`
más allá del fix de `__init__.py` ya documentado arriba.

### Dónde vive

- Código: `orchestrator_api/` (`app/main.py` endpoints, `app/runner.py` cola + ejecución, `app/analyzer.py`
  comparación de fallos, `app/models.py` esquemas, `app/store.py` registro en memoria)
- Imagen propia: `orchestrator_api/Dockerfile` (instala el `requirements.txt` raíz + su propio
  `orchestrator_api/requirements.txt` con `fastapi`/`uvicorn` — únicas librerías nuevas, aisladas del resto)
- Servicio en `docker-compose.yml`: `orchestrator-api`, puerto `127.0.0.1:8080` (solo localhost, sin auth en v1)

### Endpoints

| Método | Ruta | Qué hace |
|---|---|---|
| `GET` | `/health` | liveness check |
| `POST` | `/runs` | dispara una corrida — body `{"suite": "admin"\|"desarrollo"\|"unit"}` |
| `GET` | `/runs` | últimas corridas conocidas en memoria (máx. 50) |
| `GET` | `/runs/compare?run_a=&run_b=` | compara los fallos de dos corridas por `(archivo, test, TIPO_ERROR)`: `shared_failures` (mismo bug en ambas), `unique_to_a`, `unique_to_b` |
| `GET` | `/runs/{run_id}` | estado/timestamps/exit_code (requiere que la corrida siga en memoria) |
| `GET` | `/runs/{run_id}/report` | HTML self-contained archivado (basado en disco, sobrevive a un reinicio) |
| `GET` | `/runs/{run_id}/logs` | stdout/stderr de esa corrida (disco) |
| `GET` | `/runs/{run_id}/resumen` | el `resumen_ia.txt` archivado de esa corrida (disco) — el mismo texto que se le manda a `ia-historias` |
| `DELETE` | `/runs/{run_id}` | borra todos los artefactos de esa corrida (`reports/runs/{run_id}/` completo) + su registro en memoria; `409` si la corrida sigue `queued`/`running` |
| `DELETE` | `/runs?suite=&status=` | borrado masivo con filtros opcionales; sin filtros borra todo lo que no esté activo |

### Diseño y por qué

- **Mapeo de suites** (evita el bug de colisión de colección):
  ```python
  SUITE_MAP = {
      "admin":      "tests/tests_intranet/test_usu_admin",
      "desarrollo": "tests/tests_intranet/test_usu_desarrollo",
      "unit":       "tests/test_utili_errores.py",
  }
  ```
- **Un solo worker, cola FIFO** (`asyncio.Queue` + una tarea consumidora en el `lifespan` de FastAPI): nunca corren dos `pytest` a la vez, porque `reset_logger` borra rutas compartidas fijas (`reports/screen/`, `descargas/`) al inicio de cada sesión — correr en paralelo las corrompería.
- **Archivado por corrida**: al terminar cada subproceso de pytest, se copian `ejecucion.log`, `resumen_ia.txt` y `reports/screen/*` a `reports/runs/{run_id}/` **antes** de que arranque la siguiente corrida encolada (por eso nunca se pisan entre `admin` y `desarrollo`).
- **Verificación del grid antes de correr**: hace poll a `http://selenium-chrome:4444/wd/hub/status` (hasta 60s) antes de lanzar pytest, porque `depends_on` en compose solo espera a que el contenedor arranque, no a que el grid esté listo.
- **Timeout y shutdown**: cada corrida tiene un timeout (~45 min, con margen para el hilo no-daemon de `notificar_ia.py`); si el contenedor recibe `SIGTERM`, el subproceso en curso se termina explícitamente en vez de dejar que Docker lo mate a la fuerza. En ambos casos (timeout o shutdown) se llama además a `_kill_active_grid_sessions()` para cerrar cualquier sesión de Chrome que haya quedado abierta en `selenium-chrome`.
- **`GET`/`DELETE` basados en disco, no solo en memoria**: `report`, `logs`, `resumen` y `compare` funcionan aunque el contenedor se haya reiniciado (el registro en memoria se pierde, los archivos en `reports/runs/` no). Solo `GET /runs` y `GET /runs/{run_id}` (el JSON de estado) dependen de memoria, porque esos datos nunca se persistieron a disco.

### Limitaciones conocidas (v1, no resueltas a propósito)

- Sin autenticación — mitigado solo con bind a `127.0.0.1`.
- Sin persistencia del historial de corridas más allá de memoria (se pierde al reiniciar el contenedor; los archivos en disco quedan huérfanos pero siguen siendo consultables/borrables por `run_id`).
- ~~Matar una corrida por timeout no cierra la sesión de Chrome remota en `selenium-chrome`~~ — **resuelto 2026-09-01**: `_kill_active_grid_sessions()` en `runner.py` consulta `GET /wd/hub/status` y hace `DELETE /wd/hub/session/{id}` sobre cualquier sesión activa justo después de matar el subproceso de pytest (por timeout de 45 min o por `stop()` del servicio), liberando el slot del grid de inmediato en vez de esperar los ~5 min de `sessionTimeout`. Verificado en vivo contra el grid real.
- No hay `"all"` (correr las tres suites de una sola llamada) — se decidió deliberadamente para evitar el riesgo de archivado incorrecto entre suites dentro de una misma corrida compuesta. Un caller puede lograr lo mismo con tres `POST /runs` seguidos.
- No hay borrado automático por antigüedad (tipo cron/retención) — el borrado siempre es una llamada explícita (`DELETE /runs/{id}` o `DELETE /runs`).
- El reporte histórico agregado (comparar tendencias entre muchas corridas a través del tiempo) se hace en **otra plataforma externa**, no aquí — este servicio solo expone los datos crudos por corrida.
- **No se separó** `test-executor` del `orchestrator-api` en contenedores distintos (decisión explícita del usuario 2026-08-28): un mismo contenedor recibe la petición HTTP y ejecuta pytest directamente.

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

- `tests/tests_intranet/{test_usu_admin,test_usu_desarrollo}/test_06_proyectos.py`: flujo de proyectos con ver, editar, volver y nuevo proyecto.
- `tests/tests_intranet/{test_usu_admin,test_usu_desarrollo}/test_07_servidores.py`: flujo de servidores con inventario y detalle de servidor.
- `tests/tests_intranet/{test_usu_admin,test_usu_desarrollo}/test_08_organigrama.py`: flujo de organigrama con opciones Completo, Áreas, Líderes y Mi Área. **Deshabilitado 2026-09-02** en ambas suites: `test_organigrama_flujo` llama a `click_sidebar_menu_item()` sin los argumentos obligatorios `texto_hijo`/`xpath_hijo_respaldo` (bug del test, `TypeError` garantizado) — comentado con nota hasta corregir la firma de las llamadas y reactivarlo. Ya estaba deshabilitado en `test_usu_desarrollo` desde el 2026-08-31; el 2026-09-02 se aplicó el mismo tratamiento a `test_usu_admin`, que seguía activo y roto.

## `time.sleep` fuera de `utili/waits.py` (fix 2026-09-02)

Quedaban algunos `time.sleep` sueltos en `test_usu_admin/test_03_horarios.py` y `test_usu_admin/test_05_inventario.py`
(las copias equivalentes en `test_usu_desarrollo` ya estaban deshabilitadas, ver abajo). Tratamiento aplicado:

- `test_05_inventario.py::test_inventario_crear_articulo_flow`: el `scrollIntoView` + `time.sleep(0.4)` + `.click()`
  manual se reemplazó por `click_when_clickable()` (ya maneja ese mismo patrón internamente).
- `test_03_horarios.py::test_estado_horario`: el `time.sleep(0.5)` antes del clic se reemplazó por una espera
  explícita (`WebDriverWait` sobre `is_displayed()`/`is_enabled()` del elemento ya encontrado); el `time.sleep(5)`
  fijo tras el clic se reemplazó por un poll acotado a 5s sobre `os.listdir()` que corta en cuanto aparece el
  archivo, en vez de esperar siempre el máximo.
- El `time.sleep(0.5)` restante (tras `window.scrollBy` dentro del loop de reintento) se dejó intacto a propósito:
  es una pausa de estabilización sin una condición de DOM que esperar (el propio loop existe porque el elemento
  todavía no se encuentra), documentado con un comentario en el código.

## Tests deshabilitados (usuario desarrollo, pendientes de revisión)

Fallas específicas del rol desarrollo (no reproducen con el usuario admin), detectadas el 2026-08-31:

- `test_02_novedades.py::test_btones_novedades` — `TIEMPO_ESPERA` al abrir el PDF de la tercera novedad.
- `test_03_horarios.py::test_estado_horario` — `ERROR_HTTP` 403 Forbidden en `/horarios/exportar`. **Nota 2026-09-02**: el comentario "Deshabilitado" existía desde el 31-ago pero el test había quedado activo por error (nunca se comentó la función) — corregido para que el código coincida con la etiqueta.
- `test_03_horarios.py::test_solicitud_cambios` — `ALERT_INESPERADO` por un warning de DataTables en la tabla de solicitudes (bug de la app, no del test).
- `test_04_horas_extra.py::test_ver_horas_extra` y `test_btones_horas_extra` — `TIEMPO_ESPERA` en los botones "Registrar"/"previsualizar horas extra".
- `test_05_inventario.py::test_inventario_crear_articulo_flow` — `ERROR_PERMISOS` (500 Internal Server Error) al enviar el formulario de nuevo artículo.
- `test_08_organigrama.py::test_organigrama_flujo` — ver arriba (bug del test, también deshabilitado en `test_usu_admin`).

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

Si quieres que aplique estas convenciones a todos los tests existentes (mover XPATHs y reemplazar llamadas), lo hago por lotes empezando por los tests que más fallan. ¿Por cuál empiezo? (recomiendo `test_01_login.py` y `test_04_horas_extra.py` de `tests/tests_intranet/test_usu_admin/`).

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

