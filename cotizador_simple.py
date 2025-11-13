import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cotizador C&E", page_icon="💰", layout="centered")

st.title("💰 Cotizador Constructora Costanci & Estela")

st.write("Ingresá los datos del proyecto para calcular los costos.")

# --- Entradas ---
nombre_cliente = st.text_input("Nombre del cliente")
superficie = st.number_input("Superficie (m²)", min_value=0.0, step=0.5)
costo_material = st.number_input("Costo de materiales por m² ($)", min_value=0.0, step=100.0)
costo_mano_obra = st.number_input("Costo de mano de obra por m² ($)", min_value=0.0, step=100.0)
porcentaje_beneficio = st.slider("Margen de beneficio (%)", 0, 100, 20)

if st.button("Calcular"):
    costo_total = (costo_material + costo_mano_obra) * superficie
    total_con_beneficio = costo_total * (1 + porcentaje_beneficio / 100)

    st.subheader("📊 Resultados")
    st.write(f"**Cliente:** {nombre_cliente}")
    st.write(f"**Costo total:** ${costo_total:,.2f}")
    st.write(f"**Total con beneficio:** ${total_con_beneficio:,.2f}")

    # Crear dataframe para exportar
    df = pd.DataFrame({
        "Cliente": [nombre_cliente],
        "Superficie (m²)": [superficie],
        "Costo Material ($/m²)": [costo_material],
        "Costo Mano de Obra ($/m²)": [costo_mano_obra],
        "Beneficio (%)": [porcentaje_beneficio],
        "Total Final ($)": [total_con_beneficio]
    })

    st.download_button(
        "📥 Descargar cotización en Excel",
        df.to_excel(index=False, engine='openpyxl'),
        file_name=f"Cotizacion_{nombre_cliente}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
