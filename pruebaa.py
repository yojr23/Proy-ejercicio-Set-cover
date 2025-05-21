# Unificación y análisis de cobertura y costos para el problema Set Cover
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

# 1. Leer archivos de entrada
df_cover = pd.read_csv("set_cover_500x500.csv", header=None)
df_costos = pd.read_excel("Costo_S.xlsx", header=1)
costos = df_costos.values.flatten()[:500]  # Asegúrate de tener solo 500 costos

with open("resultados_ga.json", "r") as f:
    resultados = json.load(f)

vector_binario = np.array(resultados["vector_binario"])
indices_activadas = np.where(vector_binario == 1)[0]
costos_activadas = costos[indices_activadas]

# 2. DataFrame resumen de antenas
df_antenas = pd.DataFrame({
    "Antena": np.arange(1, 501),
    "Activada": vector_binario,
    "Costo": costos
})

# 3. Cobertura de clientes lograda por la solución
clientes_cubiertos = (df_cover.iloc[:, indices_activadas].sum(axis=1) > 0)
num_clientes_cubiertos = clientes_cubiertos.sum()

print(f"Clientes cubiertos: {num_clientes_cubiertos} / 500")
print(f"Antenas activadas: {len(indices_activadas)}")
print(f"Costo total: ${costos_activadas.sum():,.0f}")

# 4. Estadísticas de costos de antenas activadas
if len(costos_activadas) > 0:
    print(f"Costo mínimo: ${costos_activadas.min():,.0f}")
    print(f"Costo máximo: ${costos_activadas.max():,.0f}")
    print(f"Costo promedio: ${costos_activadas.mean():,.2f}")
    print(f"Costo mediano: ${np.median(costos_activadas):,.2f}")
else:
    print("No hay antenas activadas.")

# 5. Visualización: Cobertura de clientes
plt.figure(figsize=(10, 2))
plt.bar(range(1, 501), clientes_cubiertos.astype(int))
plt.xlabel("Cliente")
plt.ylabel("¿Cubierto?")
plt.title("Cobertura de clientes por la solución encontrada")
plt.tight_layout()
plt.show()

# 6. Visualización: Mapa de calor de costos de antenas activadas
filas, columnas = 20, 25
costos_todas_flat = np.full(500, np.nan)
costos_todas_flat[indices_activadas] = costos_activadas
costos_todas = costos_todas_flat.reshape(filas, columnas)

plt.figure(figsize=(12, 6))
im = plt.imshow(costos_todas, cmap=plt.cm.YlGn)
for i in range(filas):
    for j in range(columnas):
        if not np.isnan(costos_todas[i, j]):
            plt.text(j, i, f"{int(costos_todas[i, j])}", ha="center", va="center", fontsize=7, color="black")
plt.xticks([])
plt.yticks([])
plt.title("Mapa de Calor: Costo de Antenas Activadas")
plt.colorbar(im, label="Costo")
plt.tight_layout()
plt.show()

# 7. Guardar DataFrame resumen
df_antenas.to_csv("antenas_unificadas.csv", index=False)