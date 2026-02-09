import streamlit as st
import sys
import os
import matplotlib.pyplot as plt

# --- 1. ARREGLO DE RUTAS (Crucial para Streamlit Cloud) ---
# Esto permite que la página encuentre 'utils.py' subiendo un nivel
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

# --- 2. IMPORTACIONES SEGUROS ---
try:
    from utils import FEATURES_CONSENSUS
except ImportError:
    # Si falla el import, definimos una lista de emergencia para que no se caiga la app
    FEATURES_CONSENSUS = ['int_rate', 'dti', 'annual_inc', 'fico_range_low', 'term']

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

def main():
    st.set_page_config(page_title="Análisis de Características", page_icon="📊", layout="wide")

    # --- TÍTULO E INTRODUCCIÓN ---
    st.title("📊 Diccionario de Variables e Impacto")
    st.markdown("""
    Esta sección funciona como un **diccionario interactivo**. Aquí explicamos qué significa cada 
    variable que el modelo de Machine Learning analiza para determinar el riesgo de un crédito.
    """)

    st.divider()

    # --- SECCIÓN 1: DICCIONARIO DE VARIABLES ---
    # Diccionario con explicaciones humanas
    descriptions = {
        'int_rate': "Tasa de interés del préstamo. Refleja el riesgo asignado por el prestamista.",
        'dti': "Ratio Deuda/Ingresos. Indica qué porcentaje de los ingresos se destina a pagar deudas.",
        'annual_inc': "Ingresos anuales brutos reportados por el solicitante.",
        'fico_range_low': "Puntaje FICO mínimo del cliente. Es el indicador estándar de salud crediticia.",
        'term': "Plazo del préstamo (36 o 60 meses).",
        'installment': "La cuota mensual que el deudor debe pagar.",
        'ME_inflation_cpi': "Variable Macroeconómica: Índice de inflación (CPI).",
        'ME_unemployment_rate': "Variable Macroeconómica: Tasa de desempleo vigente.",
        'ME_fed_funds_rate': "Variable Macroeconómica: Tasa de interés de la Reserva Federal."
    }

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("🔍 Selecciona una variable")
        seleccion = st.selectbox("Explorar lista consensuada:", FEATURES_CONSENSUS)

    with col2:
        st.subheader("💡 ¿Qué significa?")
        detalle = descriptions.get(seleccion, "Variable técnica seleccionada durante el proceso de análisis (EDA) para mejorar la precisión del modelo.")
        st.info(f"**{seleccion}:** {detalle}")

    st.divider()

    # --- SECCIÓN 2: IMPACTO SHAP ---
    st.header("🎯 Factores Clave de Riesgo (SHAP)")
    st.write("A continuación se muestra el impacto global de las variables en la predicción:")

    # Intentamos buscar el gráfico guardado en la raíz
    img_path = os.path.join(root_path, 'shap_summary.png')

    if os.path.exists(img_path):
        st.image(img_path, caption="Análisis de importancia (SHAP Summary Plot)", use_container_width=True)
    else:
        st.warning("⚠️ No se encontró la imagen 'shap_summary.png'.")
        st.info("Para visualizar el impacto real, guarda tu gráfico SHAP desde el notebook usando: `plt.savefig('shap_summary.png')` y súbelo a la raíz de tu repositorio.")
        
        # Gráfico de barras de ejemplo para que la página no se vea vacía
        st.bar_chart([10, 25, 45, 30, 15])
        st.caption("Gráfico de ejemplo (Simulación de importancia de variables)")

if __name__ == "__main__":
    main()