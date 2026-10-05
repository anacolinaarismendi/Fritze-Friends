import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

nb = new_notebook()

nb.cells.append(new_markdown_cell("""# Predicción de Gasto de Gas (Incluyendo Precios de Mercado)
Este notebook toma el histórico de consumo de gas y los precios históricos en Alemania para entrenar un modelo que entienda cómo el precio afecta tu consumo, y así estimar tu gasto para los próximos 5 años."""))

nb.cells.append(new_code_cell("""%pip install pandas plotly matplotlib seaborn scikit-learn openpyxl
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
"""))

nb.cells.append(new_code_cell("""# 1. Cargar datos de consumo histórico
url_excel = 'data/export_zaehlerstandshistorie_891288_20261003.xlsx'
df = pd.read_excel(url_excel)
df = df.rename(columns={'Unnamed: 0': 'Fecha', 'Unnamed: 4': 'Zaehlerstand', 'Unnamed: 5': 'Verbrauch'})
df = df[['Fecha', 'Verbrauch']]

df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d.%m.%Y', errors='coerce')
df['Verbrauch'] = pd.to_numeric(df['Verbrauch'], errors='coerce')
df = df.dropna()
df['Anio'] = df['Fecha'].dt.year

df = df[df['Anio'] >= (df['Anio'].max() - 10)]
df = df.sort_values('Anio').reset_index(drop=True)

df_anual = df.groupby('Anio')['Verbrauch'].sum().reset_index()
"""))

nb.cells.append(new_code_cell("""# 2. Agregar los datos del precio histórico del gas en Alemania
# Datos de la BDEW (centavos por kWh) convertidos a EUR por m3 (1 m3 ~= 10 kWh)
precios_historicos = {
    2016: 0.60, 2017: 0.57, 2018: 0.57, 2019: 0.61, 2020: 0.60,
    2021: 0.63, 2022: 1.31, 2023: 1.42, 2024: 1.08, 2025: 1.20, 2026: 1.16
}
df_anual['Precio_Gas_EUR'] = df_anual['Anio'].map(precios_historicos)
df_anual['Gasto_Real_EUR'] = df_anual['Verbrauch'] * df_anual['Precio_Gas_EUR']
df_anual
"""))

nb.cells.append(new_code_cell("""# 3. Preparar datos para Machine Learning
# Ahora el modelo aprenderá usando el Año y el Precio del mercado
X = df_anual[['Anio', 'Precio_Gas_EUR']]
y = df_anual['Verbrauch']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Usamos Random Forest porque captura mejor la relación no lineal del consumo vs precio
mejor_modelo = RandomForestRegressor(random_state=42, n_estimators=100)
mejor_modelo.fit(X_scaled, y)
"""))

nb.cells.append(new_code_cell("""# 4. Predicción para los próximos 5 años
# Proyectamos un escenario de precios para el gas en Alemania (suponiendo una ligera estabilización/aumento)
anios_futuros = pd.DataFrame({
    'Anio': [2027, 2028, 2029, 2030, 2031],
    'Precio_Gas_EUR': [1.18, 1.20, 1.22, 1.24, 1.25]
})

X_futuro_scaled = scaler.transform(anios_futuros[['Anio', 'Precio_Gas_EUR']])

# El modelo predice cuánto consumirás, tomando en cuenta el precio futuro
anios_futuros['Verbrauch'] = mejor_modelo.predict(X_futuro_scaled)

# Calculamos el costo en base a la predicción
anios_futuros['Gasto_Estimado_EUR'] = anios_futuros['Verbrauch'] * anios_futuros['Precio_Gas_EUR']
anios_futuros
"""))

nb.cells.append(new_code_cell("""# 5. Unir y Graficar
df_historico = df_anual[['Anio', 'Verbrauch', 'Gasto_Real_EUR']].rename(columns={'Gasto_Real_EUR': 'Gasto_EUR'})
df_historico['Tipo'] = 'Histórico'

df_futuro = anios_futuros[['Anio', 'Verbrauch', 'Gasto_Estimado_EUR']].rename(columns={'Gasto_Estimado_EUR': 'Gasto_EUR'})
df_futuro['Tipo'] = 'Predicción'

df_total = pd.concat([df_historico, df_futuro], ignore_index=True)

# Gráfica de Consumo
fig1 = px.line(df_total, x='Anio', y='Verbrauch', color='Tipo', markers=True,
              title='Histórico vs Predicción: Consumo de Gas (m3)')
fig1.add_vline(x=2026.5, line_dash="dash", line_color="gray")
fig1.show()

# Gráfica de Gasto (Euros)
fig2 = px.line(df_total, x='Anio', y='Gasto_EUR', color='Tipo', markers=True,
              title='Histórico vs Predicción: Gasto Total en Gas (Euros)')
fig2.add_vline(x=2026.5, line_dash="dash", line_color="gray")
fig2.show()
"""))

with open('notebook_gas.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print("Notebook rescrito con éxito.")
