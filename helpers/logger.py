import csv
from datetime import datetime
import os

LOG_FILE = "clima_log.csv"

def registrar_datos(datos, fuente_activa="Open-Meteo"):
    """
    Guarda cada medición en clima_log.csv
    """
    now = datetime.now()
    fila = {
        "fecha": now.strftime("%Y-%m-%d"),
        "hora": now.strftime("%H:%M:%S"),
        "temperatura": round(datos.get("temp", 0), 2),
        "humedad": round(datos.get("humedad", 0), 2),
        "presion": round(datos.get("presion", 0), 2),
        "lluvia": round(datos.get("lluvia", 0), 2),
        "fuente": fuente_activa
    }

    existe = os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fila.keys())
        if not existe:
            writer.writeheader()
        writer.writerow(fila)
