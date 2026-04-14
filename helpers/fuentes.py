#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
helpers/fuentes.py
Módulo de obtención de datos meteorológicos desde fuentes externas.

Integra múltiples fuentes de datos climáticos:
    - Open-Meteo: API global de pronóstico meteorológico gratuito
    - SMN Argentina: Servicio Meteorológico Nacional (datos de estaciones locales)

Funciones:
    open_meteo: Obtiene datos desde la API de Open-Meteo.
    smn_weather: Obtiene datos desde estaciones del SMN Argentina.
    obtener_datos_triangulados_debug: Combina ambas fuentes con ponderación.

Autor: Hanzzel Corp
Licencia: MIT
Versión: 1.1.0
"""

import requests
from config import LAT, LON


# Peso de ponderación para triangulación: [Open-Meteo, SMN]
PESO_FUENTES = [0.6, 0.4]

def open_meteo() -> dict:
    """
    Obtiene datos meteorológicos actuales desde la API de Open-Meteo.

    La API de Open-Meteo proporciona datos de pronóstico gratuito
    sin necesidad de API key. Consulta temperatura, humedad, presión
    y precipitación para las coordenadas configuradas.

    Returns:
        dict: Datos meteorológicos con claves:
            - temp (float): Temperatura en °C
            - humedad (float): Humedad relativa en %
            - presion (float): Presión atmosférica en hPa
            - lluvia (float): Precipitación en mm
        En caso de error, retorna valores en cero.

    Raises:
        No lanza excepciones. Los errores se capturan y loggean.
    """
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={LAT}&longitude={LON}"
            f"&current=temperature_2m,relative_humidity_2m,surface_pressure,precipitation"
            f"&timezone=America/Argentina/Buenos_Aires"
        )
        d = requests.get(url, timeout=10).json().get("current", {})
        return {
            "temp": d.get("temperature_2m", 0.0),
            "humedad": d.get("relative_humidity_2m", 0.0),
            "presion": d.get("surface_pressure", 0.0),
            "lluvia": d.get("precipitation", 0.0),
        }
    except Exception as e:
        print("⚠️ Open-Meteo falló:", e)
        return {"temp": 0, "humedad": 0, "presion": 0, "lluvia": 0}


# ---------- SMN ARGENTINA ----------
def smn_weather() -> dict:
    """
    Obtiene datos meteorológicos desde el Servicio Meteorológico Nacional (SMN) de Argentina.

    Consulta el endpoint público del SMN y selecciona la estación meteorológica
    más cercana a las coordenadas configuradas (LAT, LON). Filtra estaciones
    con datos válidos (excluye valores nulos o vacíos).

    Returns:
        dict: Datos meteorológicos con claves:
            - temp (float): Temperatura en °C
            - humedad (float): Humedad relativa en %
            - presion (float): Presión atmosférica en hPa
            - lluvia (float): Precipitación en mm
        En caso de error o sin datos válidos, retorna valores en cero.

    Nota:
        El SMN solo cubre territorio argentino. Para ubicaciones fuera
        de Argentina, esta fuente retornará ceros.
    """
    try:
        r = requests.get("https://ws.smn.gob.ar/map_items/weather", timeout=10)
        estaciones = r.json()

        estaciones_validas = []
        for e in estaciones:
            try:
                lat = float(e.get("lat", 0))
                lon = float(e.get("lon", 0))
                temp = e.get("temp")
                hum = e.get("humidity")
                pres = e.get("pressure")
                if all(
                    x not in (None, "", "N/A", 0, "0")
                    for x in (temp, hum, pres)
                ):
                    estaciones_validas.append((e, lat, lon))
            except Exception:
                continue

        if not estaciones_validas:
            print("⚠️ SMN sin datos válidos — se omite fuente.")
            return {"temp": 0, "humedad": 0, "presion": 0, "lluvia": 0}

        estacion_cercana, _, _ = min(
            estaciones_validas,
            key=lambda e: (e[1] - LAT) ** 2 + (e[2] - LON) ** 2,
        )

        nombre = estacion_cercana.get("name", "Desconocido")
        temp = float(estacion_cercana.get("temp", 0))
        humedad = float(estacion_cercana.get("humidity", 0))
        presion = float(estacion_cercana.get("pressure", 0))
        lluvia = float(estacion_cercana.get("rain", 0) or 0)
        print(f"📍 Estación SMN usada: {nombre}")

        return {"temp": temp, "humedad": humedad, "presion": presion, "lluvia": lluvia}

    except Exception as e:
        print("⚠️ SMN falló:", e)
        return {"temp": 0, "humedad": 0, "presion": 0, "lluvia": 0}

def obtener_datos_triangulados_debug() -> tuple:
    """
    Combina datos de múltiples fuentes meteorológicas con ponderación.

    Obtiene datos simultáneamente de Open-Meteo y SMN Argentina, luego
    los combina usando ponderaciones configurables. Si SMN no tiene datos
    válidos (por ejemplo, ubicación fuera de Argentina), usa solo Open-Meteo.

    La ponderación actual es:
        - Open-Meteo: 60% (mayor cobertura global)
        - SMN: 40% (mayor precisión local en Argentina)

    Returns:
        tuple: (datos_combinados, fuentes_individuales)
            - datos_combinados (dict): Datos ponderados con las mismas claves
            - fuentes_individuales (dict): Datos originales de cada fuente
              bajo las claves "Open-Meteo" y "SMN"

    Example:
        >>> datos, fuentes = obtener_datos_triangulados_debug()
        >>> print(f"Temp: {datos['temp']:.1f}°C")
        >>> print(f"Fuentes: {fuentes.keys()}")
    """
    f1 = open_meteo()
    f2 = smn_weather()

    # Si SMN no devuelve datos válidos, usa solo Open-Meteo
    if f2["temp"] == 0 and f2["humedad"] == 0:
        print("ℹ️ Solo Open-Meteo tiene datos válidos.")
        datos = f1
    else:
        peso = PESO_FUENTES
        datos = {
            "temp": f1["temp"] * peso[0] + f2["temp"] * peso[1],
            "humedad": f1["humedad"] * peso[0] + f2["humedad"] * peso[1],
            "presion": f1["presion"] * peso[0] + f2["presion"] * peso[1],
            "lluvia": f1["lluvia"] * peso[0] + f2["lluvia"] * peso[1],
        }

    fuentes = {"Open-Meteo": f1, "SMN": f2}
    return datos, fuentes





