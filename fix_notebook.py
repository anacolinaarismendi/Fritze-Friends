import nbformat

with open('notebook_gas.ipynb', 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

# Re-write the training cell to make sure it's Linear Regression as requested
for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'code':
        if 'mejor_modelo = LinearRegression()' in cell.source or 'mejor_modelo = RandomForestRegressor' in cell.source:
            nb.cells[i].source = "# Entrenamos el modelo de Regresión Lineal (como solicitaste)\nmejor_modelo = LinearRegression()\nmejor_modelo.fit(X_scaled, y)"
            break

# Find the prediction cell
pred_cell_idx = -1
for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'code' and 'consumo_predicho = mejor_modelo.predict(X_futuro_scaled)' in cell.source:
        pred_cell_idx = i
        break

if pred_cell_idx != -1:
    # Add a new cell after the prediction cell to graph the results
    graph_code = """# Unimos los datos históricos con la predicción para graficar
df_historico = df_anual.copy()
df_historico['Tipo'] = 'Histórico'

df_prediccion = anios_futuros.copy()
df_prediccion = df_prediccion.rename(columns={'Consumo_m3_Estimado': 'Verbrauch'})
df_prediccion['Tipo'] = 'Predicción (Regresión Lineal)'

df_total = pd.concat([df_historico, df_prediccion], ignore_index=True)

# Graficamos con Plotly
fig = px.line(df_total, x='Anio', y='Verbrauch', color='Tipo', markers=True,
              title='Histórico de Consumo vs Predicción (Regresión Lineal)',
              labels={'Verbrauch': 'Consumo de Gas (m3)', 'Anio': 'Año'})

# Agregamos una línea vertical para separar el histórico del futuro
fig.add_vline(x=2026.5, line_dash="dash", line_color="gray", annotation_text="Futuro ->")
fig.show()"""
    
    new_cell = nbformat.v4.new_code_cell(source=graph_code)
    
    # Insert only if it doesn't already exist
    already_exists = False
    for cell in nb.cells:
        if cell.cell_type == 'code' and 'df_total = pd.concat' in cell.source:
            already_exists = True
            break
            
    if not already_exists:
        nb.cells.insert(pred_cell_idx + 1, new_cell)

with open('notebook_gas.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print("Notebook modificado correctamente.")
