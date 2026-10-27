import requests


def obtener_tiempo():
    respuesta = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": -33.4489,
            "longitude": -70.6693,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "apparent_temperature,"
                "wind_speed_10m"
            ),
            "timezone": "America/Santiago",
        },
        timeout=(3, 5),
    )

    respuesta.raise_for_status()
    return respuesta.json()


def mostrar_tiempo(datos):
    actual = datos["current"]

    print("=" * 40)
    print("       REPORTE DEL TIEMPO")
    print("=" * 40)
    print(f"Ciudad:              Santiago, Chile")
    print(f"Fecha y hora:        {actual['time']}")
    print("-" * 40)
    print(f"Temperatura:         {actual['temperature_2m']} °C")
    print(f"Sensación térmica:   {actual['apparent_temperature']} °C")
    print(f"Humedad:             {actual['relative_humidity_2m']} %")
    print(f"Velocidad del viento:{actual['wind_speed_10m']:>7} km/h")
    print("=" * 40)


try:
    datos = obtener_tiempo()
    mostrar_tiempo(datos)

except requests.exceptions.Timeout:
    print("Error: la conexión tardó demasiado.")

except requests.exceptions.RequestException as error:
    print(f"Error al consultar la API: {error}")

except (KeyError, TypeError, ValueError):
    print("Error: la respuesta de la API no tiene el formato esperado.")
