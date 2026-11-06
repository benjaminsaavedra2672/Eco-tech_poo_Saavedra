"""Menú limitado del empleado autenticado."""
from datetime import date
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from servicios.gestion_operaciones import mis_proyectos, registrar_mis_horas
from .menu_api import menu_api
from servicios.mi_cuenta import mi_perfil, actualizar_mis_datos, mis_registros
from servicios.permisos import exigir_empleado
from .menu_empleado import pedir_nombre, pedir_correo


def _mis_datos(usuario):
    empleado = mi_perfil(usuario)
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



def _mis_proyectos(usuario):
    exigir_empleado(usuario)
    filas = mis_proyectos(usuario)
    print("\\n-- Mis proyectos --")
    if not filas:
        print("No tienes proyectos asignados.")
        return
    for f in filas:
        print(f"{f['id_proyecto']}: {f['nombre']} | {f['fecha_inicio']} a {f['fecha_fin']}")
        print(f"   {f['descripcion']}")


def _mis_registros(usuario):
    filas = mis_registros(usuario)
    print("\\n-- Mis registros de tiempo --")
    if not filas:
        print("Todavía no tienes registros.")
        return
    for f in filas:
        print(f"{f['id_registro']} | {f['fecha']} | {f['proyecto']} | {f['horas_trabajadas']} h | {f['descripcion_tarea']}")


def _registrar_horas(usuario):
    exigir_empleado(usuario)
    proyectos = mis_proyectos(usuario)
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
    ident = registrar_mis_horas(usuario, proyecto_id, fecha, horas, descripcion)
    print(f"Registro creado con ID {ident}.")


def _editar_mis_datos(usuario):
    actual = mi_perfil(usuario)
    if actual is None:
        raise ValueError("Perfil no encontrado.")
    print("Presione Enter para conservar el valor actual.")
    nombre = pedir_nombre(f"Nombre [{actual.nombre}]: ", actual=actual.nombre)
    correo = pedir_correo(f"Correo [{actual.correo}]: ", actual=actual.correo)
    if actualizar_mis_datos(usuario, nombre, correo):
        print("Datos personales actualizados correctamente.")
    else:
        print("No se realizaron cambios.")

def menu_empleado(usuario):
    exigir_empleado(usuario)
    while True:
        print("\n" + "═" * 54)
        print(f"  🌿 ECOTECH  |  EMPLEADO: {usuario.nombre_empleado or usuario.username}")
        print("═" * 54)
        print("   1  │  👤 Consultar mi perfil")
        print("   2  │  📁 Ver mis proyectos")
        print("   3  │  ⏱  Registrar horas trabajadas")
        print("   4  │  📋 Consultar mis registros de tiempo")
        print("   5  │  🌐 Servicios API (tiempo y monedas)")
        print("   6  │  ✏  Modificar mi nombre y correo")
        print("  ────────────────────────────────────────────────────")
        print("   0  │  🚪 Cerrar sesión")
        print("═" * 54)
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
            menu_api(usuario)
        elif op == "6":
            try:
                _editar_mis_datos(usuario)
            except Exception as exc:
                print(f"No se pudieron actualizar los datos: {exc}")
        elif op == "0":
            print("Sesión de empleado cerrada.")
            return
        else:
            print("Opción no válida.")
