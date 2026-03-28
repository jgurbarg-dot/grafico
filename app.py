import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Generador de Gráficos de Procesos", layout="wide")
st.title("📊 Generador de Gráficos: Multi-Serie y Alimentación")

# --- 1. CONFIGURACIÓN DE PARÁMETROS ---
with st.sidebar:
    st.header("⚙️ Configuración de Gráfico")
    x_label = st.text_input("Etiqueta General Eje X", "Fracción Molar x")
    y_label = st.text_input("Etiqueta General Eje Y", "Fracción Molar y")
    
    orientacion = st.radio("Orientación de las Series", 
                           ["Y vs X (Convencional)", "X vs Y (Inverso)"])
    
    st.divider()
    st.header("🍲 Condiciones de Alimentación")
    z_f = st.number_input("Composición Global (z_f)", value=0.50, min_value=0.0, max_value=1.0, step=0.01)
    q_val = st.number_input("Condición Térmica (q)", value=1.00, step=0.1)

# --- 2. ENTRADA DE DATOS (Múltiples Series) ---
st.subheader("📥 Ingreso de Series de Datos")
st.info("Puedes pegar datos desde Excel o llenar las columnas x1, y1 y x2, y2.")

# Creamos un DataFrame inicial vacío con las 4 columnas
df_init = pd.DataFrame(columns=['x1', 'y1', 'x2', 'y2'])
# Opcional: una fila de ejemplo
df_init.loc[0] = [0.0, 0.0, 0.0, 0.0]

data = st.data_editor(df_init, num_rows="dynamic", use_container_width=True)

# --- 3. LÓGICA DE PROCESAMIENTO Y GRÁFICO ---
if st.button("📈 Generar Gráfico Comparativo"):
    # Limpieza de datos
    data = data.apply(pd.to_numeric, errors='coerce').dropna(how='all')

    if data.empty:
        st.warning("No hay datos suficientes para graficar.")
    else:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Función auxiliar para graficar según la orientación elegida
        def plot_series(col_x, col_y, label, color):
            if col_x in data.columns and col_y in data.columns:
                temp_df = data[[col_x, col_y]].dropna()
                if not temp_df.empty:
                    val_x = temp_df[col_x]
                    val_y = temp_df[col_y]
                    
                    if orientacion == "X vs Y (Inverso)":
                        ax.plot(val_y, val_x, marker='o', label=label, color=color)
                    else:
                        ax.plot(val_x, val_y, marker='o', label=label, color=color)

        # Graficar Serie 1
        plot_series('x1', 'y1', 'Serie 1 (x1, y1)', '#1f77b4')
        
        # Graficar Serie 2
        plot_series('x2', 'y2', 'Serie 2 (x2, y2)', '#ff7f0e')

        # Graficar punto de alimentación (z_f)
        # Se suele graficar en la diagonal o como punto de referencia
        if orientacion == "Y vs X (Convencional)":
            ax.plot(z_f, z_f, 'ro', label=f'Alimentación (z={z_f})')
            ax.axvline(x=z_f, color='red', linestyle=':', alpha=0.5)
        else:
            ax.plot(z_f, z_f, 'ro', label=f'Alimentación (z={z_f})')
            ax.axhline(y=z_f, color='red', linestyle=':', alpha=0.5)

        # Estética del gráfico
        ax.set_xlabel(y_label if orientacion == "X vs Y (Inverso)" else x_label)
        ax.set_ylabel(x_label if orientacion == "X vs Y (Inverso)" else y_label)
        ax.set_title(f"Análisis de Equilibrio - q: {q_val}")
        
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend()
        
        # Forzar escala 0 a 1 si son fracciones molares
        if data.max().max() <= 1.1:
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            # Línea de 45 grados (identidad)
            ax.plot([0, 1], [0, 1], color='gray', linestyle='--', alpha=0.3)

        st.pyplot(fig)

        # Resumen de condiciones
        col_res1, col_res2 = st.columns(2)
        col_res1.metric("Composición Alim.", z_f)
        col_res2.metric("Calidad Vapor (q)", q_val)
