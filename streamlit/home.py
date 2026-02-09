import streamlit as st

def main():
    st.set_page_config(
        page_title="Credit Scoring - LendingClub", 
        page_icon="💳", 
        layout="centered"
    )

    # Encabezado principal
    st.title("💳 Evaluación de riesgo crediticio")
    st.markdown("""
    Bienvenid@ al sistema de evaluación de riesgo crediticio basado en modelos de Machine Learning.
    Este portal permite analizar la viabilidad de préstamos utilizando datos históricos reales.
    """)

    # Sección de información del Proyecto
    with st.expander("ℹ️ Sobre el origen de los datos", expanded=True):
        st.write("""
        Los datos utilizados en este modelo provienen del dataset público de **LendingClub**, 
        la plataforma de préstamos entre pares (P2P) más grande del mundo.
        
        * **Objetivo:** Predecir si un solicitante entrará en 'Default' (incumplimiento de pago).
        * **Data:** Incluye información histórica de préstamos aprobados, historial crediticio de los clientes y estados de pago.
        """)

    st.markdown("---")
    st.subheader("🛠️ ¿Qué deseas hacer hoy?")

    # Selección de navegación
    col1, col2 = st.columns(2)

    with col1:
        st.info("### Explorar Datos")
        st.write("Analiza las variables que más influyen en el riesgo y visualiza el comportamiento de la data.")
        st.page_link("pages/Caracteristicas.py", label="Ir a Características", icon="📊")

    with col2:
        st.success("### Realizar Predicción")
        st.write("Ingresa los datos de un nuevo cliente para obtener su probabilidad de riesgo en tiempo real.")
        st.page_link("pages/Prediccion.py", label="Ir a Predicción", icon="🤖")

    st.markdown("---")
    st.caption("Proyecto Final - Bootcamp de Data Science 2026")

if __name__ == "__main__":
    main()