## Laboratorio N3
## Bredy Guerra

import os
import time
from datetime import datetime

import requests
from dotenv import load_dotenv

import db_manager

load_dotenv()

# API publica de clima: https://open-meteo.com/en/docs (no necesita API key)
URL = os.getenv("URL_API", "https://api.open-meteo.com/v1/forecast")
CIUDAD_POR_DEFECTO = os.getenv("CIUDAD_POR_DEFECTO", "panama")

# Coordenadas de las ciudades disponibles
CIUDADES = {
    "david": (8.43, -82.43),
    "panama": (8.98, -79.52),
    "santiago": (8.10, -80.98),
    "chitre": (7.96, -80.43),
    "colon": (9.36, -79.90)
}

# La API devuelve la condicion como un numero (codigo WMO)
CONDICIONES = {
    0: "Despejado", 1: "Mayormente despejado", 2: "Parcialmente nublado",
    3: "Nublado", 45: "Niebla", 51: "Llovizna", 61: "Lluvia ligera",
    63: "Lluvia", 65: "Lluvia intensa", 80: "Chubascos", 95: "Tormenta"
}


def obtener_clima(ciudad):
    if ciudad.lower() not in CIUDADES:
        print("Ciudad no disponible. Opciones:", ", ".join(CIUDADES))
        return None

    latitud, longitud = CIUDADES[ciudad.lower()]

    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "current": "temperature_2m,relative_humidity_2m,weather_code"
    }

    # 3 intentos con backoff simple (1, 2 y 3 segundos)
    for intento in range(1, 4):
        try:
            respuesta = requests.get(URL, params=parametros, timeout=10)

            if respuesta.status_code == 200:
                datos = respuesta.json()["current"]
                return {
                    "temperatura": datos["temperature_2m"],
                    "humedad": datos["relative_humidity_2m"],
                    "condicion": CONDICIONES.get(datos["weather_code"], "Desconocida")
                }

            elif respuesta.status_code == 404:
                print("Error 404: la direccion de la API no existe.")
                return None

            else:
                print(f"Error {respuesta.status_code} (intento {intento} de 3)")

        except requests.exceptions.RequestException:
            print(f"Error de conexion (intento {intento} de 3)")

        time.sleep(intento)

    print("No se pudo conectar con la API.")
    return None


def main():
    db_manager.crear_base_datos()

    entrada = input(f"Escriba una ciudad [{CIUDAD_POR_DEFECTO}]: ").strip()
    ciudad = entrada if entrada else CIUDAD_POR_DEFECTO

    clima = obtener_clima(ciudad)

    if clima is None:
        return

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    db_manager.crear_reporte(
        ciudad.title(),
        clima["temperatura"],
        clima["humedad"],
        clima["condicion"],
        fecha
    )

    print("\n--- CLIMA ACTUAL ---")
    print(f"Ciudad      : {ciudad.title()}")
    print(f"Temperatura : {clima['temperatura']} C")
    print(f"Humedad     : {clima['humedad']} %")
    print(f"Condicion   : {clima['condicion']}")
    print(f"Fecha       : {fecha}")

    print("\nREPORTES GUARDADOS:")
    db_manager.leer_reportes()


if __name__ == "__main__":
    main()
