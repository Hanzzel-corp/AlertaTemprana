#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
helpers/logger.py
Módulo de registro y persistencia de datos meteorológicos.

Gestiona el almacenamiento histórico de mediciones climáticas en formato CSV,
permitiendo análisis temporales y generación de gráficos.

El archivo de log (clima_log.csv) contiene:
    - Fecha y hora de cada medición
    - Temperatura, humedad, presión y precipitación
    - Fuente de datos utilizada

Funciones:
    registrar_datos: Guarda una nueva medición en el archivo CSV.

Dependencias:
    - csv: Manipulación de archivos CSV.
    - datetime: Timestamps de las mediciones.

Autor: Hanzzel Corp
Licencia: MIT
Versión: 1.0.0
"""

import csv
from datetime import datetime
import os

LOG_FILE = "clima_log.csv"


def registrar_datos(datos: dict, fuente_activa: str = "Open-Meteo") -> None:
    """
    Registra una medición meteorológica en el archivo CSV de historial.

    Crea automáticamente el archivo si no existe, incluyendo la cabecera
    con los nombres de columnas.

    Args:
        datos (dict): Diccionario con mediciones climáticas:
            - temp (float): Temperatura en °C
            - humedad (float): Humedad relativa en %
            - presion (float): Presión atmosférica en hPa
            - lluvia (float): Precipitación en mm
        fuente_activa (str): Identificador de la fuente de datos
            (default: "Open-Meteo").

    Estructura del CSV:
        fecha, hora, temperatura, humedad, presion, lluvia, fuente

    Example:
        >>> medicion = {"temp": 22.5, "humedad": 65, "presion": 1013, "lluvia": 0}
        >>> registrar_datos(medicion, "Open-Meteo")
    """
    now = datetime.now()
    fila = {
        "fecha": now.strftime("%Y-%m-%d"),
        "hora": now.strftime("%H:%M:%S"),
        "temperatura": round(datos.get("temp", 0), 2),
        "humedad": round(datos.get("humedad", 0), 2),
        "presion": round(datos.get("presion", 0), 2),
        "lluvia": round(datos.get("lluvia", 0), 2),
        "fuente": fuente_activa
    }

    existe = os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fila.keys())
        if not existe:
            writer.writeheader()
        writer.writerow(fila)
