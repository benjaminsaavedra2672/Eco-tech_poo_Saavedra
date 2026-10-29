import requests
import math


def obtener_datos():
    respuesta = requests.get(
        "https://open.er-api.com/v6/latest/USD",
        timeout=(3, 5),
    )

    respuesta.raise_for_status()
    datos = respuesta.json()

    if datos.get("result") != "success":
        raise ValueError("No se pudieron obtener los datos de la API.")

    return datos


def extraer_primero(datos, moneda):
    # Verificar que la respuesta sea un diccionario.
    if not isinstance(datos, dict):
        raise ValueError("Respuesta inesperada.")

    # Obtener las tasas de cambio.
    tasas = datos.get("rates")

    if not isinstance(tasas, dict):
        raise ValueError("No hay valores disponibles.")

    # Obtener el valor de la moneda solicitada.
    valor = tasas.get(moneda)

    # Validar que el valor sea un número válido.
    if (
        type(valor) not in (int, float)
        or not math.isfinite(valor)
        or valor <= 0
    ):
        raise ValueError("Valor de la moneda inválido.")

    # Devolver la fecha de actualización y el valor.
    fecha = datos.get("time_last_update_utc", "No disponible")
    return fecha, valor


def mostrar_menu():
    print("\n" + "=" * 42)
    print("          CONSULTA DE MONEDAS")
    print("=" * 42)
    print("1. Consultar valores de las monedas")
    print("2. Convertir dólares a otra moneda")
    print("3. Salir")
    print("=" * 42)


def consultar_monedas(datos):
    monedas = {
        "CLP": "Peso chileno",
        "EUR": "Euro",
        "GBP": "Libra esterlina",
        "BRL": "Real brasileño",
        "ARS": "Peso argentino",
        "PEN": "Sol peruano",
        "MXN": "Peso mexicano",
    }

    fecha, _ = extraer_primero(datos, "CLP")

    print("\n" + "=" * 52)
    print("           VALORES DE LAS MONEDAS")
    print("=" * 52)
    print("Moneda             Código       Valor por 1 USD")
    print("-" * 52)

    for codigo, nombre in monedas.items():
        _, valor = extraer_primero(datos, codigo)
        print(f"{nombre:<20} {codigo:<10} {valor:,.4f}")

    print("-" * 52)
    print(f"Moneda base: USD (dólar estadounidense)")
    print(f"Última actualización: {fecha}")
    print("=" * 52)


def convertir_moneda(datos):
    monedas = {
        "CLP": "Peso chileno",
        "EUR": "Euro",
        "GBP": "Libra esterlina",
        "BRL": "Real brasileño",
        "ARS": "Peso argentino",
        "PEN": "Sol peruano",
        "MXN": "Peso mexicano",
    }

    print("\n--- CONVERSOR DE MONEDAS ---")
    print("Monedas disponibles:")

    for codigo, nombre in monedas.items():
        print(f"  {codigo} - {nombre}")

    try:
        cantidad = float(input("\nCantidad en USD: "))

        if not math.isfinite(cantidad) or cantidad < 0:
            print("Ingresa una cantidad válida.")
            return

        moneda = input("Moneda de destino: ").strip().upper()

        if moneda not in monedas:
            print("La moneda seleccionada no está disponible.")
            return

        fecha, tasa = extraer_primero(datos, moneda)
        resultado = cantidad * tasa

        print("\n" + "=" * 42)
        print("          RESULTADO DE CONVERSIÓN")
        print("=" * 42)
        print(f"Cantidad inicial : USD {cantidad:,.2f}")
        print(f"Moneda destino   : {moneda} ({monedas[moneda]})")
        print(f"Tasa de cambio   : {tasa:,.4f}")
        print(f"Resultado        : {resultado:,.2f} {moneda}")
        print(f"Actualización    : {fecha}")
        print("=" * 42)

    except ValueError:
        print("Debes ingresar una cantidad numérica válida.")
    except (KeyError, TypeError):
        print("No se pudo procesar el valor de la moneda.")


def main():
    try:
        datos = obtener_datos()
    except (requests.RequestException, ValueError) as error:
        print(f"No se pudieron obtener los valores de la API: {error}")
        return

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            try:
                consultar_monedas(datos)
            except (ValueError, KeyError, TypeError) as error:
                print(f"Error al consultar las monedas: {error}")

        elif opcion == "2":
            convertir_moneda(datos)

        elif opcion == "3":
            print("\nSaliendo del conversor de monedas...")
            break

        else:
            print("\nOpción inválida. Selecciona 1, 2 o 3.")


if __name__ == "__main__":
    main()