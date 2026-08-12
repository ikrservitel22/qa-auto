---
name: proyecto-automacion-qa
description: "Use when: working on this Selenium/pytest test automation project. Always reference contexto-proyecto.md for project context, conventions, and best practices. Update contexto-proyecto.md when significant changes occur."
applyTo: "**/*.py"
---

# Instrucciones del Proyecto: Suite de Automatización QA

## Referencia de Contexto

**Antes de cualquier cambio**: Consulta `/workspace/contexto-proyecto.md` para:
- Estructura de carpetas y archivos del proyecto
- Dependencias y versiones exactas
- Rutas importantes (tests, localizadores, logs, reportes)
- Convenciones de código y buenas prácticas
- Templetas recomendadas para tests nuevos

**Actualiza `contexto-proyecto.md`** cuando:
- Agregues nuevos helpers o funciones reutilizables
- Modifiques la estructura de directorios
- Cambies dependencias en `requirements.txt`
- Agregues nuevos tests con patrones diferentes
- Descubras mejores prácticas o optimizaciones

## Principios de Codificación

### Localización y Centralizacón

1. **XPATHs centralizados en `utili/locators.py`**
   - NUNCA uses XPATHs inline en tests
   - Define constantes con nombres descriptivos: `SIDEBAR_MI_MODULO_BUTTON`, `MENU_MI_MODULO_OPCION`
   - Usa prefijos claros: `SIDEBAR_`, `MENU_`, `MODAL_`, `PAGE_`, etc.

2. **Imports consistentes**
   ```python
   from utili.config import *
   from utili.locators import *
   from utili.logger import logger
   from utili.errores import tipificar_error
   from utili.waits import click_when_clickable, wait_visible_xpath, wait_text_present
   ```

### Helpers y Utilidades

3. **Waits en lugar de `time.sleep`**
   - Siempre usa helpers de `utili/waits.py`:
     - `wait_visible_xpath()` para esperar a que elementos sean visibles
     - `click_when_clickable()` para clics seguros
     - `wait_text_present()` para textos en la página
     - `send_keys_when_visible()` para enviar texto
     - `wait_for_url()` para cambios de URL
   - Proporciona `timeout` cuando el defecto no sea suficiente

4. **Manejo de errores en tests**
   - Envuelve la lógica principal en `try/except`
   - Tipifica el error con `tipificar_error(e)`
   - Registra excepciones con `logger.exception()`
   - Toma captura de pantalla: `driver.save_screenshot(f"reports/screen/nombre_{timestamp}.png")`
   - Siempre relanza con `raise` después de capturar el error

### Estructura de Tests Nuevos

5. **Sigue la plantilla recomendada**:
   ```python
   from datetime import datetime
   from utili.config import *
   from utili.locators import *
   from utili.logger import logger
   from utili.errores import tipificar_error
   from utili.waits import click_when_clickable, wait_visible_xpath, wait_text_present

   def test_mi_nuevo_flujo(driver_logueado):
       try:
           logger.info("========== INICIO test_mi_nuevo_flujo ==========")
           
           # Acciones aquí usando helpers centralizados
           click_when_clickable(driver_logueado, SIDEBAR_MI_MODULO_BUTTON)
           wait_visible_xpath(driver_logueado, MI_MODULO_PAGE_TITLE)
           
           logger.info("========== FIN test_mi_nuevo_flujo ==========")
       except Exception as e:
           tipo_error = tipificar_error(e)
           logger.exception(f"ERROR EN test_mi_nuevo_flujo: {e}")
           logger.info(f"URL al fallar: {driver_logueado.current_url}")
           nombre = datetime.now().strftime("%Y%m%d_%H%M%S")
           driver_logueado.save_screenshot(f"reports/screen/mi_nuevo_flujo_{nombre}.png")
           raise
   ```

## Restricciones Estrictas

❌ **NO HAGAS ESTO**:
- No cambies la estructura de carpetas sin autorización
- No renombres variables, funciones o archivos existentes sin aprobación
- No muevas lógica entre archivos sin autorización
- No agregues librerías nuevas sin autorización
- No modifiques código no solicitado
- **No inventes XPATHs**
- **No inventes nombres de métodos**
- No crees Page Object Model sin solicitud explícita
- No uses `time.sleep` directamente

✅ **HAZ ESTO**:
- Mantén el estilo existente del proyecto
- Reutiliza helpers de `utili/waits.py`
- Centraliza constantes en `utili/locators.py`
- Usa constantes de `utili/config.py` (URL, timeout, rutas)
- Sigue la plantilla de tests recomendada
- Documenta cambios importantes en `contexto-proyecto.md`

## Artefactos y Rutas

- **Logs**: `/workspace/reports/logs/`
- **Capturas**: `/workspace/reports/screen/`
- **Reportes HTML**: `/workspace/reports/html/reporte.html`
- **Descargas**: `/workspace/descargas/`
- **Localizadores**: `/workspace/utili/locators.py`
- **Configuración**: `/workspace/utili/config.py`

## Ejecución Típica

```bash
# Levantar servicios Docker
docker-compose up -d

# Ejecutar tests con reporte HTML
python -m pytest -s tests/ --html=reports/html/reporte.html --self-contained-html
```

## Consulta Primero

Si no estás seguro de:
- Dónde poner un xpath
- Cómo implementar una funcionalidad
- Si algo requiere cambiar la estructura
- Si hay un helper existente para algo

**Consulta `contexto-proyecto.md` y el código existente en `utili/`**. Si aún tienes dudas, pregunta antes de hacer cambios.
