import streamlit as st
import pandas as pd
import joblib
import lightgbm as lgb
import os
from limpieza import transformar_datos  # Asegúrate que limpieza.py esté en la misma carpeta
from utils import FEATURES_CONSENSUS    # Tu lista de columnas del modelo

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Predicción de Riesgo", page_icon="📈", layout="wide")

# --- 2. FUNCIÓN DE PREDICCIÓN (Estilo Profesor) ---
def realizar_prediccion(data):
    """Carga el modelo y devuelve las probabilidades de Default"""
    path = 'notebooks/credit_risk_model_bundle.pkl'
    try:
        # Cargamos usando joblib (más estable para modelos LightGBM)
        model_obj = joblib.load(path)
        
        # Extraer el modelo si viene dentro de un diccionario/bundle
        if isinstance(model_obj, dict):
            model = model_obj.get('model', model_obj)
        else:
            model = model_obj
            
        return model.predict_proba(data)
    except Exception as e:
        st.error(f"Error al cargar el modelo: {e}")
        return None

def main():
    # --- 3. ENCABEZADO Y EXPLICACIÓN ---
    st.title("🚀 Sistema de Predicción de Riesgo Crediticio")
    st.markdown("""
    Esta herramienta utiliza un modelo de **Machine Learning (LightGBM)** para evaluar la probabilidad de que un solicitante no cumpla con sus pagos (*Default*).
    """)

    # --- 4. CONFIGURACIÓN DEL UMBRAL (SIDEBAR) ---
    st.sidebar.header("⚙️ Configuración")
    umbral = st.sidebar.slider(
        "Umbral de Decisión (Cut-off)", 
        min_value=0.1, max_value=0.9, value=0.5, step=0.05,
        help="Si la probabilidad de default supera este valor, el crédito es rechazado."
    )
    
    st.sidebar.info(f"""
    **Política de Riesgo:**
    - Probabilidad > {umbral:.0%}: 🔴 Rechazado
    - Probabilidad <= {umbral:.0%}: 🟢 Aprobado
    """)

    # Selección de método de entrada
    opcion = st.sidebar.radio("Seleccione Modo de Entrada", ["👤 Individual", "📂 Masivo (CSV)"])

    st.divider()

    # --- 5. MODO INDIVIDUAL ---
    if opcion == "👤 Individual":
        st.subheader("📋 Datos del Solicitante")
        with st.form("manual_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                loan_amnt = st.number_input("Monto Solicitado ($)", value=10000)
                term = st.selectbox("Plazo", [" 36 months", " 60 months"])
                int_rate = st.number_input("Tasa Interés (%)", value=12.0)
            with col2:
                annual_inc = st.number_input("Ingreso Anual ($)", value=50000)
                fico = st.slider("Puntaje FICO", 300, 850, 700)
                emp_length = st.selectbox("Antigüedad", ["< 1 year", "1 year", "5 years", "10+ years"])
            with col3:
                grade = st.selectbox("Grado", ["A", "B", "C", "D", "E", "F", "G"])
                sub_grade = st.text_input("Sub-Grado (ej. A1, B4)", "B1")
                dti = st.number_input("DTI", value=15.0)

            submit = st.form_submit_button("🚀 Calcular Riesgo")

        if submit:
            df_input = pd.DataFrame([{
                'loan_amnt': loan_amnt, 'term': term, 'grade': grade, 'int_rate': int_rate,
                'sub_grade': sub_grade, 'annual_inc': annual_inc,
                'emp_length': emp_length, 'fico_range_low': fico, 'dti': dti
            }])

            data_ready = transformar_datos(df_input, FEATURES_CONSENSUS)
            probs = realizar_prediccion(data_ready)
            
            if probs is not None:
                riesgo = probs[0][1]
                st.subheader("🎯 Resultado del Análisis")
                if riesgo > umbral:
                    st.error(f"**CRÉDITO RECHAZADO** - Riesgo de Default: {riesgo:.2%}")
                else:
                    st.success(f"**CRÉDITO APROBADO** - Riesgo de Default: {riesgo:.2%}")

    # --- 6. MODO MASIVO (CSV) ---
    else:
        st.subheader("📂 Carga de Datos por Lote")
        archivo = st.file_uploader("Suba el archivo CSV con los datos de clientes", type=["csv"])
        
        if archivo is not None:
            df_csv = pd.read_csv(archivo)
            st.write("🔍 Vista previa de datos cargados:")
            st.dataframe(df_csv.head(5))

            if st.button("⚙️ Procesar y Predecir"):
                with st.spinner("Analizando base de datos..."):
                    # Transformar y Predecir
                    df_ready = transformar_datos(df_csv, FEATURES_CONSENSUS)
                    probs = realizar_prediccion(df_ready)
                    
                    if probs is not None:
                        # Añadir resultados al DataFrame original
                        df_csv['Prob_Default'] = probs[:, 1]
                        df_csv['Decision'] = df_csv['Prob_Default'].apply(
                            lambda x: "🔴 Rechazado" if x > umbral else "🟢 Aprobado"
                        )

                        st.success(f"✅ Procesamiento completado (Umbral: {umbral:.0%})")
                        
                        # --- SELECCIÓN DE COLUMNAS PARA MOSTRAR ---
                        columnas_resumen = ['loan_amnt', 'term', 'grade', 'annual_inc', 'Prob_Default', 'Decision']
                        # Filtrar solo las que existen para evitar errores
                        cols_finales = [c for c in columnas_resumen if c in df_csv.columns]
                        
                        st.subheader("📊 Resumen de Resultados")
                        st.dataframe(
                            df_csv[cols_finales].style.format({'Prob_Default': '{:.2%}'}),
                            use_container_width=True
                        )

                        # Botón para descargar el reporte COMPLETO
                        csv_ready = df_csv.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Descargar Reporte Completo con Predicciones",
                            data=csv_ready,
                            file_name="reporte_riesgo_crediticio.csv",
                            mime="text/csv"
                        )

if __name__ == "__main__":
    main()