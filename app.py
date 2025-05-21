import streamlit as st
import json
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import plotly.figure_factory as ff
import plotly.subplots as sp

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap  # <-- Agrega esta línea


# ----------------------------
# Título Principal
# ----------------------------
st.set_page_config(page_title="Cobertura con AG", layout="wide")
st.title("📡 Resultados del Algoritmo Genético para Cobertura de Clientes")

# ----------------------------
# Cargar JSON
# ----------------------------
with st.expander("📂 Mostrar JSON crudo"):
    with open("resultados_ga.json", "r") as file:
        resultados = json.load(file)
    st.json(resultados)

# ----------------------------
# Métricas Principales
# ----------------------------
st.header("📊 Resumen General")
col1, col2, col3 = st.columns(3)
col1.metric("✅ Clientes cubiertos", f"{resultados['clientes_cubiertos']} / 500")
col2.metric("📡 Antenas activadas", resultados["antenas_activadas"])
col3.metric("💰 Costo total", f"${resultados['costo_total']:,}")

st.divider()

# ----------------------------
# Gráfica de Convergencia
# ----------------------------
st.header("📈 Convergencia del Algoritmo Genético")
image = Image.open("convergencia.png")
st.image(image, caption="Evolución del costo total durante las generaciones", use_container_width=True)

st.divider()

# ----------------------------
# Tabla y Análisis de Antenas Seleccionadas
# ----------------------------
st.header("📍 Análisis de Antenas Seleccionadas")

df_costos = pd.DataFrame({
    "Índice de Antena": resultados["indices_antenas"],
    "Costo": resultados["costos_seleccionados"]
})

# Mostrar la tabla
st.subheader("📋 Tabla de Costos por Antena")
st.dataframe(df_costos, use_container_width=True)


# Gráfico de barras: Costo por antena seleccionada
st.subheader("📊 Costo de Cada Antena Seleccionada (matplotlib)")

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(df_costos["Índice de Antena"], df_costos["Costo"], color="#00CC96", edgecolor="black", alpha=0.8)
ax.set_xlabel("Índice de Antena")
ax.set_ylabel("Costo")
ax.set_title("Costo de Cada Antena Seleccionada")
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
st.pyplot(fig)

# Boxplot
st.subheader("🧪 Boxplot del Costo de Antenas")
fig_box = px.box(df_costos, y="Costo", points="all", color_discrete_sequence=["#636EFA"])
st.plotly_chart(fig_box, use_container_width=True)

st.divider()

# Gráfico tipo matriz de antenas activadas/apagadas
st.subheader("🛰️ Matriz de Estado de Antenas (verde=activada, gris=apagada)")

# Configuración de la matriz
filas, columnas = 20, 25
estado_antenas = np.array(resultados["vector_binario"]).reshape(filas, columnas)

fig, ax = plt.subplots(figsize=(12, 6))
# Mapa de colores: 1 (True) es verde, 0 (False) es gris

cmap = ListedColormap(["#CCCCCC", "#00CC96"])

im = ax.imshow(estado_antenas, cmap=cmap, aspect="auto")

# Opcional: mostrar el número de antena en cada celda
for i in range(filas):
    for j in range(columnas):
        idx = i * columnas + j + 1
        ax.text(j, i, str(idx), ha="center", va="center", fontsize=7, color="black")

ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Matriz de Antenas: Verde=Activada, Gris=Apagada")
plt.tight_layout()
st.pyplot(fig)

st.divider()


# 1. Mapa de calor de costos de antenas activadas
st.subheader("💸 Mapa de Calor de Costos de Antenas Activadas")

# Crear vector de costos para todas las antenas (np.nan si está apagada)
total_antenas = 500
costos_todas_flat = np.full(total_antenas, np.nan)
for idx, costo in zip(resultados["indices_antenas"], resultados["costos_seleccionados"]):
    costos_todas_flat[idx - 1] = costo  # -1 porque los índices empiezan en 1

costos_todas = costos_todas_flat.reshape(filas, columnas)

fig, ax = plt.subplots(figsize=(12, 6))
cmap_heat = plt.cm.YlGn
im = ax.imshow(costos_todas, cmap=cmap_heat)

# Mostrar el costo solo si la antena está activada
for i in range(filas):
    for j in range(columnas):
        if not np.isnan(costos_todas[i, j]):
            ax.text(j, i, f"{int(costos_todas[i, j])}", ha="center", va="center", fontsize=7, color="black")

ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Mapa de Calor: Costo de Antenas Activadas")
plt.colorbar(im, ax=ax, label="Costo")
plt.tight_layout()
st.pyplot(fig)

# 2. Estadísticas de costos de antenas activadas
st.subheader("📊 Estadísticas de Costos de Antenas Activadas")
costos_activadas = np.array(resultados["costos_seleccionados"])
if costos_activadas.size > 0:
    st.markdown(
        f"- **Costo mínimo:** ${costos_activadas.min():,.0f}\n"
        f"- **Costo máximo:** ${costos_activadas.max():,.0f}\n"
        f"- **Costo promedio:** ${costos_activadas.mean():,.2f}\n"
        f"- **Costo mediano:** ${np.median(costos_activadas):,.2f}"
    )
else:
    st.write("No hay antenas activadas.")
    
    
st.divider()
# ----------------------------
# Descarga de Resultados
# ----------------------------
st.header("⬇️ Descargar Resultados")

json_str = json.dumps(resultados, indent=4)
st.download_button("📥 Descargar JSON", data=json_str, file_name="resultados_ga.json", mime="application/json")

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.caption("Desarrollado como parte de una solución a un problema de cobertura con técnicas de optimización evolutiva.")
