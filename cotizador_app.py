import streamlit as st
import pandas as pd
from io import BytesIO

st.write("App cargando OK…")

# --- Configuración ---
st.set_page_config(page_title="Cotizador C&E", page_icon="💰", layout="centered")

st.title("💰 Cotizador C&E")
st.write("Completá los datos para generar el presupuesto:")

# --- Datos del cliente y asesor ---
asesor = st.text_input("Nombre del asesor")
cliente = st.text_input("Nombre del cliente")
provincia = st.text_input("Provincia del cliente")
localidad = st.text_input("Localidad del cliente")

# --- Datos del proyecto ---
precio_m2 = st.number_input("Precio base por m² ($)", min_value=0.0, step=100.0)
superficie = st.number_input("Superficie (m²)", min_value=0.0, step=1.0)
distancia_km = st.number_input("Distancia al cliente (km)", min_value=0.0, step=10.0)

# --- Ubicación y adicionales ---
orientacion = st.selectbox("Ubicación del proyecto", ["Norte", "Sur"])
adicional = st.number_input("Adicional ($, opcional)", min_value=0.0, step=100.0, value=0.0)

# --- Cálculo ---
if st.button("Calcular presupuesto"):
    precio_ajustado = precio_m2

    if orientacion == "Norte":
        precio_ajustado += 10000
    elif orientacion == "Sur":
        tramos = distancia_km / 300
        precio_ajustado += 20000 * tramos

    total = superficie * precio_ajustado + adicional

    st.success(f"**Presupuesto total estimado:** ${total:,.2f}")

    # Crear DataFrame para exportar
    df = pd.DataFrame({
        "Asesor": [asesor],
        "Cliente": [cliente],
        "Provincia": [provincia],
        "Localidad": [localidad],
        "Precio base m² ($)": [precio_m2],
        "Superficie (m²)": [superficie],
        "Distancia (km)": [distancia_km],
        "Ubicación": [orientacion],
        "Adicional ($)": [adicional],
        "Precio ajustado m² ($)": [precio_ajustado],
        "Total ($)": [total]
    })

    # Exportar a Excel en memoria
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Presupuesto")
    buffer.seek(0)

    # Botón de descarga
    st.download_button(
        label="⬇️ Descargar presupuesto en Excel",
        data=buffer,
        file_name=f"COTIZACION_{cliente.upper().replace(' ', '_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
