
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Heat Exchanger Profile", layout="centered")
st.title("📈 Heat Exchanger Temperature Profile and Performance Calculator")

# Temperature inputs
T_h_in = st.number_input("Hot fluid inlet temperature (°C)", value=100.0)
T_h_out = st.number_input("Hot fluid outlet temperature (°C)", value=60.0)
T_c_in = st.number_input("Cold fluid inlet temperature (°C)", value=30.0)
T_c_out = st.number_input("Cold fluid outlet temperature (°C)", value=50.0)
L = st.number_input("Heat exchanger length (m)", value=5.0)
flow_type = st.selectbox("Flow Type", ["Counterflow", "Parallel flow"])

# Temperature profile plotting
n = 50
x = np.linspace(0, L, n)

if flow_type == "Counterflow":
    T_hot = np.linspace(T_h_in, T_h_out, n)
    T_cold = np.linspace(T_c_out, T_c_in, n)
else:
    T_hot = np.linspace(T_h_in, T_h_out, n)
    T_cold = np.linspace(T_c_in, T_c_out, n)

fig, ax = plt.subplots()
ax.plot(x, T_hot, label='Hot Fluid Temperature', color='red', marker='o')
ax.plot(x, T_cold, label='Cold Fluid Temperature', color='blue', marker='o')
ax.set_xlabel("Length of Heat Exchanger (m)")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Temperature Profile Along Heat Exchanger")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Additional inputs for calculations
st.markdown("### Additional Parameters for Performance Calculation")
m_h = st.number_input("Mass flow rate of hot fluid (kg/s)", value=1.0)
m_c = st.number_input("Mass flow rate of cold fluid (kg/s)", value=1.0)
cp_h = st.number_input("Specific heat of hot fluid (kJ/kg·K)", value=4.18)
cp_c = st.number_input("Specific heat of cold fluid (kJ/kg·K)", value=4.18)
A = st.number_input("Heat exchanger surface area (m2)", value=5.0)

# Calculations
C_h = m_h * cp_h
C_c = m_c * cp_c
C_min = min(C_h, C_c)
C_max = max(C_h, C_c)

Q_hot = m_h * cp_h * (T_h_in - T_h_out)
Q_cold = m_c * cp_c * (T_c_out - T_c_in)
Q = min(Q_hot, Q_cold)

Q_max = C_min * (T_h_in - T_c_in)
effectiveness = Q / Q_max if Q_max != 0 else 0

delta_T1 = T_h_in - T_c_out
delta_T2 = T_h_out - T_c_in

if delta_T1 != delta_T2 and delta_T1 > 0 and delta_T2 > 0:
    LMTD = (delta_T1 - delta_T2) / np.log(delta_T1 / delta_T2)
else:
    LMTD = (delta_T1 + delta_T2) / 2

U = Q / (A * LMTD) if (A * LMTD) != 0 else 0
NTU = (U * A) / C_min if C_min != 0 else 0

# Display results
st.subheader("📊 Heat Exchanger Calculated Results")
st.write(f"🔹 Heat Transfer Rate (Q): {Q:.2f} kW")
st.write(f"🔹 Effectiveness: {effectiveness:.3f}")
st.write(f"🔹 Log Mean Temperature Difference (LMTD): {LMTD:.2f} °C")
st.write(f"🔹 Overall Heat Transfer Coefficient (U): {U:.2f} kW/m²°C")
st.write(f"🔹 Number of Transfer Units (NTU): {NTU:.2f}")
