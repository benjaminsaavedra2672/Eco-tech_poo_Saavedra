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


def menu_usuarios():
    while True:
        print("\\n-- Administración de cuentas y roles --")
        print("1. Listar usuarios")
        print("2. Cambiar rol de usuario")
        print("3. Restablecer contraseña")
        print("4. Crear cuenta administradora")
        print("0. Volver")
        op = input("Opción: ").strip()

        if op == "0":
            return
        elif op == "1":
            ejecutar(_listar_usuarios)
        elif op == "2":
            ejecutar(_cambiar_rol)
        elif op == "3":
            ejecutar(_restablecer_password)
        elif op == "4":
            ejecutar(_crear_admin)
        else:
            print("Opción no válida.")


def _listar_usuarios():
    usuarios = UsuarioDAO.listar()
    if not usuarios:
        print("No hay usuarios.")
        return
    for u in usuarios:
        empleado = u.nombre_empleado or "(cuenta administrativa)"
        print(f"ID {u.id} | {u.username} | {u.rol.upper()} | {empleado}")


def _cambiar_rol():
    ident = entero("ID del usuario: ")
    usuarios = {u.id: u for u in UsuarioDAO.listar()}
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
    UsuarioDAO.cambiar_rol(ident, rol)
    print("Rol actualizado correctamente.")


def _crear_admin():
    from dominio.usuario import Usuario
    username = input("Nuevo nombre de usuario admin: ").strip()
    if len(username) < 3 or len(username) > 30:
        raise ValueError("El usuario debe tener entre 3 y 30 caracteres.")
    if UsuarioDAO.buscar_por_username(username):
        raise ValueError("Ese nombre de usuario ya existe.")
    clave = getpass("Contraseña (mínimo 8 caracteres): ")
    if len(clave) < 8 or any(c.isspace() for c in clave):
        raise ValueError("La contraseña debe tener 8 caracteres como mínimo y no contener espacios.")
    UsuarioDAO.insertar(Usuario(username, clave, rol="admin"))
    print("Cuenta administradora creada.")


def _restablecer_password():
    ident = entero("ID del usuario: ")
    usuarios = {u.id: u for u in UsuarioDAO.listar()}
    if ident not in usuarios:
        print("Usuario no encontrado.")
        return
    clave = getpass("Nueva contraseña (mínimo 8 caracteres): ")
    if len(clave) < 8 or any(c.isspace() for c in clave):
        raise ValueError("La contraseña debe tener 8 caracteres como mínimo y no contener espacios.")
    from dominio.usuario import Usuario
    temporal = Usuario("temporal", clave)
    UsuarioDAO.actualizar_password(ident, temporal._hash_para_persistencia())
    print("Contraseña actualizada.")


def menu_administrador(usuario):
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
            menu_empleados()
        elif op == "2":
            menu_departamentos()
        elif op == "3":
            menu_proyectos()
        elif op == "4":
            menu_registros()
        elif op == "5":
            menu_usuarios()
        elif op == "6":
            menu_api()
        elif op == "0":
            print("Sesión de administrador cerrada.")
            return
        else:
            print("Opción no válida.")
