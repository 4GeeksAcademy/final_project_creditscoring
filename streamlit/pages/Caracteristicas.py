import streamlit as st
import sys
import os
import matplotlib.pyplot as plt
import pandas as pd

# --- 1. CONFIGURACIÓN DE RUTAS (Estructura: streamlit/pages/) ---
current_dir = os.path.dirname(__file__)
root_path = os.path.abspath(os.path.join(current_dir, '..', '..'))
streamlit_path = os.path.join(root_path, 'streamlit')

if streamlit_path not in sys.path:
    sys.path.append(streamlit_path)

# --- 2. IMPORTACIONES SEGUROS ---
try:
    from utils import FEATURES_CONSENSUS
except ImportError:
    FEATURES_CONSENSUS = ["int_rate", "dti", "annual_inc", "fico_range_low", "term"]

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
    # Fíjate que todo esto ahora tiene 4 espacios de sangría
    descriptions = {
        'int_rate': "Tasa de interés anual asignada al préstamo. Refleja el nivel de riesgo percibido por la entidad y las condiciones de mercado.",
        'dti': "Debt-to-Income ratio (DTI). Proporción de los ingresos mensuales del solicitante destinada al pago de deudas. Valores altos indican mayor presión financiera.",
        'annual_inc': "Ingresos anuales brutos declarados por el solicitante. Es un indicador clave de capacidad de pago.",
        'sub_grade': "Subcategoría de riesgo crediticio definida por la entidad (por ejemplo, A1–G5). Refina el grade y resume múltiples variables internas.",
        'revol_util': "Porcentaje de utilización del crédito revolvente disponible. Un uso elevado suele asociarse a mayor riesgo.",
        'revol_bal': "Saldo total pendiente en líneas de crédito revolvente (como tarjetas de crédito).",
        'installment': "Cuota mensual fija que el prestatario debe pagar durante la vida del préstamo.",
        'total_acc': "Número total de cuentas de crédito que el solicitante ha tenido a lo largo de su historial.",
        'funded_amnt_inv': "Monto del préstamo efectivamente financiado por los inversores.",
        'funded_amnt': "Monto total del préstamo aprobado y financiado por la entidad.",
        'loan_amnt': "Monto total solicitado por el cliente en el préstamo.",
        'total_bc_limit': "Límite total de crédito disponible en cuentas bancarias y tarjetas de crédito.",
        'ME_pce': "Variable macroeconómica: Índice de gasto en consumo personal (PCE). Refleja el nivel de actividad económica y consumo.",
        'grade': "Clasificación general de riesgo crediticio del préstamo (A–G), determinada por la entidad.",
        'fico_range_low': "Valor inferior del rango de puntuación FICO del solicitante. Indicador estándar de solvencia crediticia en EE.UU.",
        'ME_inflation_cpi': "Variable macroeconómica: Índice de precios al consumidor (CPI). Mide la inflación y afecta el poder adquisitivo.",
        'mo_sin_old_rev_tl_op': "Número de meses desde la apertura de la cuenta de crédito revolvente más antigua.",
        'avg_cur_bal': "Saldo promedio actual en las cuentas de crédito del solicitante.",
        'tot_hi_cred_lim': "Límite máximo histórico de crédito otorgado al solicitante.",
        'emp_length': "Antigüedad laboral del solicitante. Mayor estabilidad laboral suele asociarse a menor riesgo.",
        'mths_since_recent_bc': "Meses transcurridos desde la apertura de la cuenta bancaria más reciente.",
        'ME_unemployment_rate': "Variable macroeconómica: Tasa de desempleo. Un desempleo elevado incrementa el riesgo sistémico.",
        'ME_fed_funds_rate': "Variable macroeconómica: Tasa de interés de la Reserva Federal. Influye en el costo del crédito y la economía general.",
        'acc_open_past_24mths': "Número de cuentas de crédito abiertas en los últimos 24 meses.",
        'inq_last_6mths': "Número de consultas de crédito realizadas en los últimos 6 meses. Muchas consultas pueden indicar estrés financiero.",
        'term': "Plazo del préstamo en meses (típicamente 36 o 60). Plazos más largos suelen implicar mayor riesgo."
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
    st.header("🎯 ### 🔍 Interpretación del Análisis de Riesgo (SHAP)")
    st.write('''
        Este gráfico de valores SHAP permite abrir la **"caja negra"** del modelo de Inteligencia Artificial para entender qué factores pesan más al decidir si un crédito es riesgoso o no. 
    
    * **Orden de Importancia**: Las variables están ordenadas de arriba hacia abajo; las de arriba (como `sub_grade` y `term`) son las que más influyen en el resultado final. 
    * **Impacto en el Riesgo**:
        * Los puntos hacia la **derecha** (valores positivos) aumentan la probabilidad de que el cliente caiga en incumplimiento (Default).
        * Los puntos hacia la **izquierda** (valores negativos) indican factores que dan confianza y reducen el riesgo.
    * **Código de Colores**: 
        * El color **rojo** representa valores altos de esa variable y el **azul** valores bajos. Por ejemplo, se observa que plazos más largos (`term` en rojo) empujan el riesgo hacia la derecha.
    ''')
    if not SHAP_AVAILABLE:
        st.error("❌ La librería 'shap' no está instalada. Verifica que 'requirements.txt' esté en la raíz del repositorio.")
    
    img_path = os.path.join(root_path, 'shap_summary.png')

    if os.path.exists(img_path):
        st.image(img_path, caption="Gráfico SHAP: Importancia de Variables", use_container_width=True)
    else:
        st.warning("⚠️ No se encontró el archivo 'shap_summary.png' en la raíz.")
        st.info("Para que este gráfico se vea real, guarda tu plot desde el notebook con plt.savefig('shap_summary.png') y súbelo a la raíz de GitHub.")
        st.bar_chart([15, 30, 45, 10, 20])
        st.caption("Gráfico de demostración (Simulación)")

if __name__ == "__main__":
    main()