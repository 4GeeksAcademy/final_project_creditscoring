import streamlit as st
import sys
import os
import matplotlib.pyplot as plt
import pandas as pd

# Intentamos importar SHAP de forma segura
try:
    import shap
except ImportError:
    st.error("La librería 'shap' no está instalada. Agrégala a requirements.txt")

# --- 1. CONFIGURACIÓN DE RUTAS ---
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

try:
    from utils import FEATURES_CONSENSUS
except ImportError:
    FEATURES_CONSENSUS = ["int_rate", "dti", "annual_inc", "fico_range_low"]

def main():
    st.set_page_config(page_title="Diccionario y SHAP", page_icon="📊", layout="wide")

    st.title("📊 Diccionario de Variables e Impacto del Modelo")
    st.markdown("""
    Explora las definiciones de las variables y su impacto global en la predicción del riesgo.
    """)

    # --- 2. DICCIONARIO ---
    descriptions = {
        'int_rate': "Tasa de interés del préstamo. A mayor tasa, mayor riesgo percibido.",
        'dti': "Ratio Deuda/Ingresos. Porcentaje de ingresos destinado al pago de deudas.",
        'annual_inc': "Ingresos anuales brutos reportados por el solicitante.",
        'fico_range_low': "Puntaje FICO mínimo del cliente. Indicador clave de salud crediticia.",
        'term': "Plazo del préstamo (36 o 60 meses).",
        'ME_inflation_cpi': "Variable Macroeconómica: Índice de inflación (CPI).",
        'ME_unemployment_rate': "Variable Macroeconómica: Tasa de desempleo vigente."
    }

    col_box, col_info = st.columns([1, 2])
    with col_box:
        st.subheader("🔍 Explorador")
        seleccion = st.selectbox("Selecciona una característica:", FEATURES_CONSENSUS)
        
    with col_info:
        st.subheader("💡 Definición")
        desc = descriptions.get(seleccion, "Variable técnica seleccionada durante el EDA.")
        st.info(f"**{seleccion}:** {desc}")

    st.divider()

    # --- 3. SECCIÓN DE SHAP ---
    st.header("🎯 Main Drivers of Default Risk (SHAP)")
    
    # Intentamos generar el gráfico SHAP
    # Nota: Aquí asumo que eventualmente cargarás tu 'final_model' y 'X_test_sel'
    if 'shap' in sys.modules:
        try:
            # BLOQUE PARA EL GRÁFICO
            st.write("Impacto de las variables en la decisión de riesgo:")
            
            # Si tienes los datos listos, descomenta estas líneas y ajusta los nombres:
            # fig, ax = plt.subplots(figsize=(10, 6))
            # shap.summary_plot(shap_values, X_test_sel, plot_type="bar", show=False)
            # st.pyplot(plt.gcf())
            
            st.warning("⚠️ Gráfico en espera: Carga tu modelo y datos para visualizar el SHAP real.")
            
        except Exception as e:
            st.error(f"Error al procesar SHAP: {e}")
    else:
        st.error("No se pudo cargar SHAP. Revisa la instalación de dependencias.")

if __name__ == "__main__":
    main()