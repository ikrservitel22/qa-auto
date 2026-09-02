# Graph Report - qa-auto  (2026-09-02)

## Corpus Check
- 4 files · ~16,741 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 270 nodes · 515 edges · 43 communities (19 shown, 24 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 17 edges (avg confidence: 0.88)
- Token cost: 69,690 input · 0 output

## Community Hubs (Navigation)
- Admin Suite: Login/Novedades/Horas Extra + Grid Timeout Report
- Orchestrator API Models & Analyzer
- Unit Tests: utili/errores.py
- Sep-2026 Fixes: Credentials, Config, Chrome Pin, Drift
- Orchestrator API Runner (Queue & Grid)
- Error-Page Detection in Waits + .gitignore
- Shared tests_intranet/conftest.py (2026-09-02 merge)
- Admin Suite: Horarios
- docker-compose Services & Network
- Desarrollo Suite: Inventario
- orchestrator_api/requirements.txt
- Desarrollo Suite: Novedades
- Desarrollo Suite: Horas Extra
- notificar_ia.py
- Report Environment Metadata
- Admin Suite: Proyectos
- Admin Suite: Servidores
- Desarrollo Suite: Proyectos
- Desarrollo Suite: Servidores
- screenshot_full.py
- Exception (isolated)
- Convención: usar waits en vez de sleep
- Convención: imports consistentes
- Instrucciones del Proyecto (título)
- Convención: XPATHs centralizados
- Convención: manejo de errores en tests
- Plantilla recomendada para tests
- Reglas de modificación de código
- pytest-html==4.2.0
- requests==2.34.2
- selenium==4.47.0
- vncdotool==1.3.0
- webdriver-manager==4.1.2
- pytest dependency marker
- pytest dependency marker
- pytest dependency marker

## God Nodes (most connected - your core abstractions)
1. `manejar_error_test()` - 27 edges
2. `wait_visible_xpath()` - 14 edges
3. `DriverFalso` - 13 edges
4. `click_when_clickable()` - 13 edges
5. `RunRecord` - 12 edges
6. `es_pagina_error_servidor()` - 12 edges
7. `click_por_texto_o_xpath()` - 11 edges
8. `_esperar_con_deteccion_de_error()` - 10 edges
9. `send_keys_when_visible()` - 9 edges
10. `tipificar_error()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `test_login run result — Error (Selenium grid session timeout)` --references--> `test_login()`  [EXTRACTED]
  reports/html/reporte.html → tests/tests_intranet/test_usu_admin/test_01_login.py
- `test_logout run result — Error (Selenium grid session timeout)` --references--> `test_logout()`  [EXTRACTED]
  reports/html/reporte.html → tests/tests_intranet/test_usu_admin/test_01_login.py
- `test_login run result — Error (Selenium grid session timeout)` --references--> `__init__.py fix (2026-08-28) for unique pytest module names`  [AMBIGUOUS]
  reports/html/reporte.html → contexto-proyecto.md
- `test_manejar_error_test_captura_texto_de_alerta()` --calls--> `manejar_error_test()`  [EXTRACTED]
  tests/test_utili_errores.py → utili/errores.py
- `test_manejar_error_test_caso_normal_selenium()` --calls--> `manejar_error_test()`  [EXTRACTED]
  tests/test_utili_errores.py → utili/errores.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **2026-09-02 cleanup fixes batch** — contexto_proyecto_conftest_merge_fix, contexto_proyecto_gitignore_reporte_fix, contexto_proyecto_time_sleep_cleanup_fix, contexto_proyecto_organigrama_disable_fix [INFERRED 0.85]
- **Role-based credential resolution flow** — contexto_proyecto_credentials_json, contexto_proyecto_credentials_split, contexto_proyecto_config_py, contexto_proyecto_driver_logueado, contexto_proyecto_role_resolution_fspath [EXTRACTED 1.00]
- **Selenium grid orphaned-session prevention pattern** — contexto_proyecto_driver_session_leak_fix, contexto_proyecto_kill_active_grid_sessions, contexto_proyecto_runner_py [INFERRED 0.80]
- **Services sharing the repo workspace bind mount** — docker_compose_qa_dev, docker_compose_chrome, docker_compose_orchestrator_api [EXTRACTED 1.00]
- **Reported grid session timeout, its likely root cause, and its mitigation mechanism** — reports_html_reporte_test_login, contexto_proyecto_kill_active_grid_sessions [INFERRED 0.75]

## Communities (43 total, 24 thin omitted)

### Community 0 - "Admin Suite: Login/Novedades/Horas Extra + Grid Timeout Report"
Cohesion: 0.13
Nodes (35): test_logout run result — Error (Selenium grid session timeout), dependency, test_login(), test_logout(), dependency, test_login(), test_logout(), dependency (+27 more)

### Community 1 - "Orchestrator API Models & Analyzer"
Cohesion: 0.11
Nodes (31): BaseModel, delete, Enum, FastAPI, get, compare_runs(), _parse_resumen_ia(), _signature() (+23 more)

### Community 2 - "Unit Tests: utili/errores.py"
Cohesion: 0.07
Nodes (30): parametrize, AlertaFalsa, DriverFalso, ElementoFalso, NoAlertPresentExceptionLocal, Exception, Tests unitarios para utili/errores.py. A diferencia de los tests en…, Un TimeoutException común, página normal (sin señales de error real). (+22 more)

### Community 3 - "Sep-2026 Fixes: Credentials, Config, Chrome Pin, Drift"
Cohesion: 0.09
Nodes (29): Chrome image pin by digest (fix 2026-09-01), utili/config.py, Conftest merge fix (2026-09-02): unify duplicated conftests, utili/credentials.json, Credentials split into admin/desarrollo blocks (fix 2026-09-02, admin block still a placeholder), Dependency drift fix (2026-09-01): qa-dev vs orchestrator-api version mismatch, docker-compose.yml, driver fixture (+21 more)

### Community 4 - "Orchestrator API Runner (Queue & Grid)"
Cohesion: 0.18
Nodes (9): _active_grid_session_ids(), _archive_fixed_artifacts(), _grid_ready(), _kill_active_grid_sessions(), _now(), RunQueue, _status_from_exit_code(), RunStatus (+1 more)

### Community 5 - "Error-Page Detection in Waits + .gitignore"
Cohesion: 0.18
Nodes (13): click_when_clickable() helper, ErrorPaginaServidorDetectado exception, utili/errores.py, es_pagina_error_servidor() function, _esperar_con_deteccion_de_error() helper, .gitignore, .gitignore fix (2026-09-02): untrack reporte.html with git rm --cached, HTTP_STATUS_REASONS catalog (+5 more)

### Community 6 - "Shared tests_intranet/conftest.py (2026-09-02 merge)"
Cohesion: 0.19
Nodes (9): fixture, hookimpl, _credenciales_por_rol(), driver(), driver_logueado(), pytest_runtest_makereport(), test_usu_admin/ y test_usu_desarrollo/ comparten este conftest.py; se determina…, # IMPORTANT: you must bind-mount the host `host_download_dir` to this container… (+1 more)

### Community 7 - "Admin Suite: Horarios"
Cohesion: 0.38
Nodes (4): dependency, test_estado_horario(), test_horarios(), test_solicitud_cambios()

### Community 8 - "docker-compose Services & Network"
Cohesion: 0.83
Nodes (4): chrome / selenium-chrome service (docker-compose.yml), orchestrator-api service (docker-compose.yml), qa-dev service (docker-compose.yml), qa-net external network

### Community 9 - "Desarrollo Suite: Inventario"
Cohesion: 0.50
Nodes (4): dependency, Flujo separado: crear un artículo nuevo desde el dashboard de inventario., test_inventario_crear_articulo_flow(), test_inventario_todos_y_nuevo_articulo()

### Community 11 - "Desarrollo Suite: Novedades"
Cohesion: 0.67
Nodes (3): dependency, test_btones_novedades(), test_btt_crear_novedad()

### Community 12 - "Desarrollo Suite: Horas Extra"
Cohesion: 0.67
Nodes (3): dependency, test_btones_horas_extra(), test_ver_horas_extra()

## Ambiguous Edges - Review These
- `test_login run result — Error (Selenium grid session timeout)` → `__init__.py fix (2026-08-28) for unique pytest module names`  [AMBIGUOUS]
  reports/html/reporte.html · relation: references

## Knowledge Gaps
- **17 isolated node(s):** `fastapi==0.115.0`, `uvicorn[standard]==0.30.6`, `Instrucciones del Proyecto: Suite de Automatización QA`, `Ejecución típica (docker-compose + orchestrator-api)`, `test_logout run result — Error (Selenium grid session timeout)` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `test_login run result — Error (Selenium grid session timeout)` and `__init__.py fix (2026-08-28) for unique pytest module names`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `test_login()` connect `Admin Suite: Login/Novedades/Horas Extra + Grid Timeout Report` to `Sep-2026 Fixes: Credentials, Config, Chrome Pin, Drift`?**
  _High betweenness centrality (0.162) - this node is a cross-community bridge._
- **Why does `test_login run result — Error (Selenium grid session timeout)` connect `Sep-2026 Fixes: Credentials, Config, Chrome Pin, Drift` to `Admin Suite: Login/Novedades/Horas Extra + Grid Timeout Report`?**
  _High betweenness centrality (0.160) - this node is a cross-community bridge._
- **Why does `manejar_error_test()` connect `Admin Suite: Login/Novedades/Horas Extra + Grid Timeout Report` to `Unit Tests: utili/errores.py`?**
  _High betweenness centrality (0.112) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `RunRecord` (e.g. with `get_run()` and `list_runs()`) actually correct?**
  _`RunRecord` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `fastapi==0.115.0`, `uvicorn[standard]==0.30.6`, `Instrucciones del Proyecto: Suite de Automatización QA` to the rest of the system?**
  _17 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Admin Suite: Login/Novedades/Horas Extra + Grid Timeout Report` be split into smaller, more focused modules?**
  _Cohesion score 0.1305194805194805 - nodes in this community are weakly interconnected._