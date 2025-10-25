# -*- coding: utf-8 -*-
"""
🤖 Predicción y alertas automáticas
Autor: Hanzzel Corp ∑Δ9
"""

import pandas as pd
from prophet import Prophet
import datetime
import os

def predecir_tendencia(archivo_csv="clima_log.csv", horas=6):
    """Predice la temperatura y humedad a futuro usando Prophet"""
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


def evaluar_alertas(datos):
    """Evalúa si deben dispararse alertas meteorológicas"""
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
