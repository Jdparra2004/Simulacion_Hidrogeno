import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import time

# Parámetros del problema
Ro = 2.0e-2
Ri = Ro - 3.0e-3
Cin = 0.1
Cout = 0.0
D = 1.0e-8
n = 500  # Número de nodos
dr = (Ro - Ri) / (n - 1)
t_end = 5.0
nt = 500  # Número de pasos de tiempo
dt = t_end / (nt - 1)

r = np.linspace(Ri, Ro, n)
H = np.zeros((n, nt + 1))

# Función para el problema de difusión pura
def simple_problem(C, C_old):
    dCdt = np.zeros_like(C)
    for i in range(1, n - 1):
        dCdt[i] = D * (C[i + 1] - 2 * C[i] + C[i - 1]) / dr**2
    return dCdt - (C - C_old) / dt

# Inicialización de la concentración
C = np.zeros(n)
C[0] = Cin
C[-1] = Cout

# Iniciar el temporizador
start_time = time.time()

# Bucle principal de homotopía
for j in range(nt):
    C_old = C.copy()
    for p in np.linspace(0, 1, 10):
        X_new = fsolve(lambda X: simple_problem(X, C_old), C)
        C = X_new

    # Aplicar condiciones de contorno
    C[0] = Cin
    C[-1] = Cout
    H[:, j + 1] = C

# Calcular el tiempo total de ejecución
end_time = time.time()
execution_time = end_time - start_time
print(f"Tiempo de ejecución: {execution_time:.2f} segundos")

# Gráficas de resultados
plt.figure(figsize=(10, 6))
for i in range(0, nt + 1, nt // 5):
    plt.plot(r * 1e3, H[:, i], label=f't={i * dt:.2f} horas')
plt.xlabel('r [mm]')
plt.ylabel('C [mol/m³]')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.title('Concentración vs radio')
plt.tight_layout()
plt.show()
