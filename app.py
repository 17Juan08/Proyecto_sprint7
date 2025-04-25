import pandas as pd
import streamlit as st
import plotly_express as px

st.markdown(
    """
    <h1 style='text-align: center; color: white;'>
        Análisis del Almacén de Vehículos Usados
    </h1>
    """,
    unsafe_allow_html=True
)

st.write(" ")


st.write("A continuación se presenta un análisis básico de un almacén de vehículos usados. En este análisis se comparan variables como el estado del vehículo, su tipo, precio y año de fabricación, con el fin de identificar patrones o tendencias relevantes.")
