import streamlit as st
import pandas as pd
import numpy as np
import pickle
import joblib
import os
import sys

# --- 1. CONFIGURACIÓN DE RUTAS ---
current_dir = os.path.dirname(__file__)
# Subimos dos niveles desde 'streamlit/pages/' para llegar a la raíz
root_path = os.path.abspath(os.path.join(current_dir, '..', '..'))
streamlit_path = os.path.join(root_path, 'streamlit')

if streamlit_path not in sys.path:
    sys.path.append(streamlit_path)

try:
    from utils import FEATURES_CONSENSUS
except ImportError:
    st.error("No se pudo encontrar 'FEATURES_CONSENSUS' en utils.py")
    FEATURES_CONSENSUS = []

# --- 2. FUNCIÓN DE TRANSFORMACIÓN (ESPEJO DEL NOTEBOOK) ---
def transformar_datos(df):
    df_transformed = df.copy()

    # A. Manejo de Fechas (Credit Age)
    if 'issue_d' in df_transformed.columns and 'earliest_cr_line' in df_transformed.columns:
        df_transformed['issue_d'] = pd.to_datetime(df_transformed['issue_d'])
        df_transformed['earliest_cr_line'] = pd.to_datetime(df_transformed['earliest_cr_line'])
        # Usamos la fecha máxima disponible como referencia
        ref_date = df_transformed['issue_d'].max()
        df_transformed['credit_age'] = (ref_date - df_transformed['earliest_cr_line']).dt.days / 365

    # B. Mapeos Ordinales
    grade_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}
    emp_map = {'< 1 year': 0, '1 year': 1, '2 years': 2, '3 years': 3, '4 years': 4,
               '5 years': 5, '6 years': 6, '7 years': 7, '8 years': 8, '9 years': 9,
               '10+ years': 10, 'Unknown': -1}
    
    # Mapeo Sub-Grade (A1-G5)
    grades = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    sub_grades = [f"{g}{i}" for g in grades for i in range(1, 6)]
    sub_grade_map = {val: i+1 for i, val in enumerate(sub_grades)}

    if 'grade' in df_transformed.columns:
        df_transformed['grade'] = df_transformed['grade'].map(grade_map)
    if 'emp_length' in df_transformed.columns:
        df_transformed['emp_length'] = df_transformed['emp_length'].fillna('Unknown').map(emp_map)
    if 'sub_grade' in df_transformed.columns:
        df_transformed['sub_grade'] = df_transformed['sub_grade'].map(sub_grade_map)
    if 'term' in df_transformed.columns:
        df_transformed['term'] = df_transformed['term'].apply(lambda x: 1 if '60' in str(x) else 0)

    # C. Indicadores de Faltantes
    mths_cols = [c for c in df_transformed.columns if c.startswith('mths_since')]
    for col in mths_cols:
        df_transformed[f"{col}_missing"] = df_transformed[col].isna().astype(int)

    # D. One-Hot Encoding
    nom_cols = ['home_ownership', 'verification_status', 'purpose', 
                'pymnt_plan', 'initial_list_status', 'application_type']
    df_transformed = pd.get_dummies(df_transformed, columns=[c for c in nom_cols if c in df_transformed.columns], drop_first=True)

    # E. Imputación Numérica
    try:
        imputer_path = os.path.join(root_path, 'notebooks', 'num_imputer.pkl')
        if os.path.exists(imputer_path):
            imputer = joblib.load(imputer_path)
            num_cols = df_transformed.select_dtypes(include='number').columns
            df_transformed[num_cols] = imputer.transform(df_transformed[num_cols])
    except Exception as e:
        st.warning(f"Aviso: No se pudo aplicar el imputer ({e}).")

    # F. Alineación Final
    df_transformed = df_transformed.reindex(columns=FEATURES_CONSENSUS, fill_value=0)
    return df_transformed.astype(float)

def main():
    st.set_page_config(page_title="Simulador de Crédito", page_icon="🤖", layout="wide")
    st.title("🤖 Predicción de Riesgo Crediticio")

    # --- 3. CARGA DEL MODELO ---
    model_path = os.path.join(root_path, 'notebooks', 'credit_risk_model_bundle.pkl')
    
    if not os.path.exists(model_path):
        st.error(f"No se encontró el modelo en: {model_path}")
        return

    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    # --- 4. TABS DE ENTRADA ---
    tab1, tab2 = st.tabs(["👤 Evaluación Manual", "📂 Carga Masiva (CSV)"])

    with tab1:
        with st.form("manual_entry"):
            c1, c2, c3 = st.columns(3)
            with c1:
                loan_amnt = st.number_input("Monto ($)", value=10000)
                term = st.selectbox("Plazo", [" 36 months", " 60 months"])
                int_rate = st.number_input("Tasa Interés (%)", value=12.0)
            with c2:
                annual_inc = st.number_input("Ingreso Anual ($)", value=50000)
                fico = st.slider("FICO Score", 300, 850, 700)
                grade = st.selectbox("Grade", ["A", "B", "C", "D", "E", "F", "G"])
            with c3:
                sub_grade = st.text_input("Subgrade (A1-G5)", "A1")
                emp_length = st.selectbox("Antigüedad", ["< 1 year", "1 year", "5 years", "10+ years"])
                dti = st.number_input("DTI", value=15.0)

            btn = st.form_submit_button("Analizar Riesgo")

        if btn:
            input_df = pd.DataFrame([{
                'loan_amnt': loan_amnt, 'term': term, 'int_rate': int_rate,
                'annual_inc': annual_inc, 'fico_range_low': fico, 'grade': grade,
                'sub_grade': sub_grade, 'emp_length': emp_length, 'dti': dti
            }])
            ready = transformar_datos(input_df)
            prob = model.predict_proba(ready)[0][1]
            
            if prob < 0.3: st.success(f"✅ Riesgo Bajo: {prob:.2%}")
            elif prob < 0.6: st.warning(f"⚠️ Riesgo Medio: {prob:.2%}")
            else: st.error(f"🚨 Riesgo Alto: {prob:.2%}")

    with tab2:
        file = st.file_uploader("Subir CSV de clientes", type="csv")
        if file:
            df_csv = pd.read_csv(file)
            if st.button("Procesar Lote"):
                processed = transformar_datos(df_csv)
                preds = model.predict_proba(processed)[:, 1]
                df_csv['Prob_Default'] = preds
                st.dataframe(df_csv)
                st.download_button("Descargar Resultados", df_csv.to_csv(index=False), "predicciones.csv")

if __name__ == "__main__":
    main()