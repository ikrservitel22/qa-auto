LOGIN_USUARIO = '//*[@id="usu_username"]' ##campo de usuario login
LOGIN_PASSWORD = '//*[@id="password"]'   ##campo de contraseña login
LOGIN_BOTON = '/html/body/div/div/div/div/div/div/div[2]/div/div/form/button'   ##botón de inicio de sesión
LOGOUT_BOTON = '//*[@id="sidebar"]/div[2]/form/button'  ##botón de cierre de sesión
SIDEBAR_BOTON = '/html/body/div/div[2]/header/i'  ##botón de barra lateral

MENU_NOVEDADES = '//*[@id="sidebarNav"]/div[2]/button'  ##menú de novedades
MENU_NOVEDADES_VER = '//*[@id="sidebarNav"]/div[2]/div/a[1]'  ##opción ver novedades
MENU_NOVEDADES_NUEVA = '//*[@id="sidebarNav"]/div[2]/div/a[2]'  ##opción nueva novedad
NOVEDADES_FORM_TYPE_SELECT = '/html/body/div/div[2]/div/div/div/div/div[2]/form/div/div[2]/span/span[1]/span'  ##select de tipo de novedad
NOVEDADES_FORM_FECHA_INICIO = '//*[@id="nov_fecha_inicio"]'  ##input de fecha de inicio
NOVEDADES_FORM_FECHA_FIN = '//*[@id="nov_fecha_fin"]'  ##input de fecha de fin
NOVEDADES_FORM_HORA_INICIO = '//*[@id="nov_hora_inicio"]'  ##input de hora de inicio
NOVEDADES_FORM_HORA_FIN = '//*[@id="nov_hora_fin"]'  ##input de hora
NOVEDADES_FORM_DESCRIPCION_TEXTAREA = '/html/body/div/div[2]/div/div/div/div/div[2]/form/div/div[12]/textarea'  ##input de descripción
NOVEDADES_FORM_GUARDAR_BUTTON = '/html/body/div/div[2]/div/div/div/div/div[2]/form/div/div[16]/button'  ##botón de guardar novedad
NOVEDADES_SUCCESS_MESSAGE = '//*[@id="swal2-html-container"]'  ##mensaje de éxito al crear novedad
NOVEDADES_SUCCESS_ACCEPT_BUTTON = '/html/body/div[2]/div/div[6]/button[1]'  ##botón de aceptar cambios 

# Horas extra
SIDEBAR_HORAS_BUTTON = '//*[@id="sidebarNav"]/div[5]/button'
MENU_HORAS_VER = '//*[@id="sidebarNav"]/div[5]/div/a[1]'
MENU_HORAS_CREAR = '//*[@id="sidebarNav"]/div[5]/div/a[2]'
HORAS_EXTRA_PAGE_TITLE = "//*[contains(normalize-space(.), 'Horas extra')]"
HORAS_EXTRA_REGISTRAR_BUTTON = '/html/body/div/div[2]/div/div/div/div/div[1]/a'

# Formulario crear horas extra
HORAS_EXTRA_FORM_FECHA_INICIO = '//*[@id="hex_fecha_inicio"]'
HORAS_EXTRA_FORM_HORA_INICIO = '//*[@id="hex_hora_inicio"]'
HORAS_EXTRA_FORM_FECHA_FIN = '//*[@id="hex_fecha_fin"]'
HORAS_EXTRA_FORM_HORA_FIN = '//*[@id="hex_hora_fin"]'
HORAS_EXTRA_FORM_RAZON_INPUT = '/html/body/div/div[2]/div/div/div/div/div[2]/form/div/div[5]/input'
HORAS_EXTRA_FORM_JUSTIF_TEXTAREA = '/html/body/div/div[2]/div/div/div/div/div[2]/form/div/div[6]/textarea'
HORAS_EXTRA_FORM_GUARDAR_BUTTON = '/html/body/div/div[2]/div/div/div/div/div[2]/form/div/div[8]/button'
HORAS_EXTRA_SUCCESS_MSG = '/html/body/div[2]/div'
HORAS_EXTRA_SUCCESS_CLOSE = '/html/body/div/div[2]/div/div/div[2]/div/div[6]/button[1]'

# Tabla y modal de horas extra
HORAS_EXTRA_TABLA_PREVIEW_BUTTON = '//*[@id="DataTables_Table_0"]/tbody/tr[1]/td[8]/div/button'
HORAS_EXTRA_MODAL_PREVIEW = '/html/body/div[2]/div'

# Novedades - tabla y acciones
NOVEDADES_TABLA_MIAS_PDF_THIRD = '//*[@id="tabla-mias"]/tbody/tr[3]/td[9]/div/a[1]'
NOVEDADES_TABLA_MIAS_EDIT_THIRD = '//*[@id="tabla-mias"]/tbody/tr[3]/td[9]/div/a[2]'
NOVEDADES_TABLA_MIAS_PREVIEW_THIRD = '//*[@id="tabla-mias"]/tbody/tr[3]/td[9]/div/button'
NOVEDADES_MODAL_DETALLE = '//*[@id="modal-detalle"]/div/div'
NOVEDADES_BACK_BUTTON = '/html/body/div/div[2]/div/div/div/div/div[1]/a'

# Proyectos
MENU_PROYECTOS = '//*[@id="sidebarNav"]/a[2]'
PROYECTOS_PAGE_TITLE = '/html/body/div/div[2]/div/div/div/div[1]/h5'
PROYECTOS_ACCION_VER = '/html/body/div/div[2]/div/div/div/div[2]/div/table/tbody/tr[1]/td[7]/a[1]/i'
PROYECTOS_DETALLE_TITLE = '/html/body/div/div[2]/div/div/div[1]/div[1]/div[1]/div/h5'
PROYECTOS_ACCION_EDITAR = '/html/body/div/div[2]/div/div/div[1]/div[1]/div[2]/a[1]'
PROYECTOS_EDITAR_TITLE = '/html/body/div/div[2]/div/div/div/div/div[1]/h5'
PROYECTOS_EDITAR_VOLVER = '/html/body/div/div[2]/div/div/div/div/div[2]/form/div[7]/a'
PROYECTOS_DETALLE_VOLVER_LISTADO = '/html/body/div/div[2]/div/div/div[1]/div[1]/div[2]/a[2]'
PROYECTOS_NUEVO_BUTTON = '/html/body/div/div[2]/div/div/div/div[1]/a'

# Servidores
MENU_SERVIDORES = '//*[@id="sidebarNav"]/a[3]'
SERVIDORES_PRIMER_ENLACE = '//*[@id="tablaServidores"]/tbody/tr[1]/td[1]/a'
SERVIDORES_PAGE_TITLE = '/html/body/div/div[2]/div/div/div/div[1]/h5'
SERVIDOR_DETAIL_TITLE = '/html/body/div/div[2]/div/div/div/div[1]/div/div/h5'

# Organigrama
SIDEBAR_ORGANIGRAMA_BUTTON = '//*[@id="sidebarNav"]/div[9]/button'
MENU_ORGANIGRAMA_COMPLETO = '//*[@id="sidebarNav"]/div[9]/div/a[1]'
MENU_ORGANIGRAMA_AREAS_LIDERES = '//*[@id="sidebarNav"]/div[9]/div/a[2]'
MENU_ORGANIGRAMA_MI_AREA = '//*[@id="sidebarNav"]/div[9]/div/a[3]'
ORGANIGRAMA_PAGE_TITLE = '/html/body/div/div[2]/div/div/div/div/div[1]/h5'

# Horarios
SIDEBAR_HORARIOS_BUTTON = '//*[@id="sidebarNav"]/div[4]/button'
MENU_HORARIOS_VER = '//*[@id="sidebarNav"]/div[4]/div/a[1]'
MENU_HORARIOS_SOLICITUD = '//*[@id="sidebarNav"]/div[4]/div/a[2]'
MENU_HORARIOS_ESTADO = '/html/body/div/div[1]/nav/div[4]/div/a[3]'
HORARIOS_PAGE_TITLE = "//*[contains(normalize-space(.), ' Horarios')]"

# Tabla detalle
TABLA_DETALLE_EXPORT_BUTTON = '//*[@id="tabla-detalle_wrapper"]/div[1]/div[2]/div/button[1]'
EXPORT_PAGE_LINK = '/html/body/div/div[2]/div/div/div/div[1]/div[3]/a'

# Inventario
SIDEBAR_INVENTARIO_BUTTON = '//*[@id="sidebarNav"]/div[6]/button'
MENU_INVENTARIO_TODOS = '//*[@id="sidebarNav"]/div[6]/div/a[1]'
INVENTARIO_PAGE_TITLE = '/html/body/div/div[2]/div/div/div[1]/div/div[1]/h4'
INVENTARIO_NUEVO_ARTICULO_HEADER_BUTTON = '/html/body/div/div[2]/div/div/div[1]/div/div[1]/div/a'

# Inventario: flujo solicitado
MENU_INVENTARIO_NUEVO_ARTICULO = '//*[@id="sidebarNav"]/div[6]/div/a[2]'
INVENTARIO_NUEVO_ARTICULO_TITLE = '/html/body/div/div[2]/div/div/div/div/div[1]/h4'

# Campos del formulario crear inventario
INV_FORM_TYPE_SELECT = '//*[@id="formInventario"]/div[1]/div[1]/span/span[1]/span'

INV_FORM_PRODUCT_INPUT = '//*[@id="formInventario"]/div[1]/div[3]/input'
INV_FORM_STATE_SELECT = '//*[@id="formInventario"]/div[1]/div[5]/span/span[1]/span'
INV_FORM_COMPANY_SELECT = '//*[@id="formInventario"]/div[1]/div[6]/span/span[1]/span'
INV_FORM_SUBMIT = '/html/body/div/div[2]/div/div/div/div/div[2]/form/div[2]/button'

