"""Menú limitado del empleado autenticado."""
from datetime import date
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from .menu_api import menu_api


def _mis_datos(usuario):
    empleado = EmpleadoDAO.buscar_por_id(usuario.empleado_id)
    if not empleado:
        print("No existe un perfil de empleado asociado a esta cuenta.")
        return
    print("\\n-- Mi perfil --")
    print(f"Nombre: {empleado.nombre}")
    print(f"Usuario: {usuario.username}")
    print(f"Correo: {empleado.correo}")
    print(f"Dirección: {empleado.direccion or '-'}")
    print(f"Teléfono: {empleado.telefono or '-'}")
    print(f"Departamento ID: {empleado.departamento_id or '-'}")
    print("Para cambiar datos personales, contacte al administrador.")


def _mis_proyectos(usuario):
    filas = ProyectoDAO.listar_por_empleado(usuario.empleado_id)
    print("\\n-- Mis proyectos --")
    if not filas:
        print("No tienes proyectos asignados.")
        return
    for f in filas:
        print(f"{f['id_proyecto']}: {f['nombre']} | {f['fecha_inicio']} a {f['fecha_fin']}")
        print(f"   {f['descripcion']}")


def _mis_registros(usuario):
    filas = RegistroTiempoDAO.listar_por_empleado(usuario.empleado_id)
    print("\\n-- Mis registros de tiempo --")
    if not filas:
        print("Todavía no tienes registros.")
        return
    for f in filas:
        print(f"{f['id_registro']} | {f['fecha']} | {f['proyecto']} | {f['horas_trabajadas']} h | {f['descripcion_tarea']}")


def _registrar_horas(usuario):
    proyectos = ProyectoDAO.listar_por_empleado(usuario.empleado_id)
    if not proyectos:
        print("No puedes registrar horas porque no tienes proyectos asignados.")
        return
    print("\\n-- Proyectos asignados --")
    ids = set()
    for p in proyectos:
        ids.add(int(p["id_proyecto"]))
        print(f"{p['id_proyecto']}: {p['nombre']}")
    while True:
        raw = input("ID del proyecto: ").strip()
        if raw.isdigit() and int(raw) in ids:
            proyecto_id = int(raw)
            break
        print("Selecciona un proyecto que tengas asignado.")
    fecha = input(f"Fecha [ {date.today().isoformat()} ]: ").strip() or date.today().isoformat()
    while True:
        raw = input("Horas trabajadas (0-24): ").strip().replace(",", ".")
        try:
            horas = float(raw)
            if 0 < horas <= 24:
                break
        except ValueError:
            pass
        print("Ingresa un número mayor que 0 y hasta 24.")
    descripcion = input("Descripción de la tarea: ").strip()
    if not descripcion:
        print("La descripción es obligatoria.")
        return
    ident = RegistroTiempoDAO.insertar(usuario.empleado_id, proyecto_id, fecha, horas, descripcion)
    print(f"Registro creado con ID {ident}.")


def menu_empleado(usuario):
    while True:
        print("\\n" + "=" * 48)
        print(f" ECOTECH | EMPLEADO: {usuario.nombre_empleado or usuario.username}")
        print("=" * 48)
        print("1. Consultar mi perfil")
        print("2. Ver mis proyectos")
        print("3. Registrar horas trabajadas")
        print("4. Consultar mis registros de tiempo")
        print("5. Servicios API (tiempo y monedas)")
        print("0. Cerrar sesión")
        op = input("Opción: ").strip()

        if op == "1":
            _mis_datos(usuario)
        elif op == "2":
            _mis_proyectos(usuario)
        elif op == "3":
            try:
                _registrar_horas(usuario)
            except Exception as exc:
                print(f"No se pudo registrar el tiempo: {exc}")
        elif op == "4":
            _mis_registros(usuario)
        elif op == "5":
            menu_api()
        elif op == "0":
            print("Sesión de empleado cerrada.")
            return
        else:
            print("Opción no válida.")
