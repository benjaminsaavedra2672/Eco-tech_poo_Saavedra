"""Inicio de la aplicación: inicialización, autenticación y enrutamiento por rol."""
from getpass import getpass
from persistencia.crear_bd import crear_tablas
from persistencia.semilla_bd import cargar_semilla
from persistencia.conexion import motor_actual
from servicios.inicializacion import asegurar_administrador
from servicios.autentificacion import iniciar_sesion
from menus.menu_admin import menu_administrador
from menus.menu_portal_empleado import menu_empleado


def menu_principal():
    try:
        crear_tablas()
        asegurar_administrador()
        cargar_semilla()
        print(f"Base de datos conectada: {motor_actual().upper()}")
    except Exception as exc:
        print(f"No se pudo inicializar la base de datos: {exc}")
        return

    print("\n" + "═" * 54)
    print("            🌿  ECOTECH  🌿")
    print("          INICIO DE SESIÓN")
    print("═" * 54)
    intentos = 3
    usuario_activo = None
    while intentos > 0:
        username = input("Usuario: ").strip()
        password = getpass("Contraseña: ")
        usuario_activo = iniciar_sesion(username, password)
        if usuario_activo:
            if usuario_activo.rol == "admin":
                menu_administrador(usuario_activo)
            elif usuario_activo.rol == "empleado" and usuario_activo.empleado_id is not None:
                menu_empleado(usuario_activo)
            else:
                print("La cuenta no tiene un perfil válido para este rol.")
            return
        intentos -= 1
        print(f"Usuario o contraseña incorrectos. Intentos restantes: {intentos}")

    print("Se agotaron los intentos de inicio de sesión.")
