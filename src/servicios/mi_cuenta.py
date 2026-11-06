"""Operaciones personales: el ID se obtiene siempre de la sesión."""
from servicios.permisos import exigir_empleado
from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO

def mi_perfil(sesion):
    return EmpleadoDAO.buscar_por_id(exigir_empleado(sesion))

def actualizar_mis_datos(sesion, nombre, correo):
    empleado_id = exigir_empleado(sesion)
    empleado = EmpleadoDAO.buscar_por_id(empleado_id)
    if empleado is None:
        raise ValueError("No se encontró el perfil asociado a la sesión.")
    nombre = Empleado.validar_nombre(nombre)
    correo = Empleado.validar_correo(correo)
    return EmpleadoDAO.actualizar_nombre_correo(empleado_id, nombre, correo)

def mis_registros(sesion):
    from persistencia.registro_tiempo_dao import RegistroTiempoDAO
    return RegistroTiempoDAO.listar_por_empleado(exigir_empleado(sesion))


def actualizar_mi_usuario(sesion, nuevo_username):
    from dominio.usuario import Usuario
    from persistencia.usuario_dao import UsuarioDAO
    if sesion is None or getattr(sesion, "id", None) is None:
        raise PermissionError("Inicie sesión para modificar su cuenta.")
    nuevo_username = Usuario.normalizar_usuario(nuevo_username)
    existente = UsuarioDAO.buscar_por_username(nuevo_username)
    if existente and existente.id != sesion.id:
        raise ValueError("El nombre de usuario ya está registrado.")
    if sesion.username == "admin" and nuevo_username != "admin":
        raise ValueError("El usuario administrador principal debe conservar el nombre admin.")
    resultado = UsuarioDAO.actualizar_username(sesion.id, nuevo_username)
    if resultado:
        sesion.username = nuevo_username
    return resultado


def actualizar_mi_clave(sesion, actual, nueva):
    from dominio.usuario import Usuario
    from persistencia.usuario_dao import UsuarioDAO
    if sesion is None or getattr(sesion, "id", None) is None:
        raise PermissionError("Inicie sesión para modificar su contraseña.")
    cuenta = UsuarioDAO.buscar_por_username(sesion.username)
    if cuenta is None or cuenta.id != sesion.id or not cuenta.autenticar(actual):
        raise ValueError("La contraseña actual es incorrecta.")
    Usuario.validar_clave(nueva)
    if len(nueva) < 8 or len(nueva) > 128 or any(c.isspace() for c in nueva):
        raise ValueError("La nueva contraseña debe tener entre 8 y 128 caracteres y no contener espacios.")
    return UsuarioDAO.actualizar_password(sesion.id, Usuario._crear_hash(nueva))
