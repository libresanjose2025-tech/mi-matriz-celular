import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Sistema Inventario", layout="wide")
url = "https://docs.google.com/spreadsheets/d/1UgzToZxFtQd3ygeqR6ITgzWLOnSnQqPXiLgV-aGR5CM/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# Leer datos
df = conn.read(spreadsheet=url)

st.title("📋 Registro de Documentación")

# Selector de número
nro_item = st.selectbox("Elija el Nº de Documento:", df["Nº"].unique())

# --- SOLUCIÓN AL ERROR DE INDEX ---
# Buscamos la fila de manera segura
datos_fila = df[df["Nº"] == nro_item]

if not datos_fila.empty:
    datos_actuales = datos_fila.iloc[0]
    st.info(f"📄 Documento: {datos_actuales['Descripción']}")
    
    with st.form("form_edicion"):
        nuevo_estado = st.selectbox("Estado", ["Tiene", "No tiene"])
        nuevas_obs = st.text_area("Observaciones", value=str(datos_actuales['Observaciones']))
        nueva_just = st.text_area("Justificación", value=str(datos_actuales['Justificación en caso de no contar con la documentación']))
        boton = st.form_submit_button("💾 GUARDAR")
        
        if boton:
            df.loc[df["Nº"] == nro_item, "Estado (Tiene o no tiene)"] = nuevo_estado
            df.loc[df["Nº"] == nro_item, "Observaciones"] = nuevas_obs
            df.loc[df["Nº"] == nro_item, "Justificación en caso de no contar con la documentación"] = nueva_just
            conn.update(spreadsheet=url, data=df)
            st.success("✅ ¡Actualizado!")
else:
    st.warning("⚠️ No se encontraron datos para ese número en el Excel.")
