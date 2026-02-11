import pandas as pd
import numpy as np

def transformar_datos(df, features_list):
    df_transformed = df.copy()

    # 1. Manejo de Fechas (Credit Age) - Basado en tu código
    if 'issue_d' in df_transformed.columns and 'earliest_cr_line' in df_transformed.columns:
        df_transformed['issue_d'] = pd.to_datetime(df_transformed['issue_d'])
        df_transformed['earliest_cr_line'] = pd.to_datetime(df_transformed['earliest_cr_line'])
        ref_date = df_transformed['issue_d'].max()
        df_transformed['credit_age'] = (ref_date - df_transformed['earliest_cr_line']).dt.days / 365

    # 2. Mapeos manuales (Grade, Emp_length, Term) - Según tu código
    grade_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}
    emp_map = {'< 1 year': 0, '1 year': 1, '2 years': 2, '3 years': 3, '4 years': 4,
               '5 years': 5, '6 years': 6, '7 years': 7, '8 years': 8, '9 years': 9,
               '10+ years': 10, 'Unknown': -1}
    
    if 'grade' in df_transformed.columns:
        df_transformed['grade'] = df_transformed['grade'].map(grade_map)
    if 'emp_length' in df_transformed.columns:
        df_transformed['emp_length'] = df_transformed['emp_length'].fillna('Unknown').map(emp_map)
    if 'term' in df_transformed.columns:
        df_transformed['term'] = df_transformed['term'].apply(lambda x: 1 if '60' in str(x) else 0)

    # 3. Sub-Grade Mapping (A1=1, A2=2...) - Según tu código
    # Generamos la lista de A1 a G5 para que el mapeo sea idéntico
    grades = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    sub_grades_sorted = [f"{g}{i}" for g in grades for i in range(1, 6)]
    sub_grade_map = {val: i+1 for i, val in enumerate(sub_grades_sorted)}
    
    if 'sub_grade' in df_transformed.columns:
        df_transformed['sub_grade'] = df_transformed['sub_grade'].map(sub_grade_map)

    # 4. Indicadores de faltantes para 'mths_since' - Según tu código
    mths_cols = [c for c in df_transformed.columns if c.startswith('mths_since')]
    for col in mths_cols:
        df_transformed[f"{col}_missing"] = df_transformed[col].isna().astype(int)

    # 5. One-Hot Encoding para nominales - Según tu código
    nom_cols = ['home_ownership', 'verification_status', 'purpose', 
                'pymnt_plan', 'initial_list_status', 'application_type']
    df_transformed = pd.get_dummies(df_transformed, columns=[c for c in nom_cols if c in df_transformed.columns], drop_first=True)

    # 6. ALINEACIÓN FINAL CON EL MODELO (Crucial)
    # Esto asegura que el DF final tenga exactamente las mismas columnas que el entrenamiento
    df_transformed = df_transformed.reindex(columns=features_list, fill_value=0)
    
    return df_transformed.astype(float)