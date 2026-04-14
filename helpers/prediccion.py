#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
helpers/prediccion.py
Módulo de predicción meteorológica y alertas automáticas.

Proporciona capacidades de forecasting usando Facebook Prophet para
predecir temperaturas futuras, y evaluación de condiciones críticas
para disparar alertas automáticas.

Funciones:
    predecir_tendencia: Predice temperatura futura usando Prophet.
    evaluar_alertas: Evalúa condiciones críticas y genera alertas.

Dependencias:
    - pandas: Manipulación de series temporales.
    - prophet: Modelo de forecasting (Facebook Prophet).

Autor: Hanzzel Corp
Licencia: MIT
Versión: 1.0.0
"""

import pandas as pd
from prophet import Prophet
import datetime
import os


def predecir_tendencia(archivo_csv: str = "clima_log.csv", horas: int = 6) -> dict | None:
    """
    Predice la temperatura futura usando el modelo Prophet.

    Entrena un modelo Prophet con el historial de temperaturas y
    genera predicciones para las próximas N horas.

    Args:
        archivo_csv (str): Ruta al CSV con historial de temperaturas.
            Debe contener columnas 'fecha' y 'temp'.
        horas (int): Horizonte de predicción en horas. Default: 6.

    Returns:
        dict | None: Predicción con claves:
            - hora (str): Hora de la predicción (formato HH:MM)
            - temp_pred (float): Temperatura predicha en °C
        Retorna None si no hay datos suficientes.

    Nota:
        Prophet requiere al menos 2 días de datos históricos
        para generar predicciones confiables.

    Example:
        >>> pred = predecir_tendencia("clima_log.csv", horas=6)
        >>> if pred:
        ...     print(f"Temperatura estimada a las {pred['hora']}: {pred['temp_pred']}°C")
    """
    if not os.path.exists(archivo_csv):
        return None

    df = pd.read_csv(archivo_csv)
    if "fecha" not in df.columns or "temp" not in df.columns:
        return None

    df["ds"] = pd.to_datetime(df["fecha"])
    df["y"] = df["temp"]

    modelo = Prophet(interval_width=0.8)
    modelo.fit(df[["ds", "y"]])

    futuro = modelo.make_future_dataframe(periods=horas, freq="H")
    pred = modelo.predict(futuro)
    pred_temp = pred.tail(horas)[["ds", "yhat"]]

    proximo = pred_temp.iloc[-1]
    return {
        "hora": proximo["ds"].strftime("%H:%M"),
        "temp_pred": round(proximo["yhat"], 1)
    }


def evaluar_alertas(datos: dict) -> list:
    """
    Evalúa condiciones meteorológicas críticas y genera alertas.

    Analiza los datos actuales contra umbrales predefinidos de
    temperatura, precipitación y humedad para identificar situaciones
    de riesgo que requieren notificación al usuario.

    Args:
        datos (dict): Diccionario con mediciones actuales:
            - temp (float): Temperatura en °C
            - lluvia (float): Precipitación en mm/h
            - humedad (float): Humedad relativa en %

    Returns:
        list: Lista de strings con mensajes de alerta.
            Lista vacía si no hay condiciones críticas.

    Umbrales de alerta:
        - Temperatura > 35°C: Ola de calor
        - Temperatura < 0°C: Riesgo de heladas
        - Lluvia > 20 mm/h: Lluvias intensas
        - Humedad > 90%: Humedad extrema

    Example:
        >>> datos = {"temp": 36.5, "lluvia": 0, "humedad": 85}
        >>> alertas = evaluar_alertas(datos)
        >>> for alerta in alertas:
        ...     print(alerta)
        🔥 Ola de calor detectada (>35°C)
    """
    alertas = []

    if datos["temp"] > 35:
        alertas.append("🔥 Ola de calor detectada (>35°C)")
    elif datos["temp"] < 0:
        alertas.append("🥶 Riesgo de heladas (T<0°C)")

    if datos["lluvia"] > 20:
        alertas.append("🌧️ Lluvias intensas (>20 mm/h)")

    if datos["humedad"] > 90:
        alertas.append("💧 Humedad extrema (>90%)")

    return alertas
