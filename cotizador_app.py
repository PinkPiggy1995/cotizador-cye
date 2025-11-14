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
distancia_km = st.number_input("Distancia al cliente (km)", min_value=0.0, step=10.0)

# --- Ubicación y adicionales ---
orientacion = st.selectbox("Ubicación del proyecto", ["Norte", "Sur"])
adicional = st.number_input("Adicional ($, opcional)", min_value=0.0, step=100.0, value=0.0)

# --- Superficie al final ---
superficie = st.number_input("Superficie (m²)", min_value=0.0, step=1.0)

# --- Cálculo ---

import math

if st.button("Calcular presupuesto"):

    # 1. Costo base por m²
    costo_base = precio_m2

    # 2. Costo de distancia según orientación
    if distancia_km <= 300:
        tramos = 0
    else:
        tramos = math.ceil((distancia_km - 300) / 300)

    if orientacion == "Norte":
        costo_distancia = tramos * 10000
    elif orientacion == "Sur":
        costo_distancia = tramos * 20000
    else:
        costo_distancia = 0

    # 3. Adicionales
    costo_adicionales = adicional

    # 4. Total final
    total = (costo_base + costo_distancia + costo_adicionales) * superficie

    st.success(f"El presupuesto total es: ${total:,.0f}")

    # Crear DataFrame para exportar
    df = pd.DataFrame({
        "Asesor": [asesor],
        "Cliente": [cliente],
        "Provincia": [provincia],
        "Localidad": [localidad],
        "Precio base m² ($)": [precio_m2],
        "Distancia (km)": [distancia_km],
        "Ubicación": [orientacion],
        "Adicional ($)": [adicional],
        "Precio ajustado m² ($)": [costo_base + costo_distancia + costo_adicionales],
        "Superficie (m²)": [superficie],
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
