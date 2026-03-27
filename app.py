import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title("📊 Generador de Gráficos Profesional")

# 1. Configuración de etiquetas
col1, col2 = st.columns(2)
with col1:
    x_label = st.text_input("Etiqueta Eje X", "Eje X")
with col2:
    y_label = st.text_input("Etiqueta Eje Y", "Eje Y")

tipo = st.selectbox("Orientación de los datos", ["Y vs X", "X vs Y"])

# 2. Entrada de datos mejorada
st.subheader("📥 Ingresar datos")
df_input = pd.DataFrame({x_label: [0.0], y_label: [0.0]}) # Valor inicial para ayudar al editor

data = st.data_editor(df_input, num_rows="dynamic")

# 3. Lógica del gráfico
if st.button("📈 Generar gráfico"):
    # Limpiamos datos vacíos o nulos
    data = data.dropna()

    if data.empty or len(data) < 2:
        st.warning("Por favor, ingresa al menos dos puntos para graficar.")
    else:
        try:
            # Convertimos a numérico por seguridad
            x = pd.to_numeric(data[x_label])
            y = pd.to_numeric(data[y_label])

            if tipo == "X vs Y":
                x, y = y, x
                actual_x_label, actual_y_label = y_label, x_label
            else:
                actual_x_label, actual_y_label = x_label, y_label

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(x, y, marker='o', linestyle='-', color='#1f77b4', label="Tendencia")
            
            ax.set_xlabel(actual_x_label)
            ax.set_ylabel(actual_y_label)
            ax.set_title(f"Gráfico de {actual_y_label} en función de {actual_x_label}")
            
            # Grilla y estilo
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Solo usamos el paso de 0.1 si el rango es pequeño (ej. química/laboratorio)
            # Si el rango es grande, dejamos que Matplotlib decida
            rango_x = max(x) - min(x)
            if rango_x < 5: 
                ax.set_xticks(np.arange(min(x), max(x) + 0.1, 0.1))

            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Hubo un error con los datos: {e}")
