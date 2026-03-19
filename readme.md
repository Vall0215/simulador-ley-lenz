🧲 Simulador Interactivo de la Ley de Lenz

Este proyecto consiste en una aplicación web desarrollada con Streamlit que permite visualizar de forma interactiva el comportamiento de la Ley de Lenz en sistemas electromagnéticos.
El simulador modela una bobina sometida a variaciones de campo magnético, permitiendo analizar cómo los cambios en el flujo magnético generan una fuerza electromotriz inducida (FEM).

⚙️ Funcionalidades:
- Simulación de un imán en movimiento (campo ∝ 1/d³)
- Simulación de un campo magnético senoidal
- Visualización en tiempo real de:
- Flujo magnético Φ(t)
- Fuerza electromotriz inducida (fem)
- Comparación de fase entre B(t) y fem(t)
- Parámetros interactivos:
- Número de espiras (N)
- Área de la bobina
- Ángulo θ
- Frecuencia y amplitud
- Exportación de datos en formato CSV

🧠 Conceptos físicos aplicados:
- Ley de Faraday:
- Ley de Lenz (signo negativo → oposición al cambio)
- Relación entre flujo magnético, campo y geometría de la bobina

🚀 Tecnologías utilizadas:
- Python
- Streamlit
- NumPy
- Pandas
- Matplotlib

▶️ Ejecución local

pip install -r requirements.txt

streamlit run app_lenz.py
