<<<<<<< HEAD
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

=======
# 🌦️ AlertaTemprana v4.0

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-2CA5E0?logo=telegram)](https://core.telegram.org/bots)

**Bot meteorológico inteligente para Telegram con geolocalización, predicciones y alertas automáticas.**

Desarrollado por **Hanzzel Corp** | Licencia: [MIT](LICENSE)

---

## 📋 Índice

- [Descripción](#-descripción)
- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Instalación](#-instalación)
- [Configuración](#️-configuración)
- [Uso](#-uso)
- [Comandos](#-comandos)
- [Documentación Técnica](#-documentación-técnica)
- [Fuentes de Datos](#-fuentes-de-datos)
- [Roadmap](#-roadmap)
- [Créditos](#-créditos)

---

## 📝 Descripción

**AlertaTemprana** es un bot de Telegram escrito en Python que proporciona información meteorológica en tiempo real. Combina múltiples fuentes de datos (Open-Meteo + SMN Argentina) para ofrecer pronósticos precisos, alertas automáticas por condiciones extremas, imágenes satelitales de NASA GOES, y predicciones de temperatura mediante machine learning con Facebook Prophet.

### 💡 Ideal para:
- Monitoreo personal del clima
- Alertas tempranas de eventos meteorológicos extremos
- Integración con sistemas de automatización del hogar
- Educación y divulgación meteorológica

---

## ✨ Características

| Funcionalidad | Descripción |
|--------------|-------------|
| 🌍 **Geolocalización** | Búsqueda de ciudades con conversión automática a coordenadas (OpenStreetMap) |
| 📡 **Bot de Telegram** | Interfaz interactiva con teclado personalizado y comandos intuitivos |
| 🛰️ **Imágenes Satelitales** | Descarga desde NASA GOES con overlay de datos meteorológicos |
| 🧠 **Predicción ML** | Forecasting de temperatura a 6 horas usando Prophet |
| ⚠️ **Alertas Automáticas** | Detección de condiciones críticas (olas de calor, heladas, lluvias intensas) |
| � **Visualización** | Gráficos históricos de temperatura con matplotlib |
| 💾 **Persistencia** | Logging CSV completo para análisis histórico |
| 🔗 **Multi-fuente** | Triangulación Open-Meteo + SMN Argentina para mayor precisión |

---

## 🏗️ Arquitectura

```
AlertaTemprana/
│
├── helpers/                      # Módulos auxiliares
│   ├── __init__.py              # Paquete Python
│   ├── analisis.py              # Descripción textual del clima
│   ├── fuentes.py               # Integración con APIs meteorológicas
│   ├── geolocalizacion.py       # Geocodificación de ciudades
│   ├── graficos.py              # Generación de gráficos
│   ├── logger.py                # Persistencia CSV
│   ├── prediccion.py            # Forecasting con Prophet
│   └── satelite.py              # Procesamiento de imágenes satelitales
│
├── bot_alerta_debug.py          # Script principal (entry point)
├── config_template.py           # Plantilla de configuración
├── requirements.txt             # Dependencias del proyecto
├── LICENSE                      # Licencia MIT
├── README.md                    # Documentación
│
└── [Archivos generados en runtime]
    ├── config.py               # Configuración local (no versionar)
    ├── chat_id.json            # ID de chat persistente
    ├── ubicacion_usuario.json  # Ubicación del usuario
    ├── clima_log.csv           # Historial de mediciones
    └── grafico_temp.png        # Gráficos generados
```

### 🔄 Flujo de Datos

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Open-Meteo    │────→│              │     │   Telegram Bot   │
│     API         │     │  bot_alerta  │←────│   (Interfaz)    │
└─────────────────┘     │    _debug    │     └─────────────────┘
                        │     .py      │
┌─────────────────┐     │              │     ┌─────────────────┐
│ SMN Argentina   │────→│  Triangulación │←───│  Prophet (ML)   │
│   (Estaciones)  │     │   + Análisis   │    │  Predicciones   │
└─────────────────┘     │              │    └─────────────────┘
                        └──────┬───────┘
                               │
              ┌────────────────┼────────────────┐
              ↓                ↓                ↓
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │  CSV Log │    │  NASA    │    │ Alertas  │
        │  (Hist)  │    │  GOES    │    │  Auto    │
        └──────────┘    └──────────┘    └──────────┘
```

---

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes)
- Git

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/Hanzzel-corp/AlertaTemprana.git
cd AlertaTemprana
```

### Paso 2: Crear entorno virtual

```bash
# Crear entorno
python -m venv .venv

# Activar (Linux/Mac)
source .venv/bin/activate

# Activar (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Activar (Windows CMD)
.venv\Scripts\activate.bat
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

> **Nota:** Prophet puede requerer compilación. En caso de errores, instala primero: `pip install pystan==2.19.1.1` y luego `pip install prophet`.

---

## ⚙️ Configuración

### 1. Crear Bot de Telegram

1. Inicia conversación con [@BotFather](https://t.me/botfather)
2. Envía `/newbot` y sigue las instrucciones
3. Guarda el token proporcionado (se verá como `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Configurar el archivo

```bash
cp config_template.py config.py
```

Edita `config.py` con tu editor favorito:

```python
# config.py

# Token del bot (requerido)
TELEGRAM_TOKEN = "123456789:TU_TOKEN_AQUI"

# Coordenadas iniciales (default: Buenos Aires)
LAT, LON = -34.6037, -58.3816
```

> **Importante:** Nunca subas `config.py` a GitHub (ya está en `.gitignore`).

### 3. Obtener Chat ID automáticamente

1. Inicia el bot: `python bot_alerta_debug.py`
2. Envía cualquier mensaje a tu bot en Telegram
3. El bot detectará automáticamente tu `CHAT_ID`

---

## 💬 Uso

### Iniciar el Bot

```bash
python bot_alerta_debug.py
```

Verás la siguiente salida:

```
🚀 Iniciando AlertaTemprana v4.0 — Inteligente + Visual
==================================================
📡 Bot Meteorológico con Telegram
🌍 Fuentes: Open-Meteo + SMN Argentina
🔮 Predicción: Prophet (Facebook)
🛰️ Imágenes: NASA GOES
==================================================
📡 CHAT_ID cargado: 123456789
🎧 Lector de comandos iniciado en hilo paralelo
```

---

## 🎮 Comandos

### Comandos de Telegram

| Comando | Emoji | Descripción |
|---------|-------|-------------|
| `/start` | - | Muestra menú interactivo y ayuda |
| `/tiempo` | 🌦️ | Clima actual con análisis descriptivo |
| `/radar` | 🛰️ | Última imagen satelital con overlay |
| `/grafico` | 📊 | Gráfico de temperatura histórica |
| `/ubicacion <ciudad>` | 📍 | Cambiar ubicación (ej: `/ubicacion Córdoba`) |
| `/ubicacion_actual` | 📍 | Muestra la ubicación configurada |

### Ejemplos de uso

```
💬 Usuario: /tiempo
� Bot: �️ Clima actual en Buenos Aires:
       🌡️ Temp: 22.5 °C
       💧 Humedad: 65%
       🌀 Presión: 1013 hPa
       ☁️ Condiciones estables y cielo variable.

💬 Usuario: /ubicacion Rosario
📤 Bot: ✅ Ubicación actualizada a Rosario
       (-32.9468, -60.6393)
```

---

## 📚 Documentación Técnica

### Módulos Principales

#### `bot_alerta_debug.py`
- **Hilo principal:** `ciclo_clima()` - Actualización cada 30 min
- **Hilo secundario:** `lector_comandos()` - Polling de comandos cada 2 seg

#### `helpers/fuentes.py`
- `open_meteo()`: API Open-Meteo (peso: 60%)
- `smn_weather()`: API SMN Argentina (peso: 40%)
- `obtener_datos_triangulados_debug()`: Fusión ponderada

#### `helpers/prediccion.py`
- `predecir_tendencia()`: Forecasting con Prophet (6h horizonte)
- `evaluar_alertas()`: Umbrales: T>35°C, T<0°C, lluvia>20mm, humedad>90%

#### `helpers/satelite.py`
- Fuente: NASA GOES Sudamérica
- Resolución: 10848x10848 px
- Overlay automático con datos del clima

### Formato del CSV de Log

```csv
fecha,hora,temperatura,humedad,presion,lluvia,fuente
2025-01-15,14:30:00,22.5,65,1013,0,Open-Meteo
```

---

## 🌍 Fuentes de Datos

| Fuente | Tipo | Cobertura | Precisión |
|--------|------|-----------|-----------|
| **Open-Meteo** | API Pronóstico | Global | Alta |
| **SMN Argentina** | Estaciones | Argentina | Muy Alta |
| **NASA GOES** | Satelital | Sudamérica | - |
| **Nominatim** | Geocodificación | Global | Alta |

---

## �️ Roadmap

- [x] Geolocalización por nombre de ciudad
- [x] Predicción ML con Prophet
- [x] Alertas automáticas por umbrales
- [x] Imágenes satelitales NASA GOES
- [x] Gráficos históricos
- [ ] Soporte multi-usuario
- [ ] Interfaz web (Dashboard)
- [ ] Integración NOAA GOES-R
- [ ] Pronóstico extendido (7 días)
- [ ] Notificaciones push nativas

---

## � Créditos

**Desarrollado por:** [Hanzzel Corp](https://github.com/Hanzzel-corp)

**Inspiración:**
> "El conocimiento es la mejor defensa ante lo imprevisible."

### Dependencias Clave
- [Open-Meteo](https://open-meteo.com/) - API meteorológica gratuita
- [Prophet](https://facebook.github.io/prophet/) - Forecasting de Facebook
- [NASA GOES](https://weather.msfc.nasa.gov/) - Imágenes satelitales
- [SMN Argentina](https://www.smn.gob.ar/) - Servicio Meteorológico Nacional

---

## 📜 Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).

```
Copyright (c) 2025 Hanzzel Corp

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
```

---

<p align="center">
  🌦️ <strong>AlertaTemprana</strong> — Inteligencia Meteorológica para Todos
</p>
>>>>>>> 89e4af6 (feat: initial Linux setup for AlertaTemprana)
