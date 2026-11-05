"""Menú para consultar las API externas de EcoTech."""
from .comun import ejecutar
from servicios import tiempo, consulta_moneda


def menu_api():
    while True:
        print("\\n-- Servicios externos / API --")
        print("1. Consultar tiempo en Santiago")
        print("2. Consultar tipo de cambio y convertir monedas")
        print("0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            ejecutar(tiempo.consultar_y_mostrar)
        elif opcion == "2":
            ejecutar(consulta_moneda.menu_monedas)
        elif opcion == "0":
            return
        else:
            print("Opción no válida.")
