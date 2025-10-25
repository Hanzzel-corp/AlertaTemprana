def describir_clima(d):
    t, h, p, l = d["temp"], d["humedad"], d["presion"], d["lluvia"]
    desc = []

    if l > 1.0:
        desc.append("alta probabilidad de lluvia o llovizna")
    if h > 70 and p < 1010:
        desc.append("ambiente húmedo e inestable")
    if t > 33:
        desc.append("calor extremo, riesgo de golpe térmico")
    if t < 10:
        desc.append("frío intenso, posible helada")
    if not desc:
        desc.append("condiciones estables y cielo variable")

    sensacion = " y ".join(desc)
    return (
        f"🌦️ Clima actual:\n"
        f"🌡️ Temp: {t:.1f} °C\n"
        f"💧 Humedad: {h:.0f}%\n"
        f"🌀 Presión: {p:.0f} hPa\n"
        f"☁️ {sensacion.capitalize()}."
    )
