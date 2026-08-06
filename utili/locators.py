LOGIN_USUARIO = '//*[@id="usu_username"]' ##campo de usuario login
LOGIN_PASSWORD = '//*[@id="password"]'   ##campo de contraseña login
LOGIN_BOTON = '/html/body/div/div/div/div/div/div/div[2]/div/div/form/button'   ##botón de inicio de sesión
LOGOUT_BOTON = '//*[@id="sidebar"]/div[2]/form/button'  ##botón de cierre de sesión
SIDEBAR_BOTON = '/html/body/div/div[2]/header/i'  ##botón de barra lateral

MENU_NOVEDADES = '//*[@id="sidebarNav"]/div[2]/button'  ##menú de novedades
BOTON_VER_NOVEDADES = '//*[@id="sidebarNav"]/div[2]/div/a[1]'  ##botón de ver novedades
BOTON_NUEVA_NOVEDAD = '/html/body/div/div[2]/div/div/div/div[1]/div[1]/a'  ##botón de nueva novedad
SELECT_TIPO = '/html/body/div/div[2]/div/div/div/div/div[2]/form/div/div[2]/span/span[1]/span'  ##select de tipo de novedad
FECHA_INICIO = '//*[@id="nov_fecha_inicio"]'  ##input de fecha de inicio
FECHA_FIN = '//*[@id="nov_fecha_fin"]'  ##input de fecha de fin
HORA_INICIO = '//*[@id="nov_hora_inicio"]'  ##input de hora de inicio
HORA_FIN = '//*[@id="nov_hora_fin"]'  ##input de hora
INPUT_DESCRIPCION = '/html/body/div/div[2]/div/div/div/div/div[2]/form/div/div[12]/textarea'  ##input de descripción
BOTON_GUARDAR = '/html/body/div/div[2]/div/div/div/div/div[2]/form/div/div[16]/button'  ##botón de guardar novedad
MENSAJE_EXITO = '//*[@id="swal2-html-container"]'  ##mensaje de éxito al crear novedad
BOTON_ACEPTAR = '/html/body/div[2]/div/div[6]/button[1]'  ##botón de aceptar cambios 

BOTON_CREAR_NOVEDAD = '//*[@id="sidebarNav"]/div[2]/div/a[2]'  ##botón de crear novedad

# Horas extra
SIDEBAR_HORAS_BUTTON = '//*[@id="sidebarNav"]/div[5]/button'
MENU_HORAS_VER = '//*[@id="sidebarNav"]/div[5]/div/a[1]'
MENU_HORAS_CREAR = '//*[@id="sidebarNav"]/div[5]/div/a[2]'
HORAS_PAGE_TITLE = "//*[contains(normalize-space(.), 'Horas extra')]"
HORAS_REGISTRAR_BUTTON = '/html/body/div/div[2]/div/div/div/div/div[1]/a'

# Formulario crear horas extra
HEX_FECHA_INICIO = '//*[@id="hex_fecha_inicio"]'
HEX_HORA_INICIO = '//*[@id="hex_hora_inicio"]'
HEX_FECHA_FIN = '//*[@id="hex_fecha_fin"]'
HEX_HORA_FIN = '//*[@id="hex_hora_fin"]'
HEX_RAZON_INPUT = '/html/body/div/div[2]/div/div/div/div/div[2]/form/div/div[5]/input'
HEX_JUSTIF_TEXTAREA = '/html/body/div/div[2]/div/div/div/div/div[2]/form/div/div[6]/textarea'
HEX_GUARDAR_BUTTON = '/html/body/div/div[2]/div/div/div/div/div[2]/form/div/div[8]/button'
HORAS_SUCCESS_MSG = '/html/body/div[2]/div'
HORAS_SUCCESS_CLOSE = '/html/body/div[2]/div/div[6]/button[1]'

# Tabla y modal
TABLA_EXTRAS_PREVIEW_BUTTON = '//*[@id="tabla-extras"]/tbody/tr[1]/td[8]/div/button'
MODAL_PREVIEW_XPATH = '/html/body/div[2]/div'

