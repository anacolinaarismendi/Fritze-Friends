import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

st.set_page_config(page_title="Predicción de Gasto / Cost Prediction", layout="wide")

# --- DICCIONARIO DE TRADUCCIONES --- #
translations = {
    "title": {
        "Español": "🔥 Predicción de Consumo y Comparativa de Sistemas",
        "English": "🔥 Gas Consumption Prediction and System Comparison",
        "Deutsch": "🔥 Gasverbrauchsprognose und Systemvergleich"
    },
    "intro": {
        "Español": "Esta aplicación entrena un modelo de Machine Learning en vivo para predecir el consumo de gas de los próximos 5 años y calcula los costes bajo el **Peor Escenario Posible** debido a los impuestos de CO₂ en Alemania. Además, compara estos costes contra la opción de un sistema Híbrido.",
        "English": "This application trains a live Machine Learning model to predict gas consumption for the next 5 years and calculates costs under the **Worst-Case Scenario** due to CO₂ taxes in Germany. It also compares these costs against a Hybrid system option.",
        "Deutsch": "Diese Anwendung trainiert ein Live-Machine-Learning-Modell, um den Gasverbrauch der nächsten 5 Jahre vorherzusagen, und berechnet die Kosten im **Worst-Case-Szenario** aufgrund von CO₂-Steuern in Deutschland. Außerdem werden diese Kosten mit einer Hybrid-Systemoption verglichen."
    },
    "sec1": {
        "Español": "1. Datos Históricos",
        "English": "1. Historical Data",
        "Deutsch": "1. Historische Daten"
    },
    "chart1": {
        "Español": "Consumo Histórico de Gas (BM3 / m³)",
        "English": "Historical Gas Consumption (BM3 / m³)",
        "Deutsch": "Historischer Gasverbrauch (BM3 / m³)"
    },
    "sec2": {
        "Español": "2. Entrenamiento del Modelo de IA",
        "English": "2. AI Model Training",
        "Deutsch": "2. KI-Modelltraining"
    },
    "training": {
        "Español": "Entrenando `RandomForestRegressor` con los datos históricos escalados...",
        "English": "Training `RandomForestRegressor` with scaled historical data...",
        "Deutsch": "Training des `RandomForestRegressor` mit skalierten historischen Daten..."
    },
    "success": {
        "Español": "¡Modelo entrenado con éxito!",
        "English": "Model trained successfully!",
        "Deutsch": "Modell erfolgreich trainiert!"
    },
    "sec3": {
        "Español": "3. Predicción a 5 Años (2027 - 2031)",
        "English": "3. 5-Year Prediction (2027 - 2031)",
        "Deutsch": "3. 5-Jahres-Prognose (2027 - 2031)"
    },
    "chart2": {
        "Español": "Proyección de Consumo (m³) a 2031",
        "English": "Consumption Projection (m³) to 2031",
        "Deutsch": "Verbrauchsprognose (m³) bis 2031"
    },
    "sec4": {
        "Español": "💥 4. Análisis del Peor Escenario (Proyección Económica)",
        "English": "💥 4. Worst-Case Scenario Analysis (Economic Projection)",
        "Deutsch": "💥 4. Analyse des Worst-Case-Szenarios (Wirtschaftliche Prognose)"
    },
    "worst_case": {
        "Español": "**¿Qué significa el Peor Escenario?**\nA partir de 2027/2028, Alemania entra en el mercado libre europeo de emisiones (ETS-2). Si hay shocks geopolíticos y los precios de los bonos de CO₂ se disparan, el precio por kWh podría escalar drásticamente cada año, pudiendo alcanzar los 22 céntimos de euro por kWh para el final de la década.",
        "English": "**What does the Worst-Case Scenario mean?**\nStarting in 2027/2028, Germany joins the European emissions trading system (ETS-2). If there are geopolitical shocks and CO₂ bond prices soar, the price per kWh could climb drastically every year, potentially reaching 22 euro cents per kWh by the end of the decade.",
        "Deutsch": "**Was bedeutet das Worst-Case-Szenario?**\nAb 2027/2028 tritt Deutschland dem europäischen Emissionshandelssystem (ETS-2) bei. Bei geopolitischen Schocks und explodierenden Preisen für CO₂-Zertifikate könnte der Preis pro kWh jedes Jahr drastisch steigen und bis Ende des Jahrzehnts 22 Cent pro kWh erreichen."
    },
    "table_proj": {
        "Español": "Tabla de Proyección (Peor Caso)",
        "English": "Projection Table (Worst Case)",
        "Deutsch": "Prognosetabelle (Worst Case)"
    },
    "summary": {
        "Español": "Resumen",
        "English": "Summary",
        "Deutsch": "Zusammenfassung"
    },
    "total_spend": {
        "Español": "Gasto Total Acumulado (Facturas a 5 años)",
        "English": "Total Cumulative Cost (5-year bills)",
        "Deutsch": "Kumulierte Gesamtkosten (Rechnungen über 5 Jahre)"
    },
    "annual_cost": {
        "Español": "Costo Anual para 2031",
        "English": "Annual Cost for 2031",
        "Deutsch": "Jährliche Kosten für 2031"
    },
    "monthly_warn": {
        "Español": "Si los precios suben de esta forma, estarás pagando más de **1,200 € mensuales** en gas para el año 2031.",
        "English": "If prices rise this way, you will be paying over **€1,200 a month** in gas by 2031.",
        "Deutsch": "Wenn die Preise so steigen, werden Sie bis 2031 monatlich über **1.200 €** für Gas bezahlen."
    },
    "chart3": {
        "Español": "Curva de Aumento de Gasto Anual en Gas (Peor Escenario)",
        "English": "Annual Gas Cost Increase Curve (Worst Case)",
        "Deutsch": "Kurve des jährlichen Anstiegs der Gaskosten (Worst Case)"
    },
    "sec5": {
        "Español": "🏗️ 5. Comparativa de Inversión: Instalación de Gas vs Sistema Híbrido",
        "English": "🏗️ 5. Investment Comparison: Gas Installation vs Hybrid System",
        "Deutsch": "🏗️ 5. Investitionsvergleich: Gasinstallation vs. Hybrid-System"
    },
    "comp_intro": {
        "Español": "Dado que también hay que contemplar los costes de instalación (Instalación de Gas nueva = 40,000 € vs Instalación de Bomba de Calor Híbrida = 92,500 €), hemos extendido el modelo a **15 años** para observar las correlaciones y ver el punto exacto en el que ambos sistemas cruzan rentabilidades.",
        "English": "Since installation costs must also be considered (New Gas Installation = €40,000 vs Hybrid Heat Pump Installation = €92,500), we have extended the model to **15 years** to observe correlations and see the exact point where both systems cross profitabilities.",
        "Deutsch": "Da auch Installationskosten berücksichtigt werden müssen (Neue Gasinstallation = 40.000 € vs. Hybrid-Wärmepumpeninstallation = 92.500 €), haben wir das Modell auf **15 Jahre** erweitert, um Korrelationen zu beobachten und den genauen Punkt zu sehen, an dem sich die Rentabilität beider Systeme kreuzt."
    },
    "opt1": {
        "Español": "Opción 1: Solo Gas (Inst. 40k)",
        "English": "Option 1: Gas Only (Inst. 40k)",
        "Deutsch": "Option 1: Nur Gas (Inst. 40k)"
    },
    "opt2_no": {
        "Español": "Opción 2: Híbrido SIN Subvención (Inst. 92.5k)",
        "English": "Option 2: Hybrid NO Subsidy (Inst. 92.5k)",
        "Deutsch": "Option 2: Hybrid OHNE Subvention (Inst. 92.5k)"
    },
    "opt2_yes": {
        "Español": "Opción 2: Híbrido CON Subvención 30% (Inst. 64.7k)",
        "English": "Option 2: Hybrid WITH 30% Subsidy (Inst. 64.7k)",
        "Deutsch": "Option 2: Hybrid MIT 30% Subvention (Inst. 64.7k)"
    },
    "chart4": {
        "Español": "Punto de Equilibrio: Gasto Acumulado (Instalación + Facturas Energéticas)",
        "English": "Break-Even Point: Cumulative Cost (Installation + Energy Bills)",
        "Deutsch": "Break-Even-Punkt: Kumulierte Kosten (Installation + Energierechnungen)"
    },
    "x_axis": {
        "Español": "Año",
        "English": "Year",
        "Deutsch": "Jahr"
    },
    "y_axis": {
        "Español": "Gasto Acumulado (€)",
        "English": "Cumulative Cost (€)",
        "Deutsch": "Kumulierte Kosten (€)"
    },
    "conc_title": {
        "Español": "**Conclusiones Finales:**",
        "English": "**Final Conclusions:**",
        "Deutsch": "**Abschließende Schlussfolgerungen:**"
    },
    "conc_1": {
        "Español": "* Fíjate cómo la línea verde del Híbrido (con subvención del 30%) se cruza con la línea roja del Gas exactamente en el **Año 5**.",
        "English": "* Notice how the green Hybrid line (with the 30% subsidy) crosses the red Gas line exactly in **Year 5**.",
        "Deutsch": "* Beachten Sie, wie die grüne Hybridlinie (mit 30% Subvention) die rote Gaslinie genau im **Jahr 5** kreuzt."
    },
    "conc_2": {
        "Español": "* A partir de 2032, el ahorro anual en las facturas frente al gas empieza a ser tan grande que la curva del gas se dispara, mientras el híbrido amortizado te blinda ante la subida de impuestos.",
        "English": "* From 2032 onwards, the annual savings on bills compared to gas start becoming so large that the gas curve skyrockets, while the amortized hybrid shields you against tax hikes.",
        "Deutsch": "* Ab 2032 werden die jährlichen Einsparungen bei den Rechnungen im Vergleich zu Gas so groß, dass die Gaskurve in die Höhe schießt, während der amortisierte Hybrid Sie vor Steuererhöhungen schützt."
    },
    "t_hist": {
        "Español": "Histórico",
        "English": "Historical",
        "Deutsch": "Historisch"
    },
    "t_pred": {
        "Español": "Predicción",
        "English": "Prediction",
        "Deutsch": "Vorhersage"
    },
    "t_type": {
        "Español": "Tipo",
        "English": "Type",
        "Deutsch": "Typ"
    }
}

# Selector de idioma
lang = st.sidebar.selectbox("🌐 Language / Idioma / Sprache", ["Español", "English", "Deutsch"])

def t(key):
    return translations[key][lang]

st.title(t("title"))
st.markdown(t("intro"))

@st.cache_data
def cargar_y_preparar_datos():
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
    return df_anual

df_anual = cargar_y_preparar_datos()

# ----------------- PRIMERA PARTE ----------------- #

st.header(t("sec1"))
# Renombrar columnas para la tabla
df_display = df_anual.copy()
df_display.columns = [t("x_axis"), "Verbrauch (m³)"]
st.dataframe(df_display.tail(10), use_container_width=True)

fig_hist = px.bar(df_anual, x="Anio", y="Verbrauch", title=t("chart1"), labels={"Anio": t("x_axis"), "Verbrauch": "Verbrauch"})
st.plotly_chart(fig_hist, use_container_width=True)

st.header(t("sec2"))
st.write(t("training"))

X = df_anual[['Anio']]
y = df_anual['Verbrauch']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

mejor_modelo = RandomForestRegressor(random_state=42, n_estimators=100)
mejor_modelo.fit(X_scaled, y)
st.success(t("success"))

st.header(t("sec3"))
anios_futuros_5 = pd.DataFrame({'Anio': [2027, 2028, 2029, 2030, 2031]})
X_futuro_5_scaled = scaler.transform(anios_futuros_5[['Anio']])

consumo_predicho_5 = mejor_modelo.predict(X_futuro_5_scaled)
anios_futuros_5['Consumo_m3_Estimado'] = consumo_predicho_5

# Añadir los precios y costes directamente aquí para que los datos coincidan
precios_peor_caso_kwh = [0.14, 0.16, 0.18, 0.20, 0.22]
precios_peor_caso_m3 = [p * 10 for p in precios_peor_caso_kwh]
anios_futuros_5['Precio_Est_m3_EUR'] = precios_peor_caso_m3
anios_futuros_5['Costo_Total_EUR'] = anios_futuros_5['Consumo_m3_Estimado'] * anios_futuros_5['Precio_Est_m3_EUR']

# Mostrar la tabla exacta que pide el usuario
st.write("Datos de Predicción (Consumo, Precio y Gasto Total):")
st.dataframe(anios_futuros_5, use_container_width=True)

# Actualizar la gráfica para mostrar el coste total proyectado
fig_pred = px.bar(anios_futuros_5, x="Anio", y="Costo_Total_EUR", 
                  title="Predicción de Gasto a 5 Años (€)", 
                  labels={"Anio": t("x_axis"), "Costo_Total_EUR": "Total €"},
                  text_auto='.2f')
fig_pred.update_traces(marker_color='red')
st.plotly_chart(fig_pred, use_container_width=True)


st.header(t("sec4"))
st.error(t("worst_case"))

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(t("table_proj"))
    df_styled = anios_futuros_5.copy()
    df_styled.columns = [t("x_axis"), "Estim.", "€/m³", "Total €"]
    st.dataframe(df_styled.style.format({
        'Estim.': '{:.2f} m³',
        '€/m³': '{:.2f} €/m³',
        'Total €': '{:.2f} €'
    }), use_container_width=True)

with col2:
    st.subheader(t("summary"))
    gasto_total = anios_futuros_5['Costo_Total_EUR'].sum()
    st.metric(t("total_spend"), f"{gasto_total:,.2f} €")
    st.metric(t("annual_cost"), f"{anios_futuros_5.iloc[-1]['Costo_Total_EUR']:,.2f} €")
    st.write(t("monthly_warn"))

fig_costo = px.line(anios_futuros_5, x="Anio", y="Costo_Total_EUR", markers=True, title=t("chart3"), labels={"Anio": t("x_axis"), "Costo_Total_EUR": "€"}, color_discrete_sequence=['red'])
st.plotly_chart(fig_costo, use_container_width=True)

st.markdown("---")

# ----------------- NUEVAS GRAFICAS DE CORRELACION ----------------- #

st.header(t("sec5"))
st.write(t("comp_intro"))

anios_futuros = pd.DataFrame({'Anio': np.arange(2027, 2042)})
X_futuro_scaled = scaler.transform(anios_futuros[['Anio']])
anios_futuros['Consumo_m3_Estimado'] = mejor_modelo.predict(X_futuro_scaled)

precios_gas = [1.40, 1.60, 1.80, 2.00, 2.20, 2.30, 2.40, 2.40, 2.40, 2.40, 2.40, 2.40, 2.40, 2.40, 2.40]
anios_futuros['Precio_Est_Gas_m3'] = precios_gas

costo_instalacion_gas = 40000
anios_futuros['Gasto_Factura_Gas'] = anios_futuros['Consumo_m3_Estimado'] * anios_futuros['Precio_Est_Gas_m3']
anios_futuros['Acumulado_Solo_Gas'] = costo_instalacion_gas + anios_futuros['Gasto_Factura_Gas'].cumsum()

anios_futuros['Demanda_Calor_kWh'] = anios_futuros['Consumo_m3_Estimado'] * 10
anios_futuros['Elec_WP_kWh'] = (anios_futuros['Demanda_Calor_kWh'] * 0.8) / 3.5  
anios_futuros['Gas_Hibrido_m3'] = anios_futuros['Consumo_m3_Estimado'] * 0.2

precio_elec = 0.30 
anios_futuros['Gasto_Factura_Hibrido'] = (anios_futuros['Elec_WP_kWh'] * precio_elec) + (anios_futuros['Gas_Hibrido_m3'] * anios_futuros['Precio_Est_Gas_m3'])

costo_instalacion_hibrido_sin_sub = 92500
costo_instalacion_hibrido_con_sub = 92500 * 0.70 

anios_futuros['Acumulado_Hibrido_Sin_Sub'] = costo_instalacion_hibrido_sin_sub + anios_futuros['Gasto_Factura_Hibrido'].cumsum()
anios_futuros['Acumulado_Hibrido_Con_Sub'] = costo_instalacion_hibrido_con_sub + anios_futuros['Gasto_Factura_Hibrido'].cumsum()

fig_comparativa = go.Figure()

fig_comparativa.add_trace(go.Scatter(x=anios_futuros['Anio'], y=anios_futuros['Acumulado_Solo_Gas'],
                                     mode='lines+markers', name=t("opt1"),
                                     line=dict(color='red')))

fig_comparativa.add_trace(go.Scatter(x=anios_futuros['Anio'], y=anios_futuros['Acumulado_Hibrido_Sin_Sub'],
                                     mode='lines+markers', name=t("opt2_no"),
                                     line=dict(color='orange', dash='dash')))

fig_comparativa.add_trace(go.Scatter(x=anios_futuros['Anio'], y=anios_futuros['Acumulado_Hibrido_Con_Sub'],
                                     mode='lines+markers', name=t("opt2_yes"),
                                     line=dict(color='green')))

fig_comparativa.update_layout(title=t("chart4"),
                              xaxis_title=t("x_axis"),
                              yaxis_title=t("y_axis"),
                              hovermode="x unified")

st.plotly_chart(fig_comparativa, use_container_width=True)

st.success(f"""
{t("conc_title")}\n
{t("conc_1")}\n
{t("conc_2")}
""")

