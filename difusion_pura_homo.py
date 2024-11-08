import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Parámetros del problema
Ro = 2.0e-2  # Radio externo [m]
Ri = Ro - 3.0e-3  # Radio interno [m]
Cin = 0.1  # Concentración en el radio interno [mol/m³]
Cout = 0.0  # Concentración en el radio externo [mol/m³]
D = 1.0e-8  # Coeficiente de difusión [m²/s]
n = 2000  # Número de nodos
dr = (Ro - Ri) / (n - 1)  # Tamaño del paso radial
t_end = 5.0  # Tiempo total de simulación [horas]
nt = 1000  # Número de pasos de tiempo
dt = t_end / (nt - 1)  # Tamaño del paso de tiempo

# Definición de los vectores de espacio y tiempo
r = np.linspace(Ri, Ro, n)  # Vector radial
t = np.linspace(0, t_end, nt + 1)  # Vector de tiempo

# Función para el problema de difusión pura
def simple_problem(C, C_old):
    dCdt = np.zeros_like(C)  # Inicializa la tasa de cambio de concentración
    # Calcula la tasa de cambio en el interior del cilindro
    for i in range(1, n - 1):
        dCdt[i] = D * (C[i + 1] - 2 * C[i] + C[i - 1]) / dr**2
    # Retorna la diferencia entre la tasa de cambio y la diferencia temporal
    return dCdt - (C - C_old) / dt

# Función de homotopía (simplificada para difusión pura)
def homotopy(X, C_old, p):
    C = X[:n]  # Extrae la concentración del vector X
    H1 = simple_problem(C, C_old)  # Llama a la función de difusión pura
    return H1  # Retorna el resultado

# Inicialización de la concentración
C = np.zeros(n)  # Vector de concentración
C[0] = Cin  # Condición de contorno en el radio interno
C[-1] = Cout  # Condición de contorno en el radio externo

H = np.zeros((n, nt + 1))  # Matriz para almacenar resultados

# Bucle principal de homotopía
p_values = np.linspace(0, 1, 10)  # Valores de p para la homotopía

# Iteración sobre el tiempo
for j in range(nt):
    C_old = C.copy()  # Almacena la concentración anterior
    
    # Iteración sobre los valores de p
    for p in p_values:
        # Resuelve el sistema para el valor actual de p
        X = C.copy()  # Vector de concentración actual
        X_new = fsolve(homotopy, X, args=(C_old, p))  # Resuelve la ecuación
        C = X_new  # Actualiza la concentración
    
    # Aplicar condiciones de contorno
    C[0] = Cin  # Reestablece la concentración en el radio interno
    C[-1] = Cout  # Reestablece la concentración en el radio externo
    
    # Almacenar resultados
    H[:, j + 1] = C  # Guarda la concentración en la matriz de resultados

# Gráficas de resultados
plt.figure(figsize=(10, 6))
# Plotea la concentración vs radio para diferentes tiempos
for i in range(0, nt + 1, nt // 5):
    plt.plot(r * 1e3, H[:, i], label=f't={i * dt:.1f} hours')  # Convertir r a mm
plt.xlabel('r [mm]')  # Etiqueta del eje x
plt.ylabel('C [mol/m³]')  # Etiqueta del eje y
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Leyenda
plt.title('Concentración vs radio')  # Título del gráfico
plt.tight_layout()  # Ajustar el diseño
plt.show()  # Mostrar el gráfico