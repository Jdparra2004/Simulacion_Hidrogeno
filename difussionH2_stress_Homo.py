#método de homotopia

import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

# Parámetros del problema
Ro = 2.0e-2
Ri = Ro - 3.0e-3
Cin = 0.1
Cout = 0.0
D = 1.0e-8
E = 10e9  # Pa
nu = 0.3
Omega = 5.0e-3
C0 = 0.0
pin = 400.0e3  # Pa
n = 2000  # nodes
dr = (Ro - Ri) / (n - 1)
S = 60 * 60  # seconds per hour
t_end = 5.0
nt = 1000
dt = t_end / (nt - 1)

r = np.linspace(Ri, Ro, n)
t = np.linspace(0, nt * dt, nt + 1)

# Función para el problema simple (difusión pura)
def simple_problem(C, C_old):
    dCdt = np.zeros_like(C)
    for i in range(1, n-1):
        dCdt[i] = D * (C[i+1] - 2*C[i] + C[i-1]) / dr**2
    return dCdt - (C - C_old) / dt

# Función para el problema complejo (difusión con esfuerzos)
def complex_problem(C, C_old, Disp):
    dCdt = np.zeros_like(C)
    for i in range(1, n-1):
        dCdt[i] = D * (C[i+1] - 2*C[i] + C[i-1]) / dr**2
    
    # Añadir el efecto de los esfuerzos (esto es una simplificación)
    stress_effect = Omega * np.gradient(np.gradient(Disp, r), r)
    
    return dCdt - (C - C_old) / dt + stress_effect

# Función de homotopía
def homotopy(X, C_old, p):
    C = X[:n]
    Disp = X[n:]
    
    H1 = (1-p) * simple_problem(C, C_old) + p * complex_problem(C, C_old, Disp)
    
    # Ecuación para el desplazamiento (simplificada)
    H2 = np.gradient(np.gradient(Disp, r), r) + Omega * np.gradient(C, r)
    
    return np.concatenate((H1, H2))

# Inicialización
C = np.zeros(n)
C[0] = Cin
C[-1] = Cout
Disp = np.zeros(n)

H = np.zeros((n, nt+1))
HDisp = np.zeros((n, nt+1))

# Bucle principal de homotopía
p_values = np.linspace(0, 1, 10)

for j in range(nt):
    C_old = C.copy()
    
    for p in p_values:
        # Resolver el sistema para el valor actual de p
        X = np.concatenate((C, Disp))
        X_new = fsolve(homotopy, X, args=(C_old, p))
        
        C = X_new[:n]
        Disp = X_new[n:]
    
    # Aplicar condiciones de contorno
    C[0] = Cin
    C[-1] = Cout
    Disp[0] = 0  # Suponiendo desplazamiento nulo en el radio interno
    
    # Almacenar resultados
    H[:, j+1] = C
    HDisp[:, j+1] = Disp

Cflux = np.zeros((n, nt+1))
for j in range(nt+1):
    for i in range(1, n-1):
        Cflux[i,j] = -2.0 * np.pi * r[i] * D * (H[i+1,j] - H[i-1,j]) / (2*dr)
    Cflux[0,j] = -2.0 * np.pi * r[0] * D * (-3*H[0,j] + 4*H[1,j] - H[2,j]) / (2*dr)
    Cflux[-1,j] = -2.0 * np.pi * r[-1] * D * (3*H[-1,j] - 4*H[-2,j] + H[-3,j]) / (2*dr)

# Cálculo de esfuerzos y deformaciones
sigma_r = np.zeros((n, nt+1))
sigma_t = np.zeros((n, nt+1))
epsilon_r = np.zeros((n, nt+1))
epsilon_t = np.zeros((n, nt+1))

for j in range(nt+1):
    epsilon_t[:,j] = HDisp[:,j] / r
    for i in range(n):
        if i > 0 and i < n-1:
            epsilon_r[i,j] = (HDisp[i+1,j] - HDisp[i-1,j]) / (2*dr)
        elif i == 0:
            epsilon_r[i,j] = (-3*HDisp[i,j] + 4*HDisp[i+1,j] - HDisp[i+2,j]) / (2*dr)
        else:
            epsilon_r[i,j] = (3*HDisp[i,j] - 4*HDisp[i-1,j] + HDisp[i-2,j]) / (2*dr)
        
        sigma_r[i,j] = (E/((1.+nu)*(2.*nu-1.))) * ((nu-1.)*epsilon_r[i,j] - nu*epsilon_t[i,j] + (1./3.)*Omega*H[i,j])
        sigma_t[i,j] = (E/((1.+nu)*(2.*nu-1.))) * ((nu-1.)*epsilon_t[i,j] - nu*epsilon_r[i,j] + (1./3.)*Omega*H[i,j])

# Gráficas

# 1. Concentración vs r para cada tiempo
plt.figure(figsize=(10, 6))
for i in range(0, nt+1, nt//5):
    plt.plot(r*1e3, H[:,i], label=f't={i*dt:.1f} hours')
plt.xlabel('r [mm]')
plt.ylabel('C')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.title('Concentración vs radio')
plt.tight_layout()
plt.show()

# 2. Concentración vs tiempo para cada radio
plt.figure(figsize=(10, 6))
for i in range(0, n, n//10):
    plt.plot(t, H[i,:], label=f'r={r[i]*1e3:.1f} mm')
plt.xlabel('t [hours]')
plt.ylabel('C')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.title('Concentración vs tiempo')
plt.tight_layout()
plt.show()

# 3. Flujo vs r para cada tiempo
plt.figure(figsize=(10, 6))
for i in range(0, nt+1, nt//5):
    plt.plot(r*1e3, Cflux[:,i], label=f't={i*dt:.1f} hours')
plt.xlabel('r [mm]')
plt.ylabel('Flux [m³/s]')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.title('Flujo vs radio')
plt.tight_layout()
plt.show()

# 4. Flujos en radio interno y externo vs tiempo
plt.figure(figsize=(10, 6))
plt.plot(t, Cflux[0,:], label='inner radius flow')
plt.plot(t, Cflux[-1,:], label='outer radius flow')
plt.xlabel('t [hours]')
plt.ylabel('Flux [m³/s]')
plt.legend(loc='upper right')
plt.title('Flujo vs tiempo en radios interno y externo')
plt.tight_layout()
plt.show()

# 5. Desplazamiento vs radio para cada tiempo
plt.figure(figsize=(10, 6))
for i in range(0, nt+1, nt//5):
    plt.plot(r*1e3, HDisp[:,i]*1e3, label=f't={i*dt:.1f} hours')
plt.xlabel('r [mm]')
plt.ylabel('u [mm]')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.title('Desplazamiento vs radio')
plt.tight_layout()
plt.show()

# 6. sigma_r vs radio para cada tiempo
plt.figure(figsize=(10, 6))
for i in range(0, nt+1, nt//5):
    plt.plot(r*1e3, sigma_r[:,i], label=f't={i*dt:.1f} hours')
plt.xlabel('r [mm]')
plt.ylabel('σ_r [Pa]')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.title('Esfuerzo radial vs radio')
plt.tight_layout()
plt.show()

# 7. sigma_t vs radio para cada tiempo
plt.figure(figsize=(10, 6))
for i in range(0, nt+1, nt//5):
    plt.plot(r*1e3, sigma_t[:,i], label=f't={i*dt:.1f} hours')
plt.xlabel('r [mm]')
plt.ylabel('σ_θ [Pa]')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.title('Esfuerzo tangencial vs radio')
plt.tight_layout()
plt.show()

# 8. epsilon_r vs radio para cada tiempo
plt.figure(figsize=(10, 6))
for i in range(0, nt+1, nt//5):
    plt.plot(r*1e3, epsilon_r[:,i], label=f't={i*dt:.1f} hours')
plt.xlabel('r [mm]')
plt.ylabel('ε_r')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.title('Deformación radial vs radio')
plt.tight_layout()
plt.show()

# 9. epsilon_t vs radio para cada tiempo
plt.figure(figsize=(10, 6))
for i in range(0, nt+1, nt//5):
    plt.plot(r*1e3, epsilon_t[:,i], label=f't={i*dt:.1f} hours')
plt.xlabel('r [mm]')
plt.ylabel('ε_θ')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.title('Deformación tangencial vs radio')
plt.tight_layout
plt.show()