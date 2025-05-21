# ----------------------------
# Importación de librerías
# ----------------------------
import streamlit as st
import json
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

# ----------------------------
# Configuración de la página
# ----------------------------
st.set_page_config(page_title="Cobertura con AG", layout="wide")
st.title("📡 Resultados del Algoritmo Genético para Cobertura de Clientes")

# ----------------------------
# Cargar y mostrar el JSON de resultados
# ----------------------------
with st.expander("📂 Mostrar JSON crudo"):
    with open("resultados_ga.json", "r") as file:
        resultados = json.load(file)
    st.json(resultados)

# ----------------------------
# Métricas principales del modelo
# ----------------------------
st.header("📊 Resumen General")
col1, col2, col3 = st.columns(3)
col1.metric("✅ Clientes cubiertos", f"{resultados['clientes_cubiertos']} / 500")
col2.metric("📡 Antenas activadas", resultados["antenas_activadas"])
col3.metric("💰 Costo total", f"${resultados['costo_total']:,}")

st.divider()

# ----------------------------
# Gráfica de convergencia del algoritmo genético
# ----------------------------
st.header("📈 Convergencia del Algoritmo Genético")
try:
    image = Image.open("convergencia.png")
    st.image(image, caption="Evolución del costo total durante las generaciones", use_container_width=True)
except FileNotFoundError:
    st.warning("⚠️ Archivo 'convergencia.png' no encontrado.")

st.divider()

# ----------------------------
# Tabla y análisis de antenas seleccionadas
# ----------------------------
st.header("📍 Análisis de Antenas Seleccionadas")

# Crear un DataFrame con los costos de las antenas seleccionadas
df_costos = pd.DataFrame({
    "Índice de Antena": resultados["indices_antenas"],
    "Costo": resultados["costos_seleccionados"]
})

# Mostrar la tabla de costos
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

# Boxplot de los costos de las antenas seleccionadas
st.subheader("🧪 Boxplot del Costo de Antenas")
fig_box = plt.figure()
plt.boxplot(df_costos["Costo"], vert=False, patch_artist=True, boxprops=dict(facecolor="#636EFA"))
plt.xlabel("Costo")
plt.title("Boxplot de Costos de Antenas Seleccionadas")
st.pyplot(fig_box)

st.divider()

# ----------------------------
# Estadísticas de costos de antenas activadas
# ----------------------------
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
# Matriz de estado de antenas activadas/apagadas
# ----------------------------
st.subheader("🛰️ Matriz de Estado de Antenas (verde=activada, gris=apagada)")

# Configuración de la matriz (20 filas x 25 columnas)
filas, columnas = 20, 25
estado_antenas = np.array(resultados["vector_binario"]).reshape(filas, columnas)

fig, ax = plt.subplots(figsize=(12, 6))
cmap = ListedColormap(["#CCCCCC", "#00CC96"])  # Gris para apagadas, verde para activadas
im = ax.imshow(estado_antenas, cmap=cmap, aspect="auto")

# Mostrar el índice de cada antena en la celda correspondiente
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

# ----------------------------
# Mapa de calor de costos de antenas activadas
# ----------------------------
st.subheader("💸 Mapa de Calor de Costos de Antenas Activadas")

# Crear un vector de costos para todas las antenas (np.nan si está apagada)
total_antenas = 500
costos_todas_flat = np.full(total_antenas, np.nan)
for idx, costo in zip(resultados["indices_antenas"], resultados["costos_seleccionados"]):
    costos_todas_flat[idx - 1] = costo  # -1 porque los índices empiezan en 1

costos_todas = costos_todas_flat.reshape(filas, columnas)

fig, ax = plt.subplots(figsize=(12, 6))
cmap_heat = plt.cm.YlGn  # Colormap para el mapa de calor
im = ax.imshow(costos_todas, cmap=cmap_heat)

# Mostrar el costo en cada celda activada
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

st.divider()

# ----------------------------
# Mostrar gráficos generados previamente
# ----------------------------
# Gráfica de clientes cubiertos por antena
st.subheader("👥 Clientes Cubiertos por Cada Antena")
try:
    img_clientes = Image.open("clientes_por_antena.png")
    st.image(img_clientes, caption="Distribución de clientes cubiertos por antena activada", use_container_width=True)
except FileNotFoundError:
    st.warning("⚠️ Archivo 'clientes_por_antena.png' no encontrado.")

# Histograma de costos de antenas
st.subheader("📊 Distribución de Costos de Antenas")
try:
    img_histograma = Image.open("histograma_costos_antenas.png")
    st.image(img_histograma, caption="Frecuencia de antenas por rango de costo", use_container_width=True)
except FileNotFoundError:
    st.warning("⚠️ Archivo 'histograma_costos_antenas.png' no encontrado.")

st.divider()

# ----------------------------
# Descarga de resultados
# ----------------------------
st.header("⬇️ Descargar Resultados")
json_str = json.dumps(resultados, indent=4)
st.download_button("📥 Descargar JSON", data=json_str, file_name="resultados_ga.json", mime="application/json")

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.caption("Desarrollado como parte de una solución a un problema de SET and COVER para investigación de operaciones 1.")