import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

with open('notebook_gas.ipynb', 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
try:
    ep.preprocess(nb, {'metadata': {'path': './'}})
    with open('notebook_gas.ipynb', 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Notebook ejecutado y guardado.")
except Exception as e:
    print(f"Error ejecutando notebook: {e}")
