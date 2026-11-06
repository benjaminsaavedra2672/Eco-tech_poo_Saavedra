"""Acciones administrativas con autorización obligatoria en el servicio."""
from servicios.permisos import exigir_admin
from persistencia.usuario_dao import UsuarioDAO
from persistencia.empleado_dao import EmpleadoDAO
from dominio.usuario import Usuario

def listar_cuentas(sesion):
    exigir_admin(sesion)
    return UsuarioDAO.listar()

def cambiar_rol(sesion, usuario_id, rol):
    exigir_admin(sesion)
    rol = Usuario.validar_rol(rol)
    cuentas = {u.id:u for u in UsuarioDAO.listar()}
    cuenta = cuentas.get(usuario_id)
    if cuenta is None:
        raise ValueError("Cuenta inexistente.")
    if cuenta.username == "admin" and rol != "admin":
        raise ValueError("No se puede degradar al administrador inicial.")
    if rol == "empleado" and cuenta.empleado_id is None:
        raise ValueError("El rol empleado requiere un empleado asociado.")
    return UsuarioDAO.cambiar_rol(usuario_id, rol)

def crear_admin(sesion, username, clave):
    exigir_admin(sesion)
    nuevo = Usuario(username, clave, rol="admin")
    if UsuarioDAO.buscar_por_username(nuevo.username):
        raise ValueError("Nombre de usuario ya registrado.")
    return UsuarioDAO.insertar(nuevo)

def cambiar_clave(sesion, usuario_id, clave):
    exigir_admin(sesion)
    Usuario.validar_clave(clave)
    if usuario_id not in {u.id for u in UsuarioDAO.listar()}:
        raise ValueError("Cuenta inexistente.")
    return UsuarioDAO.actualizar_password(usuario_id, Usuario._crear_hash(clave))

def listar_empleados(sesion):
    exigir_admin(sesion)
    return EmpleadoDAO.listar()

def buscar_empleado(sesion, ident):
    exigir_admin(sesion)
    return EmpleadoDAO.buscar_por_id(ident)

def crear_empleado(sesion, empleado):
    exigir_admin(sesion)
    return EmpleadoDAO.insertar(empleado)

def editar_empleado(sesion, empleado):
    exigir_admin(sesion)
    return EmpleadoDAO.actualizar(empleado)

def eliminar_empleado(sesion, ident):
    exigir_admin(sesion)
    return EmpleadoDAO.eliminar(ident)
