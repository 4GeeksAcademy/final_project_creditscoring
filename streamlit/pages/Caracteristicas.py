import streamlit as st
import sys
import os
import matplotlib.pyplot as plt
import pandas as pd

# --- 1. CONFIGURACIÓN DE RUTAS (Estructura: streamlit/pages/) ---
# Subimos dos niveles para llegar a la raíz del repositorio
current_dir = os.path.dirname(__file__)
root_path = os.path.abspath(os.path.join(current_dir, '..', '..'))
# Añadimos la carpeta 'streamlit' al path para encontrar utils.py
streamlit_path = os.path.join(root_path, 'streamlit')

if streamlit_path not in sys.path:
    sys.path.append(streamlit_path)

# --- 2. IMPORTACIONES SEGUROS ---
try:
    from utils import FEATURES_CONSENSUS
except ImportError:
    FEATURES_CONSENSUS = ["int_rate", "dti", "annual_inc", "fico_range_low", "term"]

# Intentamos importar SHAP (esto fallará si requirements.txt no está en la raíz)
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

def main():
    st.set_page_config(page_title="Diccionario de Variables", page_icon="📊", layout="wide")

    # --- TÍTULO E INTRODUCCIÓN ---
    st.title("📊 Diccionario de Variables e Impacto")
    st.markdown("""
    Esta sección detalla las variables clave analizadas por nuestro modelo de **Credit Scoring**. 
    Puedes consultar la definición de cada una y entender su peso en la decisión final.
    """)

    st.divider()

    # --- 3. DICCIONARIO DE DEFINICIONES ---
    descriptions = {
        'int_rate': "Tasa de interés del préstamo. Refleja el riesgo asignado por el prestamista.",
        'dti': "Ratio Deuda/Ingresos. Porcentaje de los ingresos mensuales destinado al pago de deudas.",
        'annual_inc': "Ingresos anuales brutos reportados por el solicitante.",
        'fico_range_low': "Puntaje FICO mínimo del cliente. Es el indicador estándar de salud crediticia en EE.UU.",
        'term': "Plazo del préstamo (36 o 60 meses). Plazos más largos suelen tener mayor riesgo.",
        'installment': "La cuota mensual que el deudor debe pagar si el préstamo es aprobado.",
        'ME_inflation_cpi': "Variable Macro: Índice de inflación. Afecta el poder adquisitivo del deudor.",
        'ME_unemployment_rate': "Variable Macro: Tasa de desempleo. Un entorno de alto desempleo eleva el riesgo.",
        'ME_fed_funds_rate': "Variable Macro: Tasa de la Reserva Federal. Influye en el costo del dinero."
    }

    # --- INTERFAZ: SELECTBOX Y DEFINICIÓN ---
    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.subheader("🔍 Explorador")
        seleccion = st.selectbox("Selecciona una característica:", FEATURES_CONSENSUS)

    with col2:
        st.subheader("💡 ¿Qué significa?")
        detalle = descriptions.get(seleccion, "Variable técnica seleccionada durante el proceso de EDA para optimizar la precisión del modelo.")
        st.info(f"**{seleccion}:** {detalle}")

    st.divider()

    # --- 4. SECCIÓN SHAP (IMPACTO GLOBAL) ---
    st.header("🎯 Main Drivers of Default Risk (SHAP)")
    st.write("El siguiente gráfico explica qué variables influyen más en que el modelo prediga un 'Default' (Impago).")

    if not SHAP_AVAILABLE:
        st.error("❌ La librería 'shap' no está instalada. Verifica que 'requirements.txt' esté en la raíz del repositorio (fuera de la carpeta streamlit).")
    
    # Intentamos cargar la imagen estática (Es la forma más rápida y estable para Streamlit Cloud)
    # Buscamos 'shap_summary.png' en la raíz del repositorio
    img_path = os.path.join(root_path, 'shap_summary.png')

    if os.path.exists(img_path):
        st.image(img_path, caption="Gráfico SHAP: Importancia de Variables", use_container_width=True)
    else:
        st.warning("⚠️ No se encontró el archivo 'shap_summary.png' en la raíz.")
        st.info("Para que este gráfico se vea real, guarda tu plot desde el notebook con `plt.savefig('shap_summary.png')` y súbelo a la raíz de GitHub.")
        # Gráfico de barras de respaldo
        st.bar_chart([15, 30, 45, 10, 20])
        st.caption("Gráfico de demostración (Simulación)")

if __name__ == "__main__":
    main()