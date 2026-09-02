# Graph Report - qa-auto  (2026-09-02)

## Corpus Check
- 19 files · ~21,305 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 263 nodes · 526 edges · 41 communities (20 shown, 21 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 20 edges (avg confidence: 0.89)
- Token cost: 91,406 input · 0 output

## Community Hubs (Navigation)
- Admin Suite: Login/Novedades/Horas Extra
- Unit Tests: utili/errores.py
- Orchestrator API Models & Analyzer
- Orchestrator API Design Rationale
- Orchestrator API Runner (Queue & Grid)
- Dependency Pinning & Version Drift Fixes
- Admin conftest Fixtures
- Desarrollo conftest Fixtures
- Admin Suite: Horarios
- Error-Page Detection in Waits
- Desarrollo Suite: Inventario
- orchestrator_api/requirements.txt
- Desarrollo Suite: Novedades
- Desarrollo Suite: Horas Extra
- notificar_ia.py
- Admin/Desarrollo Credentials Split
- Disabled Tests: Organigrama Bug
- Admin Suite: Proyectos
- Admin Suite: Servidores
- Desarrollo Suite: Proyectos
- Desarrollo Suite: Servidores
- screenshot_full.py
- HTTP_STATUS_REASONS Catalog Fix
- ia-historias External Service
- Convención: usar waits en vez de sleep
- Convención: imports consistentes
- Instrucciones del Proyecto (título)
- Convención: XPATHs centralizados
- Convención: manejo de errores en tests
- Plantilla recomendada para tests
- Reglas de modificación de código
- pytest dependency marker
- pytest dependency marker
- pytest dependency marker

## God Nodes (most connected - your core abstractions)
1. `manejar_error_test()` - 27 edges
2. `es_pagina_error_servidor()` - 17 edges
3. `wait_visible_xpath()` - 14 edges
4. `DriverFalso` - 13 edges
5. `tipificar_error()` - 13 edges
6. `click_when_clickable()` - 13 edges
7. `RunRecord` - 12 edges
8. `guardar_texto_pagina_error()` - 11 edges
9. `_esperar_con_deteccion_de_error()` - 11 edges
10. `click_por_texto_o_xpath()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `test_logout run result — Error (Selenium grid session timeout)` --references--> `test_logout()`  [EXTRACTED]
  reports/html/reporte.html → tests/tests_intranet/test_usu_admin/test_01_login.py
- `es_pagina_error_servidor() page-content-based error reclassification` --rationale_for--> `es_pagina_error_servidor()`  [EXTRACTED]
  contexto-proyecto.md → utili/errores.py
- `test_organigrama_flujo disabled — missing required click_sidebar_menu_item args` --references--> `click_sidebar_menu_item()`  [EXTRACTED]
  contexto-proyecto.md → utili/waits.py
- `test_login run result — Error (Selenium grid session timeout)` --references--> `__init__.py fix for pytest module name collision (2026-08-28)`  [AMBIGUOUS]
  reports/html/reporte.html → contexto-proyecto.md
- `test_login run result — Error (Selenium grid session timeout)` --references--> `test_login()`  [EXTRACTED]
  reports/html/reporte.html → tests/tests_intranet/test_usu_admin/test_01_login.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **orchestrator-api reliability/design mechanisms (queue, mapping, archiving, grid checks, cleanup)** — contexto_proyecto_suite_map, contexto_proyecto_fifo_queue, contexto_proyecto_archivado_por_corrida, contexto_proyecto_grid_verification, contexto_proyecto_kill_active_grid_sessions [INFERRED 0.85]
- **Services sharing the repo workspace bind mount** — docker_compose_qa_dev, docker_compose_chrome, docker_compose_orchestrator_api [EXTRACTED 1.00]
- **Reported grid session timeout, its likely root cause, and its mitigation mechanism** — reports_html_reporte_test_login, contexto_proyecto_driver_fixture_orphan_fix, contexto_proyecto_kill_active_grid_sessions [INFERRED 0.75]

## Communities (41 total, 21 thin omitted)

### Community 0 - "Admin Suite: Login/Novedades/Horas Extra"
Cohesion: 0.15
Nodes (29): dependency, test_login(), test_logout(), dependency, test_login(), test_logout(), dependency, test_btt_crear_novedad() (+21 more)

### Community 1 - "Unit Tests: utili/errores.py"
Cohesion: 0.06
Nodes (36): parametrize, AlertaFalsa, DriverFalso, ElementoFalso, NoAlertPresentExceptionLocal, Exception, Tests unitarios para utili/errores.py. A diferencia de los tests en…, Un TimeoutException común, página normal (sin señales de error real). (+28 more)

### Community 2 - "Orchestrator API Models & Analyzer"
Cohesion: 0.11
Nodes (31): BaseModel, delete, Enum, FastAPI, get, compare_runs(), _parse_resumen_ia(), _signature() (+23 more)

### Community 3 - "Orchestrator API Design Rationale"
Cohesion: 0.13
Nodes (20): Per-run artifact archiving to reports/runs/{run_id}, Chrome image pinned by digest to match selenium==4.47.0 (fix 2026-09-01), chrome / selenium-chrome Selenium Grid service, driver fixture try/except orphan-session fix (2026-09-01), orchestrator-api HTTP endpoints (health, runs, compare, report, logs, resumen, delete), Single-worker FIFO queue for pytest runs, Selenium grid readiness poll before launching pytest, _kill_active_grid_sessions() cleanup on timeout/shutdown (+12 more)

### Community 4 - "Orchestrator API Runner (Queue & Grid)"
Cohesion: 0.18
Nodes (9): _active_grid_session_ids(), _archive_fixed_artifacts(), _grid_ready(), _kill_active_grid_sessions(), _now(), RunQueue, _status_from_exit_code(), RunStatus (+1 more)

### Community 5 - "Dependency Pinning & Version Drift Fixes"
Cohesion: 0.22
Nodes (10): Dependencias principales (documented root requirements list), qa-dev/orchestrator-api pytest+selenium version drift resolution (2026-09-01), __init__.py fix for pytest module name collision (2026-08-28), Report environment metadata (Python 3.12.14, pytest 9.1.1, pluggy 1.6.0), pytest==9.1.1, pytest-html==4.2.0, requests==2.34.2, selenium==4.47.0 (+2 more)

### Community 6 - "Admin conftest Fixtures"
Cohesion: 0.28
Nodes (5): driver(), driver_logueado(), fixture, # IMPORTANT: you must bind-mount the host `host_download_dir` to this container…, reset_logger()

### Community 7 - "Desarrollo conftest Fixtures"
Cohesion: 0.28
Nodes (5): driver(), driver_logueado(), fixture, # IMPORTANT: you must bind-mount the host `host_download_dir` to this container…, reset_logger()

### Community 8 - "Admin Suite: Horarios"
Cohesion: 0.32
Nodes (5): Exception, dependency, test_estado_horario(), test_horarios(), test_solicitud_cambios()

### Community 9 - "Error-Page Detection in Waits"
Cohesion: 0.40
Nodes (5): es_pagina_error_servidor() page-content-based error reclassification, _esperar_con_deteccion_de_error() early error-page detection in waits (fix 2026-09-01), ErrorPaginaServidorDetectado, Exception, La lanzan los helpers de espera de `utili/waits.py` cuando, mientras se espera…

### Community 10 - "Desarrollo Suite: Inventario"
Cohesion: 0.50
Nodes (4): dependency, Flujo separado: crear un artículo nuevo desde el dashboard de inventario., test_inventario_crear_articulo_flow(), test_inventario_todos_y_nuevo_articulo()

### Community 12 - "Desarrollo Suite: Novedades"
Cohesion: 0.67
Nodes (3): dependency, test_btones_novedades(), test_btt_crear_novedad()

### Community 13 - "Desarrollo Suite: Horas Extra"
Cohesion: 0.67
Nodes (3): dependency, test_btones_horas_extra(), test_ver_horas_extra()

## Ambiguous Edges - Review These
- `__init__.py fix for pytest module name collision (2026-08-28)` → `test_login run result — Error (Selenium grid session timeout)`  [AMBIGUOUS]
  reports/html/reporte.html · relation: references

## Knowledge Gaps
- **13 isolated node(s):** `Instrucciones del Proyecto: Suite de Automatización QA`, `fastapi==0.115.0`, `uvicorn[standard]==0.30.6`, `Ejecución típica (docker-compose + orchestrator-api)`, `qa-dev container` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `__init__.py fix for pytest module name collision (2026-08-28)` and `test_login run result — Error (Selenium grid session timeout)`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `test_login()` connect `Admin Suite: Login/Novedades/Horas Extra` to `Orchestrator API Design Rationale`, `Admin conftest Fixtures`?**
  _High betweenness centrality (0.127) - this node is a cross-community bridge._
- **Why does `test_login run result — Error (Selenium grid session timeout)` connect `Orchestrator API Design Rationale` to `Admin Suite: Login/Novedades/Horas Extra`, `Dependency Pinning & Version Drift Fixes`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Why does `manejar_error_test()` connect `Admin Suite: Login/Novedades/Horas Extra` to `Unit Tests: utili/errores.py`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **What connects `Instrucciones del Proyecto: Suite de Automatización QA`, `fastapi==0.115.0`, `uvicorn[standard]==0.30.6` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Unit Tests: utili/errores.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06464646464646465 - nodes in this community are weakly interconnected._
- **Should `Orchestrator API Models & Analyzer` be split into smaller, more focused modules?**
  _Cohesion score 0.11097560975609756 - nodes in this community are weakly interconnected._