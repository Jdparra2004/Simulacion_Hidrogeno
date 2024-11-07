# Importamos las bibliotecas necesarias
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Definimos los parámetros del problema
Ro = 2.0e-2  # Radio externo [m]
Ri = Ro - 3.0e-3  # Radio interno [m]
Cin = 0.1  # Concentración en r = Ri (condición de contorno interna)
Cout = 0.0  # Concentración en r = Ro (condición de contorno externa)
D = 1.0e-8  # Coeficiente de difusión [m²/s]

# Configuramos la discretización espacial
n = 100  # Número de puntos en la dirección radial
r = np.linspace(Ri, Ro, n)  # Crea un array de n puntos equidistantes entre Ri y Ro

# Definimos la ecuación de difusión en coordenadas cilíndricas
def diffusion_cylindrical(C, r, D):
    """
    Implementa la ecuación de difusión en coordenadas cilíndricas
    dC/dt = D * (d²C/dr² + (1/r)dC/dr)
    """
    # Calculamos las derivadas espaciales
    dCdr = np.gradient(C, r)  # Primera derivada respecto a r
    d2Cdr2 = np.gradient(dCdr, r)  # Segunda derivada respecto a r
    
    # Calculamos el término radial (1/r)∂C/∂r
    radial_term = dCdr / r
    
    # Retornamos la expresión completa de la ecuación de difusión
    return D * (d2Cdr2 + radial_term)

# Definimos la condición inicial
def initial_condition(r):
    """Condición inicial: distribución lineal entre Cin y Cout"""
    return Cout + (Cin - Cout) * (Ro - r)/(Ro - Ri)

# Configuramos el tiempo de simulación
t = np.linspace(0, 5*3600, 1000)  # 5 horas en segundos, 1000 puntos

# Resolvemos la ecuación diferencial
C0 = initial_condition(r)  # Condición inicial
# odeint resuelve la ecuación diferencial. Le pasamos la función, la condición inicial y los tiempos
solution = odeint(lambda C, t: diffusion_cylindrical(C, r, D), C0, t)

# Graficamos los resultados
plt.figure(figsize=(10, 6))
times_to_plot = [0, int(len(t)/4), int(len(t)/2), int(3*len(t)/4), -1]  # Seleccionamos tiempos para graficar
for i in times_to_plot:
    plt.plot(r*1000, solution[i], label=f't = {t[i]/3600:.1f} h')

plt.xlabel('Radio [mm]')
plt.ylabel('Concentración')
plt.title('Difusión en coordenadas cilíndricas')
plt.grid(True)
plt.legend()
plt.show()

# Graficamos la evolución temporal en diferentes posiciones radiales
plt.figure(figsize=(10, 6))
positions = [0, int(n/4), int(n/2), int(3*n/4), -1]  # Seleccionamos posiciones radiales para graficar
for i in positions:
    plt.plot(t/3600, solution[:, i], label=f'r = {r[i]*1000:.1f} mm')

plt.xlabel('Tiempo [h]')
plt.ylabel('Concentración')
plt.title('Evolución temporal de la concentración')
plt.grid(True)
plt.legend()
plt.show()

# Graficamos el perfil de concentración en 3D
R, T = np.meshgrid(r*1000, t/3600)  # Creamos una malla 2D para r y t
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')  # Creamos un subplot 3D
surf = ax.plot_surface(R, T, solution, cmap='viridis')  # Graficamos la superficie
ax.set_xlabel('Radio [mm]')
ax.set_ylabel('Tiempo [h]')
ax.set_zlabel('Concentración')
plt.colorbar(surf)  # Añadimos una barra de color
plt.title('Evolución espacio-temporal de la concentración')
plt.show()