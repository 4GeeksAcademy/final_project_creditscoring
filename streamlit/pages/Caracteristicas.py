import streamlit as st
from utils import FEATURES_CONSENSUS

def main():
    st.set_page_config(page_title="Diccionario de Variables", page_icon="📊", layout="wide")

    # --- TÍTULO Y DESCRIPCIÓN INFORMATIVA ---
    st.title("📖 Diccionario de Características (Features)")
    st.markdown("""
    En esta sección, puedes explorar las variables que nuestro modelo de Machine Learning utiliza para calcular 
    el **Credit Scoring**. Cada una de estas características ha sido seleccionada tras un análisis exhaustivo (EDA), 
    identificando su impacto directo en la probabilidad de cumplimiento de pago.
    
    **Instrucciones:** Selecciona una variable del menú desplegable para entender qué representa y por qué es 
    importante para el análisis de riesgo de LendingClub.
    """)

    st.divider()

    # --- DICCIONARIO DE EXPLICACIONES ---
    # He creado descripciones amigables para las variables principales
    descriptions = {
        'int_rate': "Tasa de interés del préstamo. Refleja el riesgo asignado por el prestamista.",
        'dti': "Ratio Deuda/Ingresos. Indica qué porcentaje de los ingresos mensuales del deudor se destina al pago de deudas.",
        'annual_inc': "Ingresos anuales reportados por el solicitante al momento del registro.",
        'sub_grade': "Sub-calificación detallada de LendingClub (ej. A1, B3) basada en el historial del cliente.",
        'fico_range_low': "El límite inferior del rango de puntaje FICO del cliente proporcionado por la agencia de crédito.",
        'loan_amnt': "Monto total del préstamo solicitado por el cliente.",
        'term': "Número de pagos del préstamo (36 o 60 meses).",
        'revol_util': "Tasa de utilización de líneas de crédito rotativas (cuánto crédito usa frente al límite disponible).",
        'installment': "La cuota mensual que el deudor debe pagar si el préstamo es aprobado.",
        'emp_length': "Años de antigüedad en el empleo actual (0 a 10+ años).",
        'ME_inflation_cpi': "Variable Macroeconómica: Índice de Precios al Consumidor. Mide la inflación del periodo.",
        'ME_unemployment_rate': "Variable Macroeconómica: Tasa de desempleo al momento del préstamo.",
        'ME_fed_funds_rate': "Variable Macroeconómica: Tasa de interés de la Reserva Federal (EE.UU.)."
    }

    # --- INTERFAZ DE SELECCIÓN ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Selección")
        seleccion = st.selectbox(
            "Busca una característica:",
            options=FEATURES_CONSENSUS,
            help="Escribe o selecciona una variable de la lista."
        )

    with col2:
        st.subheader("Explicación")
        if seleccion in descriptions:
            st.success(f"### {seleccion}")
            st.write(descriptions[seleccion])
        else:
            # Mensaje genérico para las variables que no tengan descripción manual aún
            st.info(f"### {seleccion}")
            st.write("Esta variable forma parte del conjunto de datos seleccionado para el modelo. Representa métricas específicas del historial crediticio o condiciones macroeconómicas del entorno de LendingClub.")

    st.divider()
    
    # --- PIE DE PÁGINA ---
    st.caption("Nota: Las variables con prefijo 'ME_' corresponden a datos macroeconómicos externos vinculados por fecha.")

if __name__ == "__main__":
    main()