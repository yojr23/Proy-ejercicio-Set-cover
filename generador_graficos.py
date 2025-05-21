import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

# 1. Leer archivos de entrada
df_cover = pd.read_csv("set_cover_500x500.csv", header=None)
df_cover = df_cover.iloc[:500,:]
print(df_cover.shape)
df_costos = pd.read_excel("Costo_S.xlsx", header=None)
costos = df_costos.iloc[1, 1:501].values.astype(float)

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

# Clientes cubiertos por cada antena activada
clientes_por_antena = df_cover.iloc[:, indices_activadas].sum(axis=0)

plt.figure(figsize=(8,4))
bars = plt.bar(range(1, len(indices_activadas)+1), clientes_por_antena, color='skyblue')

# Resalta la barra 95 en rojo (índice 94 porque Python es base 0)
if len(indices_activadas) >= 95:
    bars[94].set_color('red')
plt.xlabel("Antena activada (índice en la solución)")
plt.ylabel("Clientes cubiertos")
plt.title("Clientes cubiertos por cada antena activada\n(Antena 95 resaltada en rojo)")
plt.tight_layout()
plt.show()

# Antenas que cubren a cada cliente
antenas_por_cliente = df_cover.iloc[:, indices_activadas].sum(axis=1)

plt.figure(figsize=(8,4))
n, bins, patches = plt.hist(costos_activadas, bins=15, edgecolor='black')
plt.xlabel("Costo de antena activada")
plt.ylabel("Cantidad")
plt.title("Distribución de costos de antenas activadas")
plt.tight_layout()

# Agrega el número encima de cada barra
for i in range(len(n)):
    plt.text((bins[i] + bins[i+1]) / 2, n[i], int(n[i]), ha='center', va='bottom')

plt.show()

