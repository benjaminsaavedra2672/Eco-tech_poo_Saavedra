from persistencia.crear_bd import crear_tablas
from persistencia.semilla_bd import cargar_semilla
from persistencia.conexion import motor_actual
from .menu_empleado import menu_empleados
from .menu_departamento import menu_departamentos
from .menu_proyecto import menu_proyectos
from .menu_registro_tiempo import menu_registros
from persistencia.usuario_dao import UsuarioDAO


def menu_principal():
    try:
        crear_tablas()
        cargar_semilla()
        print(f"Base de datos conectada: {motor_actual().upper()}")
    except Exception as exc:
        print(f"No se pudo inicializar la base de datos: {exc}")
        if motor_actual() == "mysql":
            print("Revisa que MySQL esté iniciado, que la base exista y que las credenciales de .env sean correctas.")
        return

    # El acceso se valida con la cuenta guardada en la base de datos.
    print("\n=== INICIO DE SESIÓN ECOTECH ===")
    intentos = 3
    usuario_activo = None
    while intentos > 0:
        username = input("Usuario: ").strip()
        password = input("Contraseña: ")
        usuario = UsuarioDAO.buscar_por_username(username)
        if usuario and usuario.autenticar(password) and usuario.empleado_id is not None:
            usuario_activo = usuario
            break
        intentos -= 1
        print(f"Usuario o contraseña incorrectos. Intentos restantes: {intentos}")
    if usuario_activo is None:
        print("No se pudo iniciar sesión.")
        return

    nombre = usuario_activo.nombre_empleado or usuario_activo.username
    print(f"\nBienvenido/a, {nombre} ({usuario_activo.rol or 'Empleado'}).")

    while True:
        print("\n=== ECOTECH SOLUTIONS ===\n1 Empleados\n2 Departamentos\n3 Proyectos\n4 Registros de tiempo\n0 Cerrar sesión y salir")
        op = input("Opción: ").strip()
        if op == "1":
            menu_empleados()
        elif op == "2":
            menu_departamentos()
        elif op == "3":
            menu_proyectos()
        elif op == "4":
            menu_registros()
        elif op == "0":
            print("Hasta luego.")
            break
        else:
            print("Opción no válida.")
