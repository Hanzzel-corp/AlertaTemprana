#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
helpers/satelite.py
Módulo de obtención y procesamiento de imágenes satelitales.

Descarga imágenes satelitales en tiempo real desde NASA GOES,
las procesa con overlays informativos (datos climáticos, ubicación),
y gestiona fallbacks offline cuando no hay conectividad.

Funciones:
    obtener_imagen_satelital: Descarga y procesa imagen satelital.

Dependencias:
    - requests: Descarga de imágenes HTTP.
    - Pillow (PIL): Procesamiento de imágenes.

Autor: Hanzzel Corp
Licencia: MIT
Versión: 1.0.0
"""

import requests
import datetime
from PIL import Image, ImageDraw, ImageFont
from config import LAT, LON


def obtener_imagen_satelital(datos: dict | None = None) -> str:
    """
    Descarga, procesa y guarda una imagen satelital con datos de clima.

    Intenta obtener la imagen más reciente de NASA GOES (Sudamérica).
    Si la descarga falla, genera una imagen de respaldo offline.
    Superpone información meteorológica sobre la imagen descargada.

    Args:
        datos (dict | None): Diccionario con datos climáticos para el overlay:
            - temp (float): Temperatura en °C
            - humedad (float): Humedad en %
            - presion (float): Presión en hPa
            Si es None, muestra mensaje de datos no disponibles.

    Returns:
        str: Nombre del archivo de imagen generado:
            - "satelite_YYYYMMDD_HHMMSS.png" si exitoso
            - "offline.png" si falla la descarga

    Proceso:
        1. Descarga imagen desde NASA GOES (timeout 12s)
        2. Valida que sea contenido de imagen
        3. Dibuja punto rojo indicando ubicación central
        4. Superpone barra con datos meteorológicos
        5. Guarda con timestamp único

    Fuentes:
        - NASA GOES: https://weather.msfc.nasa.gov/GOES/

    Example:
        >>> datos = {"temp": 22.5, "humedad": 65, "presion": 1013}
        >>> imagen = obtener_imagen_satelital(datos)
        >>> print(f"Imagen generada: {imagen}")
    """
    nombre = f"satelite_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

    # --- 1️⃣ Intentar NASA GOES Sudamérica ---
    try:
        url_nasa = "https://weather.msfc.nasa.gov/GOES/GOES16_SouthAmerica_10848x10848.jpg"
        print("🛰️ Descargando imagen desde NASA GOES...")
        r = requests.get(url_nasa, timeout=12)

        if r.status_code != 200 or "image" not in r.headers.get("Content-Type", ""):
            raise Exception("NASA GOES devolvió contenido no válido")

    except Exception as e:
        print(f"⚠️ NASA GOES falló ({e}). Usando imagen local de respaldo...")

        # Crear una imagen gris local si no hay conexión
        img = Image.new("RGB", (800, 800), (90, 90, 90))
        draw = ImageDraw.Draw(img)
        draw.text((300, 390), "Sin conexión satelital", fill=(255, 255, 255))
        img.save("offline.png")
        return "offline.png"

    # --- 2️⃣ Guardar imagen descargada ---
    with open(nombre, "wb") as f:
        f.write(r.content)

    # --- 3️⃣ Procesar imagen: marcar ubicación y datos ---
    try:
        img = Image.open(nombre).convert("RGBA")
        draw = ImageDraw.Draw(img)
        ancho, alto = img.size

        # Punto rojo central
        cx, cy = ancho // 2, alto // 2
        draw.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), fill="red", outline="white")

        # Cargar fuente (usa una genérica del sistema)
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()

        # Overlay con datos del clima
        if datos:
            texto = (
                f"Buenos Aires — {datos['temp']:.1f}°C / "
                f"{datos['humedad']:.0f}% H / {datos['presion']:.0f} hPa"
            )
        else:
            texto = "Clima actual — datos no disponibles"

        # Fondo semitransparente detrás del texto
        draw.rectangle((50, 50, ancho - 50, 160), fill=(0, 0, 0, 150))
        draw.text((70, 80), texto, font=font, fill=(255, 255, 255, 255))

        img.save(nombre)
        print(f"✅ Imagen satelital procesada y guardada: {nombre}")
        return nombre

    except Exception as e:
        print("⚠️ Error al procesar imagen satelital:", e)
        return "offline.png"





