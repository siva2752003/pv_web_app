from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

# Physical constants
e = 1.602e-19  # Electron charge (C)
k = 1.38e-23   # Boltzmann constant (J/K)

# PV cell parameters
Iph = 5        # Photocurrent (A)
I0 = 0.0002    # Reverse saturation current (A)
Rs = 0.001     # Series resistance (Ohms)
Tc = 293.15    # Cell temperature (K)
A = 1.2        # Curve fitting factor

# Function to calculate cell voltage (V)
def calc_voltage(I_C, Iph, I0, Rs, A, Tc, e, k):
    return (A * k * Tc / e) * np.log((Iph + I0 - I_C) / I0) - I_C * Rs

# Function to compute PV and IV characteristics
def compute_pv_iv():
    I_C_range = np.linspace(0, Iph, 100)  # Range of output currents (A)
    V_C_array = np.zeros_like(I_C_range)
    P_array = np.zeros_like(I_C_range)

    # Compute voltage and power for each current
    for i, I_C in enumerate(I_C_range):
        V_C = calc_voltage(I_C, Iph, I0, Rs, A, Tc, e, k)
        V_C_array[i] = V_C
        P_array[i] = V_C * I_C

    return V_C_array, I_C_range, P_array

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    V_C_array, I_C_range, P_array = compute_pv_iv()
    return jsonify({
        'voltage': V_C_array.tolist(),
        'current': I_C_range.tolist(),
        'power': P_array.tolist()
    })

if __name__ == '__main__':
    app.run(debug=True)
