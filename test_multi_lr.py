import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

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

precios_historicos = {
    2016: 0.60, 2017: 0.57, 2018: 0.57, 2019: 0.61, 2020: 0.60,
    2021: 0.63, 2022: 1.31, 2023: 1.42, 2024: 1.08, 2025: 1.20, 2026: 1.16
}
df_anual['Precio_Gas_EUR'] = df_anual['Anio'].map(precios_historicos)

X = df_anual[['Anio', 'Precio_Gas_EUR']]
y = df_anual['Verbrauch']
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

lr = LinearRegression()
lr.fit(X_scaled, y)

anios_futuros = pd.DataFrame({
    'Anio': [2027, 2028, 2029, 2030, 2031],
    'Precio_Gas_EUR': [1.18, 1.20, 1.22, 1.24, 1.25]
})
X_fut_scaled = scaler.transform(anios_futuros[['Anio', 'Precio_Gas_EUR']])
print("LR Predict:")
print(lr.predict(X_fut_scaled))
