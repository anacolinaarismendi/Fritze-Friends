import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

# Recreate df_anual based on notebook
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

print("Datos historicos:")
print(df_anual)

X = df_anual[['Anio']]
y = df_anual['Verbrauch']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

mejor_modelo = LinearRegression()
mejor_modelo.fit(X_scaled, y)

print(f"Coeficientes: {mejor_modelo.coef_}, Intercepto: {mejor_modelo.intercept_}")

anios_futuros = pd.DataFrame({'Anio': [2027, 2028, 2029, 2030, 2031]})
X_futuro_scaled = scaler.transform(anios_futuros[['Anio']])
print("X_futuro_scaled:")
print(X_futuro_scaled)

consumo_predicho = mejor_modelo.predict(X_futuro_scaled)
anios_futuros['Consumo_m3_Estimado'] = consumo_predicho
print("Prediccion:")
print(anios_futuros)
