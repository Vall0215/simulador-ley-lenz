import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from io import StringIO

st.set_page_config(page_title="Ley de Lenz", layout="centered")

st.markdown("""
    <style>
    /* Aplicar Times New Roman globalmente */
    html, body, [class*="css"], div, span, p, label, input, textarea, select, button {
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 17px !important;
    }

    /* Títulos principales */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Times New Roman', Times, serif !important;
        font-weight: bold !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"], .stSlider, .stRadio, .stSelectbox, .stNumberInput {
        font-family: 'Times New Roman', Times, serif !important;
    }

    /* Botón de descarga */
    div.stDownloadButton > button:first-child {
        font-family: 'Times New Roman', Times, serif !important;
    }

    /* Caja de información (st.info) */
    .stAlert {
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 16px !important;
    }

    /* Métricas (cajas de valores) */
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
        font-family: 'Times New Roman', Times, serif !important;
    }

    /* Alinear el texto principal */
    .block-container {
        font-family: 'Times New Roman', Times, serif !important;
        line-height: 1.4em;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧲 Simulador interactivo")
st.markdown(
"""
Esta app modela una bobina que **siente** un imán que se mueve:

   ·  Distancia variable → Flujo variable → Fem inducida.  

Puedes cambiar nº de espiras, área, velocidad del imán, frecuencia y ver la señal de fem(t). La Ley de Lenz aparece 
con el signo negativo, mostrando la oposición al cambio.:

1) **Imán móvil:** el campo en la bobina cambia por la distancia imán–bobina.

2) **Campo senoidal:** el campo cambia en el tiempo.

"""
)

# ----------- Opciones iteracctivas usuario ------------
st.sidebar.header("Parámetros de la bobina")
N = st.sidebar.slider("Número de espiras N", 10, 2000, 200, step=10)
A_cm2 = st.sidebar.slider("Área de la espira (cm²)", 1.0, 50.0, 10.0, step=0.5)
A = A_cm2 * 1e-4  # cm² → m²
theta_deg = st.sidebar.slider("Ángulo θ (°)", 0, 90, 0, step=5)
theta = np.deg2rad(theta_deg)

st.sidebar.header("Tiempo de simulación")
T = st.sidebar.slider("Duración (s)", 0.5, 5.0, 2.0, step=0.5)
fs = 3000  # Hz
t = np.linspace(0, T, int(T*fs), endpoint=False)

# -------------- Botones de modos ------------
modo = st.radio(
    "Elige el modo de simulación",
    ["Imán móvil (B∝1/d³)", "Campo senoidal (B=B0·sin)"],
    index=0
)

# ------------ Cálculo de B(t) y condiciones ------------
if modo == "Imán móvil (B∝1/d³)":
    st.sidebar.subheader("Movimiento del imán")
    d0_mm = st.sidebar.slider("Distancia media d₀ (mm)", 5.0, 60.0, 20.0, step=1.0)
    amp_mm = st.sidebar.slider("Amplitud de oscilación (mm)", 0.0, 15.0, 5.0, step=0.5)
    freq = st.sidebar.slider("Frecuencia (Hz)", 0.1, 10.0, 2.0, step=0.1)
    k_B = st.sidebar.slider("k (intensidad relativa del imán)", 1e-7, 1e-5, 2e-6, step=1e-7, format="%.1e")

    d0 = d0_mm * 1e-3
    amp = amp_mm * 1e-3
    d = d0 + amp * np.sin(2*np.pi*freq*t)
    eps = 1e-6
    B = k_B / np.maximum(d, eps)**3

else:
    st.sidebar.subheader("Campo senoidal")
    B0 = st.sidebar.slider("Amplitud B₀ (tesla)", 0.001, 1.0, 0.1, step=0.001)
    freq = st.sidebar.slider("Frecuencia (Hz)", 0.1, 200.0, 60.0, step=0.1)
    B = B0 * np.sin(2*np.pi*freq*t)

# ------------Flujo y fuerza electromotriz inducida ------------
phi = N * B * A * np.cos(theta)          
fem = -np.gradient(phi, t)                

# ------------Escalas amigables ------------
def unit_scale(x, base_unit, thresholds=(1e-2, 1e-6), scaled=("m", "µ")):
    
    maximum = np.max(np.abs(x)) + 1e-30
    if base_unit == "V":
        if maximum < thresholds[0]:
            return scaled[0] + base_unit, 1e3   
    if base_unit == "Wb":
        if maximum < thresholds[1]:
            return scaled[1] + base_unit, 1e6   
    return base_unit, 1.0

fem_unit, fem_scale = unit_scale(fem, "V", thresholds=(1e-2, 0))
phi_unit, phi_scale = unit_scale(phi, "Wb", thresholds=(0, 1e-6))

# ------------ Métricas ------------
c1, c2, c3 = st.columns(3)
c1.metric("N (espiras)", f"{N}")
c2.metric("f (Hz)", f"{freq:.2f}")
c3.metric("θ (°)", f"{theta_deg}")

# ------------ Gráficas ------------
COLOR_FLUJO = "#2196F3"  
COLOR_FEM = "#E91E63"      

mostrar_fase = st.checkbox("Mostrar B(t) y fem(t) juntos (fase/derivada)", value=True)

if mostrar_fase:
    fig = plt.figure(figsize=(7,3))
    plt.plot(t, B, label="B(t) [T]", color=COLOR_FLUJO, linewidth=2)
    plt.plot(t, fem*fem_scale, label=f"fem(t) [{fem_unit}]", color=COLOR_FEM, linewidth=2, alpha=0.85)
    plt.xlabel("t (s)", color="#333")
    plt.ylabel("Magnitud", color="#333")
    plt.title("B(t) y fem(t)", color="#1A237E", fontsize=14, fontweight="bold")
    plt.grid(True)
    plt.legend()
    st.pyplot(fig, clear_figure=True)

st.subheader("Flujo magnético Φ(t)")
fig1 = plt.figure(figsize=(7,3))
plt.plot(t, phi*phi_scale, color=COLOR_FLUJO, linewidth=2)
plt.xlabel("t (s)", color="#333")
plt.ylabel(f"Φ(t) [{phi_unit}]", color="#333")
plt.title("Flujo magnético Φ(t)", color="#1A237E", fontsize=14, fontweight="bold")
plt.grid(True)
st.pyplot(fig1, clear_figure=True)

st.subheader("FEM inducida (Ley de Lenz)")
fig2 = plt.figure(figsize=(7,3))
plt.plot(t, fem*fem_scale, color=COLOR_FEM, linewidth=2)
plt.xlabel("t (s)", color="#333")
plt.ylabel(f"fem(t) [{fem_unit}]", color="#333")
plt.title("FEM inducida (Ley de Lenz)", color="#1A237E", fontsize=14, fontweight="bold")
plt.grid(True)
st.pyplot(fig2, clear_figure=True)

# ------------- Observaciones ------------

st.info(
    f"""
**Observaciones rápidas**
- ↑ **N** o **A** ⇒ ↑ |Φ| y ↑ |fem|.
- ↑ **frecuencia** o **amplitud de movimiento** ⇒ ↑ |dΦ/dt| ⇒ **mayor fem**.
- El signo **–** indica oposición al cambio (Ley de **Lenz**).
"""
)

# ------------ Descarga de datos CSV ------------
df = pd.DataFrame({
    "t_s": t,
    "B_T": B,
    "Phi_Wb": phi,
    "fem_V": fem
})
csv_buf = StringIO()
df.to_csv(csv_buf, index=False)
st.download_button(
    label="⬇️ Descargar los datos (CSV)",
    data=csv_buf.getvalue(),
    file_name="lenz_simulacion.csv",
    mime="text/csv"
)