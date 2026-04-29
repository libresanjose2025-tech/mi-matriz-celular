import streamlit as st
import pandas as pd

st.set_page_config(page_title="Inventario Celular", layout="wide")

st.title("📋 Registro de Documentación")

if 'datos' not in st.session_state:
    st.session_state.datos = pd.DataFrame(columns=[
        "Nº", "Descripción", "Tipo", "Cantidad", "Estado", "Responsable", "Justificación", "Aclaraciones"
    ])

with st.form("formulario", clear_on_submit=True):
    st.subheader("📝 Rellenar Campos")
    c1, c2 = st.columns(2)
    with c1:
        nro = st.number_input("Nº", min_value=1, max_value=77)
        desc = st.text_input("Descripción")
        tipo = st.text_input("Tipo de Documento")
        cant = st.text_input("Cantidad")
    with c2:
        est = st.selectbox("Estado", ["Tiene", "No tiene"])
        resp = st.text_input("Responsable")
        just = st.text_area("Justificación")
        acla = st.text_area("Aclaraciones")
        foto = st.file_uploader("Cámara / Foto", type=["jpg", "png"])
    
    enviar = st.form_submit_button("GUARDAR DATOS")

if enviar:
    nueva_fila = {"Nº": nro, "Descripción": desc, "Tipo": tipo, "Cantidad": cant, "Estado": est, "Responsable": resp, "Justificación": just, "Aclaraciones": acla}
    st.session_state.datos = pd.concat([st.session_state.datos, pd.DataFrame([nueva_fila])], ignore_index=True)
    st.success("✅ Guardado correctamente")

st.write("### Matriz Actualizada")
st.dataframe(st.session_state.datos, use_container_width=True)
