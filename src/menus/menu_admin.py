"""Menú exclusivo para administradores."""
from getpass import getpass
from persistencia.usuario_dao import UsuarioDAO
from persistencia.empleado_dao import EmpleadoDAO
from .menu_empleado import menu_empleados
from .menu_departamento import menu_departamentos
from .menu_proyecto import menu_proyectos
from .menu_registro_tiempo import menu_registros
from .menu_api import menu_api
from .comun import ejecutar, entero
from servicios import gestion_admin as ga
from servicios.permisos import exigir_admin


def menu_usuarios(sesion):
    exigir_admin(sesion)
    while True:
        print("-- Administración de cuentas y roles --")
        print("1. Listar usuarios")
        print("2. Cambiar rol de usuario")
        print("3. Restablecer contraseña")
        print("4. Crear cuenta administradora")
        print("0. Volver")
        op = input("Opción: ").strip()

        if op == "0":
            return
        elif op == "1":
            ejecutar(lambda: _listar_usuarios(sesion))
        elif op == "2":
            ejecutar(lambda: _cambiar_rol(sesion))
        elif op == "3":
            ejecutar(lambda: _restablecer_password(sesion))
        elif op == "4":
            ejecutar(lambda: _crear_admin(sesion))
        else:
            print("Opción no válida.")


def _listar_usuarios(sesion):
    usuarios = ga.listar_cuentas(sesion)
    if not usuarios:
        print("No hay usuarios.")
        return
    for u in usuarios:
        empleado = u.nombre_empleado or "(cuenta administrativa)"
        print(f"ID {u.id} | {u.username} | {u.rol.upper()} | {empleado}")


def _cambiar_rol(sesion):
    ident = entero("ID del usuario: ")
    usuarios = {u.id: u for u in ga.listar_cuentas(sesion)}
    usuario = usuarios.get(ident)
    if not usuario:
        print("Usuario no encontrado.")
        return
    print("1. admin")
    print("2. empleado")
    opcion = input("Nuevo rol: ").strip()
    rol = {"1": "admin", "2": "empleado"}.get(opcion)
    if not rol:
        print("Opción no válida.")
        return
    if rol != "admin" and usuario.empleado_id is None:
        print("Esta cuenta no tiene perfil de empleado; no puede cambiarse a empleado.")
        return
    if usuario.username == "admin" and rol != "admin":
        print("No se puede quitar el rol al administrador principal.")
        return
    ga.cambiar_rol(sesion, ident, rol)
    print("Rol actualizado correctamente.")


def _crear_admin(sesion):
    from dominio.usuario import Usuario
    username = input("Nuevo nombre de usuario admin: ").strip()
    if UsuarioDAO.buscar_por_username(username):
        raise ValueError("Ese nombre de usuario ya existe.")
    clave = getpass("Contraseña (mínimo 8 caracteres): ")
    if len(clave) < 8 or any(c.isspace() for c in clave):
        raise ValueError("La contraseña debe tener 8 caracteres como mínimo y no contener espacios.")
    ga.crear_admin(sesion, username, clave)
    print("Cuenta administradora creada.")


def _restablecer_password(sesion):
    ident = entero("ID del usuario: ")
    usuarios = {u.id: u for u in ga.listar_cuentas(sesion)}
    if ident not in usuarios:
        print("Usuario no encontrado.")
        return
    clave = getpass("Nueva contraseña (mínimo 8 caracteres): ")
    if len(clave) < 8 or any(c.isspace() for c in clave):
        raise ValueError("La contraseña debe tener 8 caracteres como mínimo y no contener espacios.")
    from dominio.usuario import Usuario
    ga.cambiar_clave(sesion, ident, clave)
    print("Contraseña actualizada.")


def menu_administrador(usuario):
    exigir_admin(usuario)
    while True:
        print("\\n" + "=" * 48)
        print(f" ECOTECH | ADMINISTRADOR: {usuario.username}")
        print("=" * 48)
        print("1. Gestión de empleados")
        print("2. Gestión de departamentos")
        print("3. Gestión de proyectos")
        print("4. Gestión de registros de tiempo")
        print("5. Gestión de usuarios y roles")
        print("6. Servicios API (tiempo y monedas)")
        print("0. Cerrar sesión")
        op = input("Opción: ").strip()

        if op == "1":
            menu_empleados(usuario)
        elif op == "2":
            menu_departamentos(usuario)
        elif op == "3":
            menu_proyectos(usuario)
        elif op == "4":
            menu_registros(usuario)
        elif op == "5":
            menu_usuarios(usuario)
        elif op == "6":
            menu_api(usuario)
        elif op == "0":
            print("Sesión de administrador cerrada.")
            return
        else:
            print("Opción no válida.")
