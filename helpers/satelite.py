import requests
import datetime
from PIL import Image, ImageDraw, ImageFont
from config import LAT, LON

def obtener_imagen_satelital(datos=None):
    """
    Descarga imagen satelital actual (NASA GOES).
    Si falla, usa imagen local de respaldo.
    Dibuja overlay con datos del clima.
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





