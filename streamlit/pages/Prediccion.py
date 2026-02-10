import streamlit as st
import pandas as pd
import pickle
import os
from limpieza import transformar_datos  # Tu función con toda la codificación
from utils import FEATURES_CONSENSUS    # La lista de columnas del modelo
import joblib
import lightgbm as lgb # Importante añadir esta línea


# --- 1. FUNCIÓN DE PREDICCIÓN (Estilo Profesor) ---
def realizar_prediccion(data):
    path = 'notebooks/credit_risk_model_bundle.pkl'
    try:
        # Usamos joblib que es más flexible que pickle para modelos
        import joblib
        bundle = joblib.load(path)
        
        if isinstance(bundle, dict):
            model = bundle.get('model', bundle)
        else:
            model = bundle
        return model.predict_proba(data)
    except Exception as e:
        st.error(f"Error al cargar el modelo: {e}")
        # Si falla joblib, intentamos pickle como último recurso
        import pickle
        with open(path, "rb") as f:
            return pickle.load(f).predict_proba(data)

def main():
    st.set_page_config(page_title="Predicción de Riesgo", page_icon="📈", layout="wide")

    # --- 2. ENCABEZADO Y EXPLICACIÓN ---
    st.title("🚀 Sistema de Predicción de Riesgo Crediticio")
    st.markdown("""
    Bienvenido al módulo de evaluación. Esta herramienta utiliza un modelo de **Machine Learning** entrenado para identificar la probabilidad de incumplimiento (*Default*) de un crédito.
    
    ### 📌 Instrucciones:
    1. **Entrada Manual:** Ideal para evaluar a un cliente individual rápidamente.
    2. **Carga masiva (CSV):** Permite procesar una base de datos completa de solicitantes.
    
    *El sistema aplica automáticamente la ingeniería de variables, imputación de nulos y codificación 
    de categorías (Grade, Sub-Grade, etc.) necesarias para el modelo.*
    """)

    st.divider()

    # --- 3. SELECCIÓN DE MÉTODO (Sidebar para evitar errores visuales) ---
    opcion = st.sidebar.radio("Seleccione Modo de Entrada", ["👤 Individual", "📂 Masivo (CSV)"])

    if opcion == "👤 Individual":
        st.subheader("📋 Datos del Solicitante")
        with st.form("manual_form"):
            col1, col2 = st.columns(2)
            with col1:
                loan_amnt = st.number_input("Monto Solicitado ($)", value=10000)
                term = st.selectbox("Plazo", [" 36 months", " 60 months"])
                grade = st.selectbox("Grado (Grade)", ["A", "B", "C", "D", "E", "F", "G"])
                sub_grade = st.text_input("Sub-Grado (ej. A1, B4)", "B1")
            
            with col2:
                annual_inc = st.number_input("Ingreso Anual ($)", value=50000)
                emp_length = st.selectbox("Antigüedad Laboral", ["< 1 year", "1 year", "5 years", "10+ years"])
                fico = st.slider("Puntaje FICO", 300, 850, 700)
                dti = st.number_input("DTI (Relación Deuda/Ingreso)", value=15.0)

            submit = st.form_submit_button("🚀 Calcular Riesgo")

        if submit:
            # Crear DataFrame con los nombres exactos del notebook
            df_input = pd.DataFrame([{
                'loan_amnt': loan_amnt, 'term': term, 'grade': grade,
                'sub_grade': sub_grade, 'annual_inc': annual_inc,
                'emp_length': emp_length, 'fico_range_low': fico, 'dti': dti
            }])

            # 1. Transformar (Lógica completa)
            data_ready = transformar_datos(df_input, FEATURES_CONSENSUS)
            
            # 2. Predecir
            probs = realizar_prediccion(data_ready)
            riesgo = probs[0][1]

            # 3. Mostrar resultado visual
            st.subheader("🎯 Resultado del Análisis")
            if riesgo < 0.3:
                st.success(f"**CRÉDITO APROBADO** - Probabilidad de Default: {riesgo:.2%}")
            elif riesgo < 0.6:
                st.warning(f"**REVISIÓN MANUAL REQUERIDA** - Probabilidad de Default: {riesgo:.2%}")
            else:
                st.error(f"**CRÉDITO DENEGADO** - Probabilidad de Default: {riesgo:.2%}")

    else:
        st.subheader("📂 Carga de Datos por Lote")
        st.info("Suba un archivo CSV con las columnas originales para obtener predicciones masivas.")
        
        archivo = st.file_uploader("Seleccione el archivo CSV", type=["csv"])
        
        if archivo is not None:
            df_csv = pd.read_csv(archivo)
            st.write("Vista previa de datos cargados:")
            st.dataframe(df_csv.head(5))

            if st.button("⚙️ Procesar y Predecir"):
                with st.spinner("Transformando datos y calculando riesgos..."):
                    # 1. Transformar todo el archivo
                    df_ready = transformar_datos(df_csv, FEATURES_CONSENSUS)
                    
                    # 2. Predecir
                    probs = realizar_prediccion(df_ready)
                    
                    # 3. Añadir resultados al DF original para descarga
                    df_csv['Prob_Default'] = probs[:, 1]
                    df_csv['Decision'] = df_csv['Prob_Default'].apply(lambda x: "Rechazado" if x > 0.5 else "Aprobado")

                st.success("✅ Procesamiento completado")
                st.dataframe(df_csv)

                # Botón de descarga
                csv = df_csv.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Descargar Resultados (CSV)", data=csv, file_name="resultados_prediccion.csv")

if __name__ == "__main__":
    main()