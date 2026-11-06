from servicios.gestion_operaciones import OperacionesAdmin
from persistencia.departamento_dao import DepartamentoDAO
from .comun import ejecutar, entero, texto


def menu_departamentos(sesion):
    DepartamentoDAO = OperacionesAdmin(sesion, DepartamentoDAO)
    while True:
        print("\n" + "═" * 54)
        print("  🌿 ECOTECH  |  Departamentos")
        print("═" * 54)
        print("   1  │  Crear departamento")
        print("   2  │  Listar departamentos")
        print("   3  │  Buscar departamento")
        print("   4  │  Actualizar departamento")
        print("   5  │  Eliminar departamento")
        print("   0  │  Volver")
        print("─" * 54)
        op = input("Opción: ").strip()
        if op == "0":
            return
        if op == "1":
            ejecutar(lambda: print(f"Departamento creado con ID {DepartamentoDAO.insertar(texto('Nombre: '))}."))
        elif op == "2":
            def listar():
                filas = DepartamentoDAO.listar()
                if not filas:
                    print("No hay departamentos registrados.")
                for fila in filas:
                    print(f"{fila['id_depto']}: {fila['nombre']} | empleados: {fila['empleados']}")
            ejecutar(listar)
        elif op == "3":
            ejecutar(lambda: print(DepartamentoDAO.buscar_por_id(entero("ID: ")) or "No encontrado."))
        elif op == "4":
            def actualizar():
                ident = entero("ID: ")
                print("Actualizado." if DepartamentoDAO.actualizar(ident, texto("Nuevo nombre: ")) else "No encontrado.")
            ejecutar(actualizar)
        elif op == "5":
            ejecutar(lambda: print("Eliminado." if DepartamentoDAO.eliminar(entero("ID: ")) else "No encontrado."))
        else:
            print("Opción no válida.")
