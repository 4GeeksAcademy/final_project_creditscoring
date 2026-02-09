import streamlit as st
import sys
import os
import matplotlib.pyplot as plt
import shap
import pandas as pd
import pickle

# --- 1. CONFIGURACIÓN DE RUTAS ---
# Esto permite que la página encuentre el archivo utils.py en la raíz
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

try:
    from utils import FEATURES_CONSENSUS
except ImportError:
    st.error("No se pudo encontrar 'utils.py' en la raíz.")
    FEATURES_CONSENSUS = []

def main():
    st.set_page_config(page_title="Diccionario y SHAP", page_icon="📊", layout="wide")

    # --- 2. TÍTULO Y DESCRIPCIÓN ---
    st.title("📊 Diccionario de Variables e Impacto del Modelo")
    st.markdown("""
    En esta sección puedes explorar qué significa cada variable utilizada por nuestro modelo de **Credit Scoring** y observar cómo influyen globalmente en la predicción del riesgo de impago.
    """)

    st.divider()

    # --- 3. DICCIONARIO INTERACTIVO ---
    descriptions = {
        'int_rate': "Tasa de interés del préstamo. Refleja el riesgo asignado; a mayor tasa, mayor riesgo percibido.",
        'dti': "Ratio Deuda/Ingresos. Porcentaje de los ingresos mensuales destinado al pago de deudas.",
        'annual_inc': "Ingresos anuales brutos reportados por el solicitante.",
        'fico_range_low': "Puntaje FICO mínimo del cliente. Es el indicador estándar de salud crediticia.",
        'sub_grade': "Sub-clasificación detallada de LendingClub basada en el historial.",
        'term': "Plazo del préstamo (36 o 60 meses).",
        'revol_util': "Tasa de utilización de crédito rotativo disponible.",
        'installment': "La cuota mensual que el deudor debe pagar.",
        'ME_inflation_cpi': "Variable Macroeconómica: Índice de inflación (CPI).",
        'ME_unemployment_rate': "Variable Macroeconómica: Tasa de desempleo vigente.",
        'ME_fed_funds_rate': "Variable Macroeconómica: Tasa de interés de la Reserva Federal."
    }

    col_box, col_info = st.columns([1, 2])

    with col_box:
        st.subheader("🔍 Explorador")
        seleccion = st.selectbox("Selecciona una característica:", FEATURES_CONSENSUS)
        
    with col_info:
        st.subheader("💡 Definición")
        desc = descriptions.get(seleccion, "Variable técnica seleccionada durante el proceso de EDA para optimizar la precisión del modelo de riesgo.")
        st.info(f"**{seleccion}:** {desc}")

    st.divider()

    # --- 4. SECCIÓN DE SHAP (CÁLCULO EN VIVO) ---
    st.header("🎯 Main Drivers of Default Risk (SHAP)")
    st.write("El siguiente gráfico muestra el peso de cada variable en las decisiones del modelo.")

    # NOTA: Para que esto no falle, necesitamos simular o cargar los datos de SHAP.
    # En tu caso, deberías cargar tu modelo y X_test aquí.
    
    try:
        # Aquí es donde intentamos renderizar el gráfico que tienes en tu notebook
        # IMPORTANTE: Para la demo, si no tienes el modelo cargado aquí, 
        # intentaremos generar el contenedor del plot.
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Este bloque asume que ya tienes 'shap_values' y 'X_test_sel' cargados.
        # Como estamos en una página nueva, si no los tienes, lanzará un error.
        
        # EJEMPLO DE CÓMO LLAMARLO:
        # shap.summary_plot(shap_values, X_test_sel, plot_type="bar", max_display=15, show=False)
        
        # Para que el código no se rompa si aún no cargas el modelo en esta página:
        if 'shap_values' in locals() or 'shap_values' in globals():
            shap.summary_plot(shap_values, X_test_sel, plot_type="bar", max_display=15, show=False)
            plt.xlabel("Feature impact on default risk")
            plt.tight_layout()
            st.pyplot(plt.gcf())
        else:
            st.warning("Para mostrar el gráfico SHAP real, se requiere cargar el modelo y los datos de prueba en esta página.")
            st.info("💡 **Tip:** Puedes cargar tu modelo guardado usando `pickle.load(open('tu_modelo.pkl', 'rb'))` antes de llamar a SHAP.")

    except Exception as e:
        st.error(f"Error al generar el gráfico SHAP: {e}")

    st.divider()
    st.caption("Proyecto Credit Scoring | Sebas, Dorota y Johan")

if __name__ == "__main__":
    main()