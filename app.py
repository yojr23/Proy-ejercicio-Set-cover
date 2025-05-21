import streamlit as st
import json
import pandas as pd
from PIL import Image

# Título principal
st.title("Resultados del Algoritmo Genético para Cobertura de Clientes")

# Cargar JSON
st.header("📄 Resultados Generales")
with open("resultados_ga.json", "r") as file:
    resultados = json.load(file)

# Mostrar métricas clave
st.metric("✅ Clientes cubiertos", f"{resultados['clientes_cubiertos']} / 500")
st.metric("📡 Antenas activadas", resultados["antenas_activadas"])
st.metric("💰 Costo total", f"${resultados['costo_total']:,}")

# Mostrar lista de antenas activadas
st.subheader("📍 Índices de Antenas Activadas")
st.write(resultados["indices_antenas"])

# Mostrar imagen de convergencia
st.subheader("📈 Gráfica de Convergencia del Algoritmo")
image = Image.open("convergencia.png")
st.image(image, caption="Evolución del costo total durante las generaciones")

# (Opcional) Mostrar tabla con los costos de las antenas seleccionadas
df_costos = pd.DataFrame({
    "Índice de Antena": resultados["indices_antenas"],
    "Costo": resultados["costos_seleccionados"]
})
st.subheader("💵 Costos de las Antenas Seleccionadas")
st.dataframe(df_costos)

# Footer
st.markdown("---")
st.caption("Desarrollado como parte de una solución a un problema de cobertura con técnicas de optimización.")
