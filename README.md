# 🔥 Gas Consumption Predictor & Hybrid System ROI Calculator

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

Este proyecto es una aplicación interactiva desarrollada en **Streamlit** que utiliza **Machine Learning** para predecir el consumo futuro de gas natural de una vivienda. Además, realiza un análisis de viabilidad económica (*Break-Even Analysis*) para comparar los costes de mantener una instalación tradicional de gas frente a la transición hacia un sistema híbrido (Bomba de calor + Caldera de gas), tomando en cuenta los escenarios de incremento de impuestos al CO₂ (ETS-2) en Alemania.

## 🌟 Características Principales

1. **Internacionalización (i18n):** La aplicación soporta tres idiomas nativos (Español, Inglés y Alemán) seleccionables desde el menú lateral.
2. **Entrenamiento en Tiempo Real:** Utiliza el algoritmo `LinearRegression` de `scikit-learn` para aprender del histórico de lecturas del medidor (últimos 10 años) y proyectar el consumo a 5 años (con una proyección extendida a 15 años).
3. **Análisis del Peor Escenario:** Simula el impacto del mercado de emisiones europeo (ETS-2) a partir de 2027, mostrando cómo la inflación y los bonos de carbono afectarán la factura.
4. **Calculadora de Amortización (15 Años):** Compara los costes acumulados de instalación y consumo de dos opciones:
   * Instalación de gas 100%.
   * Sistema Híbrido (*Wärmepumpe* al 80% + Gas al 20%) con y sin subvenciones gubernamentales (ej. KfW).

## 🛠️ Tecnologías Utilizadas
* **Python 3**
* **Streamlit** (Interfaz web interactiva)
* **Pandas / NumPy** (Procesamiento y limpieza de datos)
* **Scikit-learn** (Modelo predictivo Random Forest)
* **Plotly** (Gráficos interactivos y visualización de datos)

## 🚀 Instalación y Ejecución Local

Sigue estos pasos si deseas ejecutar la aplicación en tu propio ordenador:

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
   cd TU_REPOSITORIO
   ```

2. **Crea un entorno virtual (recomendado):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # En Windows usa: .venv\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecuta la aplicación:**
   ```bash
   streamlit run app.py
   ```
   La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`.

## 📁 Estructura del Proyecto

```text
├── data/
│   └── export_zaehlerstandshistorie_891288_20261003.xlsx  # Histórico de lecturas de gas
├── app.py                 # Código principal de la aplicación Streamlit
├── requirements.txt       # Dependencias del proyecto
├── .gitignore             # Archivos excluidos del control de versiones
└── README.md              # Documentación del proyecto
```

## 🌍 Despliegue en Streamlit Community Cloud
Este repositorio está listo para ser desplegado de forma gratuita en [Streamlit Community Cloud](https://streamlit.io/cloud). Solo necesitas vincular este repositorio de GitHub con tu cuenta de Streamlit y apuntar al archivo `app.py`.
