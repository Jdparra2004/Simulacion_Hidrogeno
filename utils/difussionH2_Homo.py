import numpy as np
import matplotlib.pyplot as plt

# Parámetros del problema
Ro = 2.0e-2  # Radio exterior en metros
Ri = Ro - 3.0e-3  # Radio interior en metros
D = 1.0e-8  # Coeficiente de difusión del hidrógeno en m^2/s (ajustado)
Cin = 0.0  # Concentración inicial en la región interior (ajustado)
Cout = 0.0  # Concentración en la región exterior
n = 100  # Número de nodos
r = np.linspace(Ri, Ro, n)  # Coordenadas radiales
t_end = 5 * 365 * 24 * 3600  # Tiempo total en segundos (5 años)
nt = 1000  # Número de pasos de tiempo
dt = t_end / nt  # Tamaño del paso de tiempo

# Inicialización de variables
C = np.zeros(n)  # Concentración
H = np.zeros((n, nt + 1))  # Historia de concentración
H[:, 0] = Cin  # Condición inicial

# Parámetro de homotopía
alpha = 0.0  # Comenzar desde 0 para evitar oscilaciones
alpha_step = 0.01  # Paso para aumentar alpha (ajustado)
max_iterations = 300  # Número máximo de iteraciones para la convergencia (ajustado)

# Iteración del método de Homotopía
for j in range(nt):
    # Inicializar la concentración para la iteración actual
    C_new = np.copy(H[:, j])
    
    # Bucle para resolver la ecuación de difusión
    for k in range(max_iterations):  # Número máximo de iteraciones para la convergencia
        C_old = np.copy(C_new)
        
        # Ecuación de difusión en coordenadas radiales (simplificada)
        for i in range(1, n - 1):
            if r[i] > 0:  # Evitar división por cero
                C_new[i] = C_old[i] + (D * dt / (r[i]**2)) * (C_old[i + 1] - 2 * C_old[i] + C_old[i - 1])
        
        # Condiciones de frontera
        C_new[0] = Cin  # Concentración en el borde interno
        C_new[-1] = Cout  # Concentración en el borde externo
        
        # Aplicar el método de Homotopía
        C_new = (1 - alpha) * C_old + alpha * C_new
        
        # Chequeo de convergencia (simple)
        if np.linalg.norm(C_new - C_old) < 1e-6:
            break
    
    # Guardar resultados
    H[:, j + 1] = C_new
    
    # Incrementar alpha para la siguiente iteración
    alpha = min(1.0, alpha + alpha_step)  # Asegurarse de que alpha no supere 1

# Gráficas de resultados
plt.figure()
for i in range(0, nt + 1, 100):  # Graficar cada 100 pasos
    plt.plot(r * 1e3, H[:, i], label=f't={i * dt / (365 * 24 * 3600):.1f} años')  # Convertir tiempo a años
plt.xlabel('r [mm]')
plt.ylabel('Concentración de Hidrógeno [mol/m^3]')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.title('Concentración de Hidrógeno vs Radio usando Método de Homotopía')
plt.grid()
plt.tight_layout()  # Ajustar el layout para evitar solapamientos
plt.show()