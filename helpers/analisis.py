#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
helpers/analisis.py
Módulo de análisis y descripción del clima.

Genera descripciones textuales legibles del estado meteorológico
a partir de datos estructurados (temperatura, humedad, presión, lluvia).

Funciones:
    describir_clima: Genera un resumen descriptivo del clima actual.

Autor: Hanzzel Corp
Licencia: MIT
Versión: 1.0.0
"""


def describir_clima(datos: dict) -> str:
    """
    Genera una descripción textual del clima a partir de datos meteorológicos.

    Args:
        datos (dict): Diccionario con las siguientes claves:
            - temp (float): Temperatura en grados Celsius
            - humedad (float): Porcentaje de humedad relativa
            - presion (float): Presión atmosférica en hPa
            - lluvia (float): Precipitación en mm/h

    Returns:
        str: Descripción formateada del clima con emojis y valores formateados.

    Reglas de interpretación:
        - Lluvia > 1.0 mm/h: Alta probabilidad de lluvia
        - Humedad > 70% + Presión < 1010 hPa: Ambiente húmedo e inestable
        - Temperatura > 33°C: Calor extremo, riesgo de golpe térmico
        - Temperatura < 10°C: Frío intenso, posible helada
        - Si ninguna condición crítica: Condiciones estables y cielo variable
    """
    t, h, p, l = datos["temp"], datos["humedad"], datos["presion"], datos["lluvia"]
    desc = []

    if l > 1.0:
        desc.append("alta probabilidad de lluvia o llovizna")
    if h > 70 and p < 1010:
        desc.append("ambiente húmedo e inestable")
    if t > 33:
        desc.append("calor extremo, riesgo de golpe térmico")
    if t < 10:
        desc.append("frío intenso, posible helada")
    if not desc:
        desc.append("condiciones estables y cielo variable")

    sensacion = " y ".join(desc)
    return (
        f"🌦️ Clima actual:\n"
        f"🌡️ Temp: {t:.1f} °C\n"
        f"💧 Humedad: {h:.0f}%\n"
        f"🌀 Presión: {p:.0f} hPa\n"
        f"☁️ {sensacion.capitalize()}."
    )
