import streamlit as st

def main():
    st.set_page_config(page_title="Bienvenid@ al portal predictivo Sebas, Dorota y johan", page_icon="🤖", layout="centered")

    st.title("Bienvenid@ al portal predictivo de la empresa Sebas, Dorota y johan")
    st.write("**Por favor seleccione el servicio predictivo que desea utilizar**")

    opcion = st.radio(
        "Seleccione el servicio:",
        ("Predicción de demanda", "Predicción de rotura de stock"),
        index=None
    )
    if opcion == "Predicción de demanda":
        st.info(
        """
        📈 **¿Qué hace este servicio?**  
        Predice cuántas unidades se venderán de un producto en un periodo futuro 
        (por ejemplo, por semana o por mes).

        📊 **¿Qué datos se necesitan?**  
        - Ventas históricas  
        - Precio del producto  
        - Descuentos aplicados  
        - Tipo de prenda / categoría  
        - Fecha o periodo de predicción  
        """
    )

    elif opcion == "Predicción de rotura de stock":
        st.info(
        """
        ⚠️ **¿Qué hace este servicio?**  
        Predice la probabilidad de que un producto se quede sin stock en el corto plazo.

        📦 **¿Qué datos se necesitan?**  
        - Stock actual  
        - Ventas recientes  
        - Tiempo estimado de reposición  
        - Tipo de producto / tienda  
        """
    )

    st.markdown("---")

    if opcion == "Predicción de demanda":
        way_to_pred = st.radio(
            "¿Cómo desea realizar la predicción de demanda?",
            ("Ingresando datos manualmente", "Subiendo un archivo CSV"),
            index=None
        )

        st.markdown("### Ir a la página")

        if way_to_pred == "Ingresando datos manualmente":
            st.page_link("pages/pred_dem_man.py", label="➡️ Predicción demanda (manual)", icon="📈")
        elif way_to_pred == "Subiendo un archivo CSV":
            st.page_link("pages/pred_dem_csv.py", label="➡️ Predicción demanda (CSV)", icon="📄")

    elif opcion == "Predicción de rotura de stock":
        way_to_pred = st.radio(
            "¿Cómo desea realizar de rotura de stock?",
            ("Ingresando datos manualmente", "Subiendo un archivo CSV"),
            index=None
        )

        st.markdown("### Ir a la página")

        if way_to_pred == "Ingresando datos manualmente":
            st.page_link("pages/pred_stock_csv.py", label="➡️ Predicción de rotura de stock (manual)", icon="📈")
        elif way_to_pred == "Subiendo un archivo CSV":
            st.page_link("pages/pred_stock_man.py", label="➡️ Predicción de rotura de stock (CSV)", icon="📄")

    else:
        st.info("Selecciona una opción para ver los accesos.")

if __name__ == "__main__":
    main()


# Local: python -m streamlit run streamlit_tutorial.py
# Streamlit Sharing 