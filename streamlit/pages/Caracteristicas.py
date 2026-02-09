import streamlit as st
import sys
import os

# 1. Ajuste de ruta para encontrar utils.py en la raíz del proyecto
# Esto sube un nivel desde /pages/ hacia la raíz
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

# 2. Ahora intentamos importar desde utils
try:
    from utils import FEATURES_CONSENSUS
except ImportError:
    st.error("⚠️ No se pudo cargar 'utils.py'. Verifica que esté en la raíz del repositorio.")
    FEATURES_CONSENSUS = []

def main():
    st.set_page_config(page_title="Diccionario de Variables", page_icon="📊", layout="wide")

    st.title("📖 Diccionario de Características")
    st.markdown("""
    Esta sección funciona como un **manual de referencia** para entender los datos que alimentan nuestro modelo.
    Cada variable seleccionada tiene un impacto estadístico en la predicción del riesgo.
    """)

    st.divider()

    # --- DICCIONARIO DE DESCRIPCIONES ---
    descriptions = {
        'int_rate': "Tasa de interés del préstamo. Refleja el riesgo asignado; a mayor tasa, mayor probabilidad de impago percibida.",
        'dti': "Ratio Deuda/Ingresos. Indica qué porcentaje de los ingresos del deudor se destinan al pago de deudas existentes.",
        'annual_inc': "Ingresos anuales reportados. Es la base de la capacidad financiera del solicitante.",
        'fico_range_low': "Puntaje FICO mínimo. Es el indicador estándar de salud crediticia en EE.UU.",
        'term': "Plazo del préstamo (36 o 60 meses). Los plazos más largos suelen tener tasas de default más altas.",
        'ME_inflation_cpi': "Inflación (CPI). Factor macro que reduce el poder adquisitivo y la capacidad de pago real.",
        'ME_unemployment_rate': "Tasa de Desempleo. Un contexto de alto desempleo aumenta el riesgo sistémico del portafolio."
    }

    # --- INTERFAZ ---
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("🔍 Selecciona una variable")
        seleccion = st.selectbox("Explorar lista:", FEATURES_CONSENSUS)
        
        desc = descriptions.get(seleccion, "Variable técnica utilizada para mejorar la precisión de la predicción de riesgo.")
        st.info(f"**¿Qué significa?**\n\n{desc}")

    with col2:
        st.subheader("📈 Análisis Visual")
        # Placeholder para futura gráfica
        st.markdown(f"**Comportamiento de {seleccion} en el Dataset**")
        st.info("Aquí puedes integrar un gráfico de importancia de variables o una distribución de valores.")
        # Ejemplo de gráfico rápido
        st.bar_chart([5, 12, 30, 25, 10])

if __name__ == "__main__":
    main()