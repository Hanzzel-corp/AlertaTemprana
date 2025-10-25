import requests
from config import LAT, LON

# ---------- OPEN METEO ----------
def open_meteo():
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={LAT}&longitude={LON}"
            f"&current=temperature_2m,relative_humidity_2m,surface_pressure,precipitation"
            f"&timezone=America/Argentina/Buenos_Aires"
        )
        d = requests.get(url, timeout=10).json().get("current", {})
        return {
            "temp": d.get("temperature_2m", 0.0),
            "humedad": d.get("relative_humidity_2m", 0.0),
            "presion": d.get("surface_pressure", 0.0),
            "lluvia": d.get("precipitation", 0.0),
        }
    except Exception as e:
        print("⚠️ Open-Meteo falló:", e)
        return {"temp": 0, "humedad": 0, "presion": 0, "lluvia": 0}

# ---------- SMN ARGENTINA ----------
def smn_weather():
    """
    Usa el servicio público del SMN. Devuelve 0 si no hay datos válidos.
    """
    try:
        r = requests.get("https://ws.smn.gob.ar/map_items/weather", timeout=10)
        estaciones = r.json()

        estaciones_validas = []
        for e in estaciones:
            try:
                lat = float(e.get("lat", 0))
                lon = float(e.get("lon", 0))
                temp = e.get("temp")
                hum = e.get("humidity")
                pres = e.get("pressure")
                if all(
                    x not in (None, "", "N/A", 0, "0")
                    for x in (temp, hum, pres)
                ):
                    estaciones_validas.append((e, lat, lon))
            except Exception:
                continue

        if not estaciones_validas:
            print("⚠️ SMN sin datos válidos — se omite fuente.")
            return {"temp": 0, "humedad": 0, "presion": 0, "lluvia": 0}

        estacion_cercana, _, _ = min(
            estaciones_validas,
            key=lambda e: (e[1] - LAT) ** 2 + (e[2] - LON) ** 2,
        )

        nombre = estacion_cercana.get("name", "Desconocido")
        temp = float(estacion_cercana.get("temp", 0))
        humedad = float(estacion_cercana.get("humidity", 0))
        presion = float(estacion_cercana.get("pressure", 0))
        lluvia = float(estacion_cercana.get("rain", 0) or 0)
        print(f"📍 Estación SMN usada: {nombre}")

        return {"temp": temp, "humedad": humedad, "presion": presion, "lluvia": lluvia}

    except Exception as e:
        print("⚠️ SMN falló:", e)
        return {"temp": 0, "humedad": 0, "presion": 0, "lluvia": 0}

# ---------- TRIANGULACIÓN DINÁMICA ----------
def obtener_datos_triangulados_debug():
    f1 = open_meteo()
    f2 = smn_weather()

    # Si SMN no devuelve datos válidos, usa solo Open-Meteo
    if f2["temp"] == 0 and f2["humedad"] == 0:
        print("ℹ️ Solo Open-Meteo tiene datos válidos.")
        datos = f1
    else:
        peso = [0.6, 0.4]
        datos = {
            "temp": f1["temp"] * peso[0] + f2["temp"] * peso[1],
            "humedad": f1["humedad"] * peso[0] + f2["humedad"] * peso[1],
            "presion": f1["presion"] * peso[0] + f2["presion"] * peso[1],
            "lluvia": f1["lluvia"] * peso[0] + f2["lluvia"] * peso[1],
        }

    fuentes = {"Open-Meteo": f1, "SMN": f2}
    return datos, fuentes





