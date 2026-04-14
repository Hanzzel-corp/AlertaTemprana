#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
helpers/geolocalizacion.py
Módulo de geolocalización y gestión de ubicación del usuario.

Proporciona funciones para convertir nombres de ciudades en coordenadas
geográficas (latitud/longitud) usando la API de Nominatim (OpenStreetMap),
y para persistir la ubicación del usuario en un archivo JSON local.

Funciones:
    obtener_por_nombre: Convierte nombre de ciudad a coordenadas.
    guardar_ubicacion: Persiste la ubicación en archivo JSON.
    cargar_ubicacion: Recupera la ubicación guardada.

Dependencias:
    - requests: Para llamadas HTTP a la API de Nominatim.

Autor: Hanzzel Corp
Licencia: MIT
Versión: 1.0.0
"""

import os
import json
import requests

CONFIG_FILE = "ubicacion_usuario.json"


def obtener_por_nombre(ciudad: str) -> dict | None:
    """
    Convierte el nombre de una ciudad en coordenadas geográficas.

    Utiliza la API de Nominatim (OpenStreetMap) para geocodificación.
    Incluye User-Agent requerido por los términos de servicio de Nominatim.

    Args:
        ciudad (str): Nombre de la ciudad a buscar (ej: "Buenos Aires", "Córdoba").

    Returns:
        dict | None: Diccionario con la información de ubicación:
            - ciudad (str): Nombre formateado de la ciudad
            - lat (float): Latitud en grados decimales
            - lon (float): Longitud en grados decimales
        Retorna None si la ciudad no se encuentra o hay error de conexión.

    Example:
        >>> ubicacion = obtener_por_nombre("Mendoza")
        >>> print(f"{ubicacion['ciudad']}: {ubicacion['lat']}, {ubicacion['lon']}")
    """
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={ciudad}&format=json&limit=1"
        r = requests.get(url, headers={"User-Agent": "HanzzelCorp-AlertaBot"}, timeout=10)
        data = r.json()
        if not data:
            return None
        return {"ciudad": ciudad.title(), "lat": float(data[0]["lat"]), "lon": float(data[0]["lon"])}
    except Exception:
        return None

def guardar_ubicacion(info: dict) -> None:
    """
    Guarda la ubicación del usuario en un archivo JSON local.

    Args:
        info (dict): Diccionario con claves 'ciudad', 'lat', 'lon'.

    Nota:
        El archivo se guarda en UTF-8 para soportar caracteres especiales
        en nombres de ciudades.
    """
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2, ensure_ascii=False)

def cargar_ubicacion() -> dict | None:
    """
    Carga la ubicación guardada del usuario desde el archivo JSON.

    Returns:
        dict | None: Diccionario con datos de ubicación si existe,
        None si no hay archivo guardado.
    """
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

