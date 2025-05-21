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
# Sidebar y Branding
# ----------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/684/684908.png", width=80)
    st.title("Set Cover AG")
    st.markdown("**Optimización de Cobertura de Clientes**")
    st.markdown("---")
    st.markdown("Creado por: *Jose Vicente* y *Nicolas Melendez*")
    st.markdown("Curso: Investigación de Operaciones 1")
    st.markdown("---")
    st.info("Usa el menú para navegar por los resultados.")

# ----------------------------
# Banner superior
# ----------------------------
st.markdown(
    """
    <div style="background: linear-gradient(90deg, #00CC96 0%, #636EFA 100%); padding: 1.2rem 2rem; border-radius: 12px; margin-bottom: 1.5rem;">
        <h1 style="color: white; margin-bottom: 0.2rem;">📡 Resultados del Algoritmo Genético para Cobertura de Clientes</h1>
        <p style="color: #f0f0f0; font-size: 1.1rem;">Visualiza y explora los resultados de la optimización de cobertura usando algoritmos genéticos.</p>
    </div>
    """, unsafe_allow_html=True
)

# ----------------------------
# Cargar y mostrar el JSON de resultados
# ----------------------------
with st.expander("📂 Mostrar JSON crudo"):
    with open("resultados_ga.json", "r") as file:
        resultados = json.load(file)
    st.json(resultados)

# ----------------------------
# Tabs principales
# ----------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Resumen", 
    "📈 Visualizaciones", 
    "📋 Tablas y Estadísticas", 
    "⬇️ Descargar"
])

with tab1:
    st.header("Resumen General")
    st.markdown("""
    Estas son las **métricas clave** que resumen el desempeño de la solución encontrada. 
    El objetivo principal es maximizar la cobertura de clientes mientras se minimiza 
    el costo total de implementación.
    """)
    # Tarjetas de métricas con colores personalizados
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
            <div style="background-color:#00CC96;padding:1.2rem 0.5rem;border-radius:10px;text-align:center;">
                <span style="font-size:2.2rem;color:white;">✅</span><br>
                <span style="font-size:1.3rem;color:white;"><b>{resultados['clientes_cubiertos']} / 500</b></span><br>
                <span style="color:white;">Clientes cubiertos</span>
            </div>
            """, unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div style="background-color:#636EFA;padding:1.2rem 0.5rem;border-radius:10px;text-align:center;">
                <span style="font-size:2.2rem;color:white;">📡</span><br>
                <span style="font-size:1.3rem;color:white;"><b>{resultados["antenas_activadas"]}</b></span><br>
                <span style="color:white;">Antenas activadas</span>
            </div>
            """, unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""
            <div style="background-color:#FFB300;padding:1.2rem 0.5rem;border-radius:10px;text-align:center;">
                <span style="font-size:2.2rem;color:white;">💰</span><br>
                <span style="font-size:1.3rem;color:white;"><b>${resultados['costo_total']:,}</b></span><br>
                <span style="color:white;">Costo total</span>
            </div>
            """, unsafe_allow_html=True
        )

with tab2:
    st.header("Visualizaciones Interactivas")

    # Gráfica de convergencia
    with st.spinner("Cargando gráfica de convergencia..."):
        try:
            image = Image.open("convergencia.png")
            st.image(image, caption="Evolución del costo total durante las generaciones", use_container_width=True)
        except FileNotFoundError:
            st.warning("⚠️ Archivo 'convergencia.png' no encontrado.")

    st.markdown("---")

    # Matriz de estado de antenas activadas/apagadas
    st.subheader("🛰️ Matriz de Estado de Antenas")
    filas, columnas = 20, 25
    estado_antenas = np.array(resultados["vector_binario"]).reshape(filas, columnas)
    fig, ax = plt.subplots(figsize=(12, 6))
    cmap = ListedColormap(["#CCCCCC", "#00CC96"])
    im = ax.imshow(estado_antenas, cmap=cmap, aspect="auto")
    for i in range(filas):
        for j in range(columnas):
            idx = i * columnas + j + 1
            ax.text(j, i, str(idx), ha="center", va="center", fontsize=7, color="black")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Matriz de Antenas: Verde=Activada, Gris=Apagada")
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")

    # Mapa de calor de costos de antenas activadas
    st.subheader("💸 Mapa de Calor de Costos de Antenas Activadas")
    total_antenas = 500
    costos_todas_flat = np.full(total_antenas, np.nan)
    for idx, costo in zip(resultados["indices_antenas"], resultados["costos_seleccionados"]):
        costos_todas_flat[idx - 1] = costo
    costos_todas = costos_todas_flat.reshape(filas, columnas)
    fig, ax = plt.subplots(figsize=(12, 6))
    cmap_heat = plt.cm.YlGn
    im = ax.imshow(costos_todas, cmap=cmap_heat)
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

    st.markdown("---")

    # Mostrar gráficos generados previamente
    st.subheader("👥 Clientes Cubiertos por Cada Antena")
    try:
        img_clientes = Image.open("clientes_por_antena.png")
        st.image(img_clientes, caption="Distribución de clientes cubiertos por antena activada", use_container_width=True)
    except FileNotFoundError:
        st.warning("⚠️ Archivo 'clientes_por_antena.png' no encontrado.")

    st.subheader("📊 Distribución de Costos de Antenas")
    try:
        img_histograma = Image.open("histograma_costos_antenas.png")
        st.image(img_histograma, caption="Frecuencia de antenas por rango de costo", use_container_width=True)
    except FileNotFoundError:
        st.warning("⚠️ Archivo 'histograma_costos_antenas.png' no encontrado.")

with tab3:
    st.header("Tablas y Estadísticas Detalladas")
    # Tabla de costos
    st.subheader("📋 Tabla de Costos por Antena")
    df_costos = pd.DataFrame({
        "Índice de Antena": resultados["indices_antenas"],
        "Costo": resultados["costos_seleccionados"]
    })
    st.dataframe(df_costos, use_container_width=True)

    # Gráfico de barras
    st.subheader("📊 Costo de Cada Antena Seleccionada")
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
    fig_box = plt.figure()
    plt.boxplot(df_costos["Costo"], vert=False, patch_artist=True, boxprops=dict(facecolor="#636EFA"))
    plt.xlabel("Costo")
    plt.title("Boxplot de Costos de Antenas Seleccionadas")
    st.pyplot(fig_box)

    # Estadísticas
    st.subheader("📊 Estadísticas de Costos de Antenas Activadas")
    costos_activadas = np.array(resultados["costos_seleccionados"])
    if costos_activadas.size > 0:
        st.markdown(
            f"""
            <ul>
                <li><b>Costo mínimo:</b> ${costos_activadas.min():,.0f}</li>
                <li><b>Costo máximo:</b> ${costos_activadas.max():,.0f}</li>
                <li><b>Costo promedio:</b> ${costos_activadas.mean():,.2f}</li>
                <li><b>Costo mediano:</b> ${np.median(costos_activadas):,.2f}</li>
            </ul>
            """, unsafe_allow_html=True
        )
    else:
        st.write("No hay antenas activadas.")

with tab4:
    st.header("⬇️ Descargar Resultados")
    json_str = json.dumps(resultados, indent=4)
    st.download_button("📥 Descargar JSON", data=json_str, file_name="resultados_ga.json", mime="application/json")

# ----------------------------
# Footer mejorado
# ----------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color: #888; font-size: 0.95rem;">
        Desarrollado como parte de una solución a un problema de <b>SET and COVER</b> para <i>Investigación de Operaciones 1</i>.<br>
        <span style="font-size:1.2rem;">🚀</span>
    </div>
    """, unsafe_allow_html=True
)