"""Menú para consultar las API externas de EcoTech."""
from .comun import ejecutar
from servicios import tiempo, consulta_moneda
from servicios.indicadores import consultar_indicador, obtener_historial


def _mostrar_indicador(resultado):
    print(f"\nOrigen: {resultado['origen']}")
    print(resultado['mensaje'])
    dato = resultado['dato']
    if dato:
        print(f"{dato['codigo']}: {dato['valor']:.4f} {dato['unidad']}")
        print(f"Fecha del dato: {dato['fecha']}")
        print(f"Última verificación: {dato['verificado_en']}")


def menu_api(sesion=None):
    while True:
        print("\n" + "═" * 54)
        print("  🌿 ECOTECH  |  Servicios externos / API")
        print("═" * 54)
        print("   1  │  Consultar tiempo en Santiago")
        print("   2  │  Tipo de cambio y conversión")
        print("   3  │  Consultar y guardar indicador")
        print("   4  │  Ver historial local (sin API)")
        print("   0  │  Volver")
        print("─" * 54)
        opcion = input("Opción: ").strip()

        if opcion == "1":
            ejecutar(tiempo.consultar_y_mostrar)
        elif opcion == "2":
            ejecutar(consulta_moneda.menu_monedas)
        elif opcion == "3":
            codigo = input("Código (CLP/EUR/GBP/BRL/ARS/PEN/MXN): ").strip().upper()
            ejecutar(lambda: _mostrar_indicador(consultar_indicador(sesion, codigo)))
        elif opcion == "4":
            def mostrar_historial():
                codigo = input("Filtrar por código (Enter = todos): ").strip().upper() or None
                filas = obtener_historial(sesion, codigo)
                if not filas:
                    print("No hay observaciones guardadas.")
                for dato in filas:
                    print(f"{dato['fecha']} | {dato['codigo']} | {dato['valor']:.4f} {dato['unidad']} | {dato['fuente']} | verificado: {dato['verificado_en']}")
            ejecutar(mostrar_historial)
        elif opcion == "0":
            return
        else:
            print("Opción no válida.")
