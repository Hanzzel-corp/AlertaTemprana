# 🌦️ AlertaTemprana v4.0  
**Bot meteorológico interactivo con geolocalización y alertas automáticas.**

Desarrollado por **Hanzzel Corp ∑Δ9**  
Licencia: [MIT](LICENSE)

---

## 🧭 Descripción general

**AlertaTemprana** es un bot escrito en Python que permite obtener el clima actual, imágenes satelitales y alertas meteorológicas según la ubicación del usuario.  
El proyecto está diseñado para funcionar de manera **local** o **en servidores**, utilizando fuentes abiertas de datos climáticos como **Open-Meteo** y el **Servicio Meteorológico Nacional (SMN Argentina)**.

Incluye:
- 🌍 Geolocalización automática por ciudad.  
- 📡 Integración con Telegram (bot interactivo).  
- ☁️ Descarga de imágenes satelitales.  
- 🧠 Descripción automática de condiciones meteorológicas.  
- 💾 Registro de datos en CSV (histórico de clima).  
- ⚠️ Alertas por umbral configurable (ej. tormentas, calor extremo, etc).

---

## 🧩 Estructura del proyecto

AlertaTemprana/
│
├── helpers/ # Funciones auxiliares del bot
│ ├── analisis.py # Genera descripciones climáticas
│ ├── fuentes.py # Obtiene datos desde Open-Meteo y SMN
│ ├── geolocalizacion.py # Convierte nombre de ciudad en coordenadas
│ ├── logger.py # Guarda registros locales
│ └── satelite.py # Descarga imágenes satelitales
│
├── bot_alerta_debug.py # Script principal del bot
├── config_template.py # Plantilla de configuración (sin tokens)
├── README.md # Este archivo
├── requirements.txt # Librerías necesarias
├── LICENSE # Licencia MIT
└── .gitignore # Ignora archivos locales y sensibles

yaml
Copiar código

---

## ⚙️ Instalación

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/Hanzzel-corp/AlertaTemprana.git
cd AlertaTemprana
2️⃣ Crear entorno virtual e instalar dependencias
bash
Copiar código
python -m venv env
env\Scripts\activate       # En Windows
# o
source env/bin/activate    # En Linux/Mac

pip install -r requirements.txt
3️⃣ Configurar el bot
Renombrar el archivo config_template.py a config.py:

bash
Copiar código
mv config_template.py config.py
Y editar su contenido:

python
Copiar código
TELEGRAM_TOKEN = "tu_token_de_telegram_aquí"
CHAT_ID = "tu_chat_id_aquí"
LAT, LON = -34.6037, -58.3816  # Coordenadas iniciales (Buenos Aires)
💬 Uso
Ejecutá el bot:

bash
Copiar código
python bot_alerta_debug.py
Luego, en Telegram, buscá tu bot y escribí cualquiera de los siguientes comandos:

Comando	Descripción
/start	Muestra la ayuda general.
/tiempo	Muestra el clima actual.
/radar	Envía la última imagen satelital.
/ubicacion <ciudad>	Cambia la ubicación del usuario (ej: /ubicacion Salta).
/ubicacion_actual	Muestra la ubicación configurada.

📡 Ejemplo de funcionamiento
Entrada:

bash
Copiar código
/tiempo
Salida:

yaml
Copiar código
🕓 18:56:07
🌤️ Clima actual:
🌡️ Temp: 13.6 °C
💧 Humedad: 77%
🌀 Presión: 1011 hPa
☁️ Condiciones estables y cielo variable.
🧠 Futuras mejoras
🚨 Alertas automáticas basadas en umbrales climáticos.

🌍 Soporte multiusuario y ubicaciones múltiples.

🛰️ Integración con radar NOAA y mapas dinámicos.

📱 Interfaz web visual con gráficos en tiempo real.

💡 Créditos
Desarrollado por Hanzzel Corp ∑Δ9
Inspirado en la idea de hacer accesible la inteligencia meteorológica a cualquier persona, desde cualquier dispositivo.

“El conocimiento es la mejor defensa ante lo imprevisible.”

📜 Licencia
Este proyecto está bajo la licencia MIT — ver el archivo LICENSE para más detalles.

yaml
Copiar código

---

### 📌 Para subirlo:
1. Guardá este contenido en tu archivo `README.md` (reemplazando el actual).  
2. Luego en la terminal:

```bash
git add README.md
git commit -m "📘 Add detailed README for AlertaTemprana"
git push

