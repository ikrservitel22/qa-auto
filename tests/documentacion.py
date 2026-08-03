import re
from pathlib import Path
from datetime import datetime

LOG_PATH = Path("/workspace/reports/logs/ejecucion.log")
OUTPUT_DIR = Path("/workspace/reports/manual")
OUTPUT_FILE = OUTPUT_DIR / "documentacion_manual.md"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SECTION_DEFINITIONS = {
    "LOGIN": {
        "title": "Ingreso a la aplicación",
        "description": "Describe el flujo de acceso a la aplicación desde la pantalla de inicio de sesión.",
        "steps": [
            "Abra la página de inicio de sesión de la aplicación.",
            "Ingrese su nombre de usuario.",
            "Ingrese su contraseña.",
            "Pulse el botón Ingresar.",
            "Espere a que el dashboard principal se cargue correctamente.",
        ],
        "notes": [
            "Solo usuarios con credenciales válidas pueden acceder.",
            "Si hay un error, verifique su usuario y contraseña.",
        ],
    },
    "LOGOUT": {
        "title": "Cerrar sesión",
        "description": "Explica cómo cerrar sesión correctamente desde el sistema.",
        "steps": [
            "Abra el menú lateral.",
            "Seleccione la opción Cerrar sesión.",
            "Espere a que la aplicación regrese a la pantalla de inicio de sesión.",
        ],
    },
    "BTT_CREAR_NOVEDAD": {
        "title": "Crear una novedad",
        "description": "Describe cómo abrir el formulario para crear una nueva novedad.",
        "steps": [
            "Abra el menú lateral.",
            "Seleccione el módulo Novedades.",
            "Pulse el botón para crear una novedad.",
            "Espere a que aparezca el formulario de creación de novedad.",
        ],
        "notes": [
            "Complete el tipo de novedad, las fechas, horas y descripción antes de guardar.",
            "Revise los datos ingresados antes de enviar el formulario.",
        ],
    },
    "BTONES_NOVEDADES": {
        "title": "Ver y revisar novedades",
        "description": "Describe cómo revisar novedades registradas y usar las opciones de PDF, edición y previsualización.",
        "steps": [
            "Abra el menú lateral.",
            "Seleccione el módulo Novedades.",
            "Abra la vista de novedades registradas.",
            "Abra el PDF asociado a una novedad para revisar su contenido.",
            "Vuelva a la pestaña principal después de revisar el PDF.",
            "Use el botón Editar para modificar una novedad existente.",
            "Use el botón Previsualizar para ver el detalle sin entrar en edición.",
        ],
    },
    "HORARIOS": {
        "title": "Consultar horarios",
        "description": "Describe cómo acceder al módulo de horarios y revisar los registros.",
        "steps": [
            "Abra el menú lateral.",
            "Seleccione el módulo Horarios.",
            "Abra la vista de horarios.",
            "Espere a que la página cargue correctamente.",
        ],
    },
    "VER_HORAS_EXTRA": {
        "title": "Ver horas extra",
        "description": "Describe cómo acceder al módulo de horas extra y registrar nuevas horas.",
        "steps": [
            "Abra el menú lateral.",
            "Seleccione el módulo Horas extra.",
            "Abra la vista de horas extra.",
            "Pulse el botón para registrar horas extra.",
            "Espere a que el formulario de registro de horas extra aparezca.",
        ],
    },
    "BTONES_HORAS_EXTRA": {
        "title": "Previsualizar horas extra",
        "description": "Describe cómo usar la previsualización en el módulo de horas extra.",
        "steps": [
            "Abra el menú lateral.",
            "Seleccione el módulo Horas extra.",
            "Abra la vista de horas extra.",
            "Pulse el botón de previsualización para revisar una entrada.",
            "Espere a que aparezca el modal de previsualización.",
        ],
    },
}

EXCLUDED_LOG_MESSAGES = {
    "USUARIO:",
    "LOGIN EXITOSO",
    "LOGOUT EXITOSO",
    "LOGIN EN FIXTURE",
    "========== FIN FIXTURE",
    "========== FIN TEST",
}


def parse_log_tests():
    if not LOG_PATH.exists():
        raise FileNotFoundError(f"Archivo de logs no encontrado: {LOG_PATH}")

    detected_tests = set()
    with LOG_PATH.open("r", encoding="utf-8") as archivo:
        for linea in archivo:
            match = re.search(r"INICIO TEST(?:_| )([A-Z0-9_]+)", linea)
            if match:
                detected_tests.add(match.group(1))
    return detected_tests


def build_manual():
    tests = parse_log_tests()
    content = [
        "# Manual de Usuario\n",
        "Este manual se genera a partir de los flujos detectados en los logs de ejecución de pruebas.\n\n",
        f"Fecha de generación: {datetime.now():%Y-%m-%d %H:%M:%S}\n\n",
    ]

    if not tests:
        content.append(
            "No se detectaron flujos en el archivo de logs. Ejecute las pruebas y vuelva a generar el manual.\n"
        )
        return "".join(content)

    index = 1
    for test_key in SECTION_DEFINITIONS:
        if test_key not in tests:
            continue

        section = SECTION_DEFINITIONS[test_key]
        content.append(f"## {index}. {section['title']}\n\n")
        content.append(f"{section['description']}\n\n")
        content.append("### Pasos\n\n")
        for step in section["steps"]:
            content.append(f"- {step}\n")
        content.append("\n")

        if "notes" in section:
            content.append("### Notas\n\n")
            for note in section["notes"]:
                content.append(f"- {note}\n")
            content.append("\n")

        index += 1

    return "".join(content)


def write_manual(manual_text: str):
    OUTPUT_FILE.write_text(manual_text, encoding="utf-8")
    print(f"Manual generado en: {OUTPUT_FILE}")


if __name__ == "__main__":
    manual_text = build_manual()
    write_manual(manual_text)
