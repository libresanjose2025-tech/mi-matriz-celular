import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Sistema de Inventario", layout="wide")

# --- CONEXIÓN CON GOOGLE SHEETS ---
# REEMPLAZA EL LINK DE ABAJO POR EL QUE COPIASTE DE TU HOJA DE GOOGLE
url = "https://docs.google.com/spreadsheets/d/1UgzToZxFtQd3ygeqR6ITgzWLOnSnQqPXiLgV-aGR5CM/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

# Leer los datos de la hoja
df = conn.read(spreadsheet=url)

st.title("📋 Control de Inventario Municipal")
st.markdown("### Seleccione el ítem para rellenar o modificar")

# Selector de ítem (del 1 al 77)
nro_item = st.selectbox("Elija el Nº de Documento:", df["Nº"].unique())

# Obtener los datos actuales de esa fila
datos_actuales = df[df["Nº"] == nro_item].iloc[0]

st.info(f"📄 **Documento:** {datos_actuales['Descripción']}")

# Formulario de edición
with st.form("form_edicion"):
    col1, col2 = st.columns(2)
    
    with col1:
        nuevo_estado = st.selectbox("Estado", ["Tiene", "No tiene"], 
                                    index=0 if datos_actuales["Estado (Tiene o no tiene)"] == "Tiene" else 1)
        nuevas_obs = st.text_area("Observaciones", value=str(datos_actuales["Observaciones"]))
        
    with col2:
        nueva_just = st.text_area("Justificación", value=str(datos_actuales["Justificación en caso de no contar con la documentación"]))
        foto = st.file_uploader("📷 Subir Foto/Evidencia", type=["jpg", "png", "jpeg"])

    boton_guardar = st.form_submit_button("💾 GUARDAR CAMBIOS")

if boton_guardar:
    # Actualizar la fila en el DataFrame
    df.loc[df["Nº"] == nro_item, "Estado (Tiene o no tiene)"] = nuevo_estado
    df.loc[df["Nº"] == nro_item, "Observaciones"] = nuevas_obs
    df.loc[df["Nº"] == nro_item, "Justificación en caso de no contar con la documentación"] = nueva_just
    
    # Guardar de vuelta en Google Sheets
    conn.update(spreadsheet=url, data=df)
    st.success(f"✅ ¡Datos del ítem {nro_item} actualizados correctamente!")
    st.balloons()

# Mostrar la tabla abajo para ver el progreso
st.divider()
st.subheader("📊 Matriz de Control en Tiempo Real")
st.dataframe(df, use_container_width=True)
