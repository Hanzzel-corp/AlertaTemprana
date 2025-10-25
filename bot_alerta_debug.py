#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌦️ AlertaTemprana v4.0 — Bot Inteligente + Predicción + Visualización
Autor: Hanzzel Corp ∑Δ9
Licencia: MIT

Ahora incluye:
- 🔮 Predicción meteorológica 6h (Prophet)
- ⚠️ Alertas automáticas (temperatura, humedad, lluvia)
- 📊 Gráfico de temperatura
- 💬 Teclado interactivo en Telegram
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


# Intervalos
INTERVALO_CLIMA = 1800  # 30 min
INTERVALO_COMANDOS = 2  # 2 seg

# Variables globales
LAST_UPDATE_ID = None
ULTIMA_IMAGEN = None
ULTIMO_RESUMEN = None
CHAT_ID = None
UBICACION = cargar_ubicacion() or {
    "ciudad": "Buenos Aires",
    "lat": -34.6037,
    "lon": -58.3816,
}


# --- Funciones de envío ---
def enviar_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg})
    except Exception as e:
        print("⚠️ Error al enviar mensaje:", e)


def enviar_imagen_telegram(imagen, texto, hora):
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


def mostrar_menu_principal(chat_id):
    """Muestra el teclado interactivo"""
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


# --- Obtener CHAT_ID automático ---
def detectar_chat_id():
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


def cargar_chat_id():
    global CHAT_ID
    if os.path.exists("chat_id.json"):
        with open("chat_id.json") as f:
            CHAT_ID = json.load(f)["chat_id"]
            print(f"📡 CHAT_ID cargado: {CHAT_ID}")
    else:
        detectar_chat_id()


# --- Lector de comandos ---
def lector_comandos():
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


# --- Ciclo principal del clima ---
def ciclo_clima():
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


# --- Inicio ---
if __name__ == "__main__":
    print("🚀 Iniciando AlertaTemprana v4.0 — Inteligente + Visual")
    cargar_chat_id()
    threading.Thread(target=lector_comandos, daemon=True).start()
    ciclo_clima()


