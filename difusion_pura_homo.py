import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Parámetros del problema
Ro = 2.0e-2  # Radio externo [m]
Ri = Ro - 3.0e-3  # Radio interno [m]
Cin = 0.1  # Concentración en r = Ri
Cout = 0.0  # Concentración en r = Ro
D = 1.0e-8  # Coeficiente de difusión [m²/s]

# Discretización
n = 100  # Número de puntos en r
r = np.linspace(Ri, Ro, n)

# Ecuación de difusión en coordenadas cilíndricas:
# ∂C/∂t = D * (∂²C/∂r² + (1/r)∂C/∂r)
def diffusion_cylindrical(C, r, D):
    """
    Implementa la ecuación de difusión en coordenadas cilíndricas
    dC/dt = D * (d²C/dr² + (1/r)dC/dr)
    """
    # Calculamos las derivadas
    dCdr = np.gradient(C, r)  # Primera derivada
    d2Cdr2 = np.gradient(dCdr, r)  # Segunda derivada
    
    # Término (1/r)∂C/∂r
    radial_term = dCdr / r
    
    return D * (d2Cdr2 + radial_term)

# Condición inicial
def initial_condition(r):
    """Condición inicial: distribución lineal entre Cin y Cout"""
    return Cout + (Cin - Cout) * (Ro - r)/(Ro - Ri)

# Tiempo de simulación
t = np.linspace(0, 5*3600, 1000)  # 5 horas en segundos

# Resolver la ecuación
C0 = initial_condition(r)
solution = odeint(lambda C, t: diffusion_cylindrical(C, r, D), C0, t)

# Graficar resultados
plt.figure(figsize=(10, 6))
times_to_plot = [0, int(len(t)/4), int(len(t)/2), int(3*len(t)/4), -1]
for i in times_to_plot:
    plt.plot(r*1000, solution[i], label=f't = {t[i]/3600:.1f} h')

plt.xlabel('Radio [mm]')
plt.ylabel('Concentración')
plt.title('Difusión en coordenadas cilíndricas')
plt.grid(True)
plt.legend()
plt.show()

# Graficar evolución temporal en diferentes posiciones radiales
plt.figure(figsize=(10, 6))
positions = [0, int(n/4), int(n/2), int(3*n/4), -1]
for i in positions:
    plt.plot(t/3600, solution[:, i], label=f'r = {r[i]*1000:.1f} mm')

plt.xlabel('Tiempo [h]')
plt.ylabel('Concentración')
plt.title('Evolución temporal de la concentración')
plt.grid(True)
plt.legend()
plt.show()

# Graficar el perfil de concentración en 3D
R, T = np.meshgrid(r*1000, t/3600)
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(R, T, solution, cmap='viridis')
ax.set_xlabel('Radio [mm]')
ax.set_ylabel('Tiempo [h]')
ax.set_zlabel('Concentración')
plt.colorbar(surf)
plt.title('Evolución espacio-temporal de la concentración')
plt.show()