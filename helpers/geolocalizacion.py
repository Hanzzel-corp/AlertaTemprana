import os, json, requests

CONFIG_FILE = "ubicacion_usuario.json"

def obtener_por_nombre(ciudad):
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={ciudad}&format=json&limit=1"
        r = requests.get(url, headers={"User-Agent": "HanzzelCorp-AlertaBot"}, timeout=10)
        data = r.json()
        if not data:
            return None
        return {"ciudad": ciudad.title(), "lat": float(data[0]["lat"]), "lon": float(data[0]["lon"])}
    except Exception:
        return None

def guardar_ubicacion(info):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2, ensure_ascii=False)

def cargar_ubicacion():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

