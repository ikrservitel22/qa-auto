# Graph Report - qa-auto  (2026-08-28)

## Corpus Check
- 35 files · ~17,641 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 269 nodes · 433 edges · 28 communities (19 shown, 9 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 25 edges (avg confidence: 0.92)
- Token cost: 0 input · 79,099 output

## Community Hubs (Navigation)
- Flujos E2E Suite Admin
- Endpoints orchestrator-api
- Diseño y Migración orchestrator-api
- Unit Tests errores.py
- Motor de Ejecución (runner.py)
- Tests de Horarios
- Fixtures conftest Admin
- Tests de Login
- Fixtures conftest Desarrollo
- Helpers de Clasificación de Errores
- Helpers de Navegación (waits)
- Metadata del Reporte HTML
- Plantilla de Tests Nuevos
- Reglas de Modificación de Código
- Resumen del Proyecto
- Convención de Manejo de Errores
- Convención de Localizadores
- Convención de Waits
- Configuración y Credenciales
- Descargas con Cookies
- Convención de Imports

## God Nodes (most connected - your core abstractions)
1. `Microservicio orchestrator-api` - 16 edges
2. `DriverFalso` - 13 edges
3. `RunRecord` - 12 edges
4. `RunQueue` - 10 edges
5. `RunStatus` - 9 edges
6. `Suite` - 8 edges
7. `RunStore` - 8 edges
8. `requirements.txt (raíz)` - 8 edges
9. `compare_runs()` - 7 edges
10. `CompareResult` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Localización y centralización de XPATHs en utili/locators.py` --conceptually_related_to--> `utili/locators.py: localizadores centralizados`  [INFERRED]
  .github/instructions/proyecto-automacion-qa.instructions.md → contexto-proyecto.md
- `Uso de waits en lugar de time.sleep` --conceptually_related_to--> `utili/waits.py: helpers de espera`  [INFERRED]
  .github/instructions/proyecto-automacion-qa.instructions.md → contexto-proyecto.md
- `Manejo de errores en tests (try/except + tipificar_error)` --conceptually_related_to--> `utili/errores.py: tipificación de errores Selenium`  [INFERRED]
  .github/instructions/proyecto-automacion-qa.instructions.md → contexto-proyecto.md
- `Plantilla recomendada para tests nuevos` --conceptually_related_to--> `Plantilla recomendada para tests nuevos (contexto-proyecto.md)`  [INFERRED]
  .github/instructions/proyecto-automacion-qa.instructions.md → contexto-proyecto.md
- `Restricciones estrictas de modificación de código` --conceptually_related_to--> `Reglas para cambios de código / Qué NO hacer`  [INFERRED]
  .github/instructions/proyecto-automacion-qa.instructions.md → contexto-proyecto.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Módulos utili/ como capa de utilidades centralizada** — contexto_proyecto_utili_errores, contexto_proyecto_utili_waits, contexto_proyecto_utili_locators, contexto_proyecto_utili_config, contexto_proyecto_utili_downloads, contexto_proyecto_utili_notificar_ia [INFERRED 0.85]
- **Ciclo de vida de una corrida vía orchestrator-api** — contexto_proyecto_orchestrator_api, contexto_proyecto_suite_map, contexto_proyecto_cola_fifo_worker, contexto_proyecto_archivado_por_corrida, contexto_proyecto_verificacion_grid_selenium, contexto_proyecto_timeout_shutdown [INFERRED 0.85]
- **Topología de servicios Docker Compose** — docker_compose_qa_dev, docker_compose_chrome, docker_compose_orchestrator_api, docker_compose_qa_net_network [EXTRACTED 1.00]

## Communities (28 total, 9 thin omitted)

### Community 0 - "Flujos E2E Suite Admin"
Cohesion: 0.06
Nodes (38): dependency, test_btones_novedades(), test_btt_crear_novedad(), dependency, test_btones_horas_extra(), test_ver_horas_extra(), dependency, Flujo separado: crear un artículo nuevo desde el dashboard de inventario. (+30 more)

### Community 1 - "Endpoints orchestrator-api"
Cohesion: 0.12
Nodes (27): BaseModel, delete, FastAPI, get, compare_runs(), _parse_resumen_ia(), _signature(), create_run() (+19 more)

### Community 2 - "Diseño y Migración orchestrator-api"
Cohesion: 0.07
Nodes (35): Archivado de artefactos por corrida (reports/runs/{run_id}), Migración hacia arquitectura de microservicios (2026-08-28), Cola FIFO de un solo worker (asyncio.Queue), Fixtures conftest.py: driver, driver_logueado, reset_logger, Servicio externo ia-historias, Proyecto hermano ia-usuario, Fix __init__.py para nombres de módulo únicos (2026-08-28), Limitaciones conocidas v1 de orchestrator-api (+27 more)

### Community 3 - "Unit Tests errores.py"
Cohesion: 0.09
Nodes (22): parametrize, AlertaFalsa, DriverFalso, ElementoFalso, Tests unitarios para utili/errores.py. A diferencia de los tests en…, Un TimeoutException común, página normal (sin señales de error real)., Aunque Selenium haya lanzado un TimeoutException genérico, si la página muestra…, La prueba más importante de todas: si el driver falso está configurado para… (+14 more)

### Community 4 - "Motor de Ejecución (runner.py)"
Cohesion: 0.21
Nodes (9): Enum, RunStatus, Suite, _archive_fixed_artifacts(), _grid_ready(), _now(), RunQueue, _status_from_exit_code() (+1 more)

### Community 5 - "Tests de Horarios"
Cohesion: 0.17
Nodes (11): Exception, NoAlertPresentExceptionLocal, Sustituto simple: no importa la excepción exacta, solo que algo se lance cuando…, dependency, test_estado_horario(), test_horarios(), test_solicitud_cambios(), dependency (+3 more)

### Community 6 - "Fixtures conftest Admin"
Cohesion: 0.22
Nodes (7): driver(), driver_logueado(), fixture, hookimpl, pytest_runtest_makereport(), # IMPORTANT: you must bind-mount the host `host_download_dir` to this container…, reset_logger()

### Community 7 - "Tests de Login"
Cohesion: 0.22
Nodes (8): dependency, test_login(), test_logout(), dependency, test_login(), test_logout(), capturar_pantalla_completa(), Captura la pantalla COMPLETA del contenedor Chrome vía VNC, incluyendo diálogos…

### Community 8 - "Fixtures conftest Desarrollo"
Cohesion: 0.22
Nodes (7): driver(), driver_logueado(), fixture, hookimpl, pytest_runtest_makereport(), # IMPORTANT: you must bind-mount the host `host_download_dir` to this container…, reset_logger()

### Community 9 - "Helpers de Clasificación de Errores"
Cohesion: 0.25
Nodes (8): es_pagina_error_servidor(), guardar_texto_pagina_error(), manejar_error_test(), Detecta si la página actual es una pantalla de error real (del framework/app,…, Manejo estándar de errores para todos los tests: - Detecta y cierra alertas…, Clasifica una excepción de Python/Selenium en una categoría legible. El orden…, Extrae todo el texto visible de la página actual y lo guarda en un .txt. Útil…, tipificar_error()

### Community 10 - "Helpers de Navegación (waits)"
Cohesion: 0.50
Nodes (4): click_por_texto_o_xpath(), click_sidebar_menu_item(), Busca un <button> o <a> cuyo texto visible contenga el texto indicado (sin…, Abre un grupo del menú lateral (solo si no está ya abierto) y hace clic en el…

### Community 11 - "Metadata del Reporte HTML"
Cohesion: 0.67
Nodes (3): reporte.html (Reporte de Automatización — Servitel Intranet), Entorno de ejecución del reporte (Python 3.12.14, pytest 9.1.1, pytest-html 4.2.0), Servitel Intranet (aplicación bajo prueba)

## Knowledge Gaps
- **20 isolated node(s):** `Servitel Intranet (aplicación bajo prueba)`, `Entorno de ejecución del reporte (Python 3.12.14, pytest 9.1.1, pytest-html 4.2.0)`, `Instrucciones del Proyecto: Suite de Automatización QA`, `Ejecución típica (docker-compose + orchestrator-api)`, `Resumen general del proyecto QA Automation` (+15 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Are the 3 inferred relationships involving `RunRecord` (e.g. with `get_run()` and `list_runs()`) actually correct?**
  _`RunRecord` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `RunQueue` (e.g. with `RunStatus` and `Suite`) actually correct?**
  _`RunQueue` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `RunStatus` (e.g. with `create_run()` and `delete_runs()`) actually correct?**
  _`RunStatus` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Servitel Intranet (aplicación bajo prueba)`, `Entorno de ejecución del reporte (Python 3.12.14, pytest 9.1.1, pytest-html 4.2.0)`, `Instrucciones del Proyecto: Suite de Automatización QA` to the rest of the system?**
  _20 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Flujos E2E Suite Admin` be split into smaller, more focused modules?**
  _Cohesion score 0.06284153005464481 - nodes in this community are weakly interconnected._
- **Should `Endpoints orchestrator-api` be split into smaller, more focused modules?**
  _Cohesion score 0.11861861861861862 - nodes in this community are weakly interconnected._
- **Should `Diseño y Migración orchestrator-api` be split into smaller, more focused modules?**
  _Cohesion score 0.06984126984126984 - nodes in this community are weakly interconnected._