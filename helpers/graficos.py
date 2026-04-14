#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
helpers/graficos.py
Módulo de generación de visualizaciones climáticas.

Crea gráficos de temperatura a partir del historial de mediciones
almacenado en el archivo CSV. Utiliza matplotlib para generar
imágenes que pueden ser enviadas mediante el bot de Telegram.

Funciones:
    generar_grafico_clima: Genera gráfico de temperatura reciente.

Dependencias:
    - pandas: Lectura y manipulación de datos CSV.
    - matplotlib: Generación de gráficos.

Autor: Hanzzel Corp
Licencia: MIT
Versión: 1.0.0
"""

import pandas as pd
import matplotlib.pyplot as plt
import os


def generar_grafico_clima(archivo_csv: str = "clima_log.csv", salida: str = "grafico_temp.png") -> str | None:
    """
    Genera un gráfico de línea con la evolución de temperatura reciente.

    Lee las últimas 30 mediciones del archivo CSV y crea un gráfico
    de temperatura vs tiempo. El resultado se guarda como imagen PNG.

    Args:
        archivo_csv (str): Ruta al archivo CSV con el historial de datos.
            Default: "clima_log.csv"
        salida (str): Nombre del archivo de imagen generado.
            Default: "grafico_temp.png"

    Returns:
        str | None: Nombre del archivo generado si tiene éxito,
            None si no hay datos suficientes o error.

    Requisitos:
        - El CSV debe contener columnas 'fecha' y 'temp'.
        - Se requieren al menos 2 registros para generar un gráfico.

    Example:
        >>> grafico = generar_grafico_clima("clima_log.csv", "mi_grafico.png")
        >>> if grafico:
        ...     print(f"Gráfico guardado: {grafico}")
    """
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
