# -*- coding: utf-8 -*-
"""
📈 Generación de gráficos climáticos
Autor: Hanzzel Corp ∑Δ9
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

def generar_grafico_clima(archivo_csv="clima_log.csv", salida="grafico_temp.png"):
    if not os.path.exists(archivo_csv):
        return None

    df = pd.read_csv(archivo_csv).tail(30)
    if "fecha" not in df.columns or "temp" not in df.columns:
        return None

    plt.figure(figsize=(6, 3))
    plt.plot(df["fecha"], df["temp"], linewidth=2)
    plt.title("📈 Temperatura Reciente")
    plt.xticks(rotation=45)
    plt.xlabel("Tiempo")
    plt.ylabel("°C")
    plt.tight_layout()
    plt.savefig(salida)
    plt.close()
    return salida
