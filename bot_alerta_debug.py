#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bot_alerta_debug.py
Script principal del Bot de Alerta Temprana Meteorológica.

Bot interactivo de Telegram que proporciona información meteorológica
en tiempo real, incluyendo:
    - Clima actual con datos triangulados (Open-Meteo + SMN)
    - Predicciones de temperatura usando Prophet (6h horizonte)
    - Alertas automáticas por condiciones críticas
    - Imágenes satelitales de NASA GOES
    - Gráficos históricos de temperatura
    - Geolocalización configurable por ciudad

Arquitectura:
    - Hilo principal: Ciclo de actualización climática cada 30 minutos
    - Hilo secundario: Escucha de comandos Telegram cada 2 segundos
    - Persistencia: CSV para historial, JSON para configuración

Comandos soportados:
    /start, /help → Muestra menú interactivo
    /tiempo, "🌦️ Clima" → Clima actual
    /radar, "🛰️ Radar" → Imagen satelital
    /grafico, "📊 Gráfico" → Gráfico de temperatura
    /ubicacion <ciudad> → Cambiar ubicación
    /ubicacion_actual → Mostrar ubicación actual

Variables de entorno (desde config.py):
    TELEGRAM_TOKEN: Token del bot de Telegram (requerido)
    CHAT_ID: ID del chat (se detecta automáticamente)
    LAT, LON: Coordenadas geográficas

Autor: Hanzzel Corp
Licencia: MIT
Versión: 4.0.0
"""

import time
import datetime
import threading
import requests
import json
import os
from helpers.fuentes import obtener_datos_triangulados_debug
from helpers.analisis import describir_clima
from helpers.logger import registrar_datos
from helpers.satelite import obtener_imagen_satelital
from helpers.geolocalizacion import obtener_por_nombre, guardar_ubicacion, cargar_ubicacion
from helpers.prediccion import predecir_tendencia, evaluar_alertas
from helpers.graficos import generar_grafico_clima
from config import TELEGRAM_TOKEN


# ---------- CONFIGURACIÓN DE INTERVALOS ----------
INTERVALO_CLIMA = 1800      # Segundos entre actualizaciones (30 minutos)
INTERVALO_COMANDOS = 2      # Segundos entre polling de comandos (2 segundos)

# ---------- VARIABLES GLOBALS ----------
LAST_UPDATE_ID: int | None = None   # ID de última actualización de Telegram
ULTIMA_IMAGEN: str | None = None     # Ruta de última imagen satelital generada
ULTIMO_RESUMEN: str | None = None    # Último resumen de clima enviado
CHAT_ID: int | None = None           # ID del chat de Telegram

# Carga ubicación guardada o usa Buenos Aires como default
UBICACION: dict = cargar_ubicacion() or {
    "ciudad": "Buenos Aires",
    "lat": -34.6037,
    "lon": -58.3816,
}


# ==========================================
# FUNCIONES DE ENVÍO A TELEGRAM
# ==========================================

def enviar_telegram(msg: str) -> None:
    """
    Envía un mensaje de texto al chat de Telegram configurado.

    Args:
        msg (str): Mensaje a enviar (soporta emojis).

    Nota:
        Requiere que CHAT_ID esté configurado. Los errores se capturan
        y loggean en consola sin interrumpir el flujo.
    """
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg})
    except Exception as e:
        print("⚠️ Error al enviar mensaje:", e)


def enviar_imagen_telegram(imagen: str, texto: str, hora: str) -> None:
    """
    Envía una imagen al chat de Telegram con caption informativo.

    Args:
        imagen (str): Ruta al archivo de imagen local.
        texto (str): Descripción del contenido de la imagen.
        hora (str): Timestamp para incluir en el caption.

    Nota:
        El caption se formatea automáticamente como: "🕓 {hora}\n{texto}"
    """
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        with open(imagen, "rb") as f:
            files = {"photo": f}
            data = {"chat_id": CHAT_ID, "caption": f"🕓 {hora}\n{texto}"}
            r = requests.post(url, data=data, files=files)
        if r.status_code == 200:
            print("📡 Imagen enviada ✅")
        else:
            print("⚠️ Error al enviar imagen:", r.text)
    except Exception as e:
        print("⚠️ No se pudo enviar imagen:", e)


def mostrar_menu_principal(chat_id: int) -> None:
    """
    Muestra el teclado interactivo personalizado en Telegram.

    Presenta un menú de botones persistente para acceso rápido
    a las funciones principales del bot.

    Args:
        chat_id (int): Identificador del chat de Telegram.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    keyboard = {
        "keyboard": [
            ["🌦️ Clima", "🛰️ Radar"],
            ["📊 Gráfico", "📍 Ubicación actual"]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }
    data = {"chat_id": chat_id, "text": "Seleccioná una opción:", "reply_markup": keyboard}
    requests.post(url, json=data)


# ==========================================
# GESTIÓN DE CHAT ID
# ==========================================

def detectar_chat_id() -> None:
    """
    Detecta automáticamente el CHAT_ID desde mensajes entrantes.

    Consulta las actualizaciones pendientes de Telegram y extrae
    el chat_id del primer mensaje disponible. Guarda el valor
    en 'chat_id.json' para persistencia entre reinicios.
    """
    global CHAT_ID
    try:
        r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates", timeout=5)
        data = r.json().get("result", [])
        for u in data:
            if "message" in u:
                CHAT_ID = u["message"]["chat"]["id"]
                with open("chat_id.json", "w") as f:
                    json.dump({"chat_id": CHAT_ID}, f)
                print(f"✅ CHAT_ID detectado: {CHAT_ID}")
                return
    except Exception:
        pass


def cargar_chat_id() -> None:
    """
    Carga el CHAT_ID desde archivo JSON o intenta detectarlo.

    Prioridad:
        1. Archivo 'chat_id.json' si existe
        2. Detección automática desde API de Telegram
    """
    global CHAT_ID
    if os.path.exists("chat_id.json"):
        with open("chat_id.json") as f:
            CHAT_ID = json.load(f)["chat_id"]
            print(f"📡 CHAT_ID cargado: {CHAT_ID}")
    else:
        detectar_chat_id()


# ==========================================
# GESTIÓN DE COMANDOS
# ==========================================

def lector_comandos() -> None:
    """
    Hilo dedicado a escuchar y procesar comandos de Telegram.

    Ejecuta polling continuo de la API getUpdates, procesando:
        - Comandos de ubicación (/ubicacion, /ubicacion_actual)
        - Consultas de clima (/tiempo, "🌦️ Clima")
        - Imágenes satelitales (/radar, "🛰️ Radar")
        - Gráficos de temperatura (/grafico, "📊 Gráfico")
        - Ayuda y menú (/start, /help)

    Nota:
        Esta función se ejecuta en un hilo daemon para no bloquear
        el ciclo principal de actualización climática.
    """
    global LAST_UPDATE_ID, UBICACION
    print("🎧 Lector de comandos iniciado...")
    while True:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
            params = {"timeout": 1}
            if LAST_UPDATE_ID:
                params["offset"] = LAST_UPDATE_ID + 1

            r = requests.get(url, params=params, timeout=5)
            data = r.json()
            updates = data.get("result", [])

            if not updates:
                time.sleep(INTERVALO_COMANDOS)
                continue

            LAST_UPDATE_ID = updates[-1]["update_id"]

            for u in updates:
                msg = u.get("message", {})
                text = msg.get("text", "")
                if not text:
                    continue

                t = text.strip().lower()
                print(f"💬 Comando recibido: {t}")

                if t.startswith("/ubicacion") or "📍" in t:
                    partes = text.split(" ", 1)
                    if len(partes) == 1:
                        enviar_telegram("📍 Uso: /ubicacion <ciudad>")
                        continue
                    ciudad = partes[1].strip()
                    nueva = obtener_por_nombre(ciudad)
                    if nueva:
                        UBICACION = nueva
                        guardar_ubicacion(nueva)
                        enviar_telegram(f"✅ Ubicación actualizada a {ciudad.title()} "
                                        f"({nueva['lat']:.4f}, {nueva['lon']:.4f})")
                    else:
                        enviar_telegram(f"⚠️ No se encontró la ciudad '{ciudad}'.")

                elif t == "/ubicacion_actual" or "ubicación actual" in t:
                    enviar_telegram(f"📍 {UBICACION['ciudad']} "
                                    f"({UBICACION['lat']:.4f}, {UBICACION['lon']:.4f})")

                elif t in ["/tiempo", "🌦️ clima"]:
                    if ULTIMO_RESUMEN:
                        enviar_telegram(f"🌦️ Clima actual en {UBICACION['ciudad']}:\n{ULTIMO_RESUMEN}")
                    else:
                        enviar_telegram("⚠️ Aún no hay datos. Espera próxima actualización.")

                elif t in ["/radar", "🛰️ radar"]:
                    if ULTIMA_IMAGEN and os.path.exists(ULTIMA_IMAGEN):
                        enviar_imagen_telegram(ULTIMA_IMAGEN, "🛰️ Última imagen satelital", datetime.datetime.now().strftime("%H:%M:%S"))
                    else:
                        enviar_telegram("⚠️ No hay imagen disponible todavía.")

                elif t in ["/grafico", "📊 gráfico"]:
                    g = generar_grafico_clima()
                    if g:
                        enviar_imagen_telegram(g, "📈 Temperatura reciente", datetime.datetime.now().strftime("%H:%M:%S"))
                    else:
                        enviar_telegram("⚠️ No hay suficientes datos para graficar.")

                elif t in ["/start", "/help"]:
                    mostrar_menu_principal(CHAT_ID)
                    enviar_telegram(
                        "🧭 Comandos:\n"
                        "/tiempo → clima actual\n"
                        "/radar → última imagen satelital\n"
                        "/grafico → gráfico de temperatura\n"
                        "/ubicacion <ciudad> → cambia ubicación\n"
                        "/ubicacion_actual → muestra ubicación actual"
                    )

        except Exception as e:
            print("⚠️ Error en lector de comandos:", e)
            time.sleep(3)


# ==========================================
# CICLO PRINCIPAL DE CLIMA
# ==========================================

def ciclo_clima() -> None:
    """
    Bucle principal de actualización meteorológica automática.

    Ejecuta cada INTERVALO_CLIMA segundos (default: 30 min):
        1. Obtiene datos triangulados de fuentes meteorológicas
        2. Registra datos en CSV para historial
        3. Evalúa y envía alertas si hay condiciones críticas
        4. Genera predicción de temperatura (Prophet)
        5. Descarga y envía imagen satelital
        6. Envía resumen de clima al chat

    Nota:
        Este es el hilo principal del programa. Nunca retorna.
    """
    global ULTIMA_IMAGEN, ULTIMO_RESUMEN
    while True:
        try:
            hora = datetime.datetime.now().strftime("%H:%M:%S")
            datos, fuentes = obtener_datos_triangulados_debug()
            resumen = describir_clima(datos)
            ULTIMO_RESUMEN = resumen
            registrar_datos(datos, "Open-Meteo")

            # Alertas automáticas
            alertas = evaluar_alertas(datos)
            for a in alertas:
                enviar_telegram(f"⚠️ {a}")

            # Predicción
            pred = predecir_tendencia()
            if pred:
                enviar_telegram(f"🔮 Predicción a {pred['hora']}: {pred['temp_pred']} °C estimados.")

            # Imagen satelital
            imagen = obtener_imagen_satelital(datos)
            if imagen:
                ULTIMA_IMAGEN = imagen
                enviar_imagen_telegram(imagen, resumen, hora)
            else:
                enviar_telegram(f"🕓 {hora}\n{resumen}")

        except Exception as e:
            print("❌ Error en ciclo de clima:", e)

        time.sleep(INTERVALO_CLIMA)


# ==========================================
# PUNTO DE ENTRADA
# ==========================================

if __name__ == "__main__":
    print("🚀 Iniciando AlertaTemprana v4.0 — Inteligente + Visual")
    print("=" * 50)
    print("📡 Bot Meteorológico con Telegram")
    print("🌍 Fuentes: Open-Meteo + SMN Argentina")
    print("🔮 Predicción: Prophet (Facebook)")
    print("🛰️ Imágenes: NASA GOES")
    print("=" * 50)

    cargar_chat_id()

    # Inicia hilo de comandos en background
    threading.Thread(target=lector_comandos, daemon=True).start()
    print("🎧 Lector de comandos iniciado en hilo paralelo")

    # Inicia ciclo principal de clima (bloqueante)
    ciclo_clima()


