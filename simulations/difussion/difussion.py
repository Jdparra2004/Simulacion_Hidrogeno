# simulations/difussion/difussion.py

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# En diffusion.py
from simulations.difussion import (
    Ro, Ri, Cin, Cout, D, E, nu, Omega, C0, pin, n, dr, S, t_end, nt, dt,
    H, r, Cflux
)

def simulate_diffusion():
    # Definir la malla 3D para la tubería P80
    z = np.linspace(0, 1, 50)  # Longitud de la tubería (reducido)
    theta = np.linspace(0, 2 * np.pi, 50)  # Ángulo (reducido)
    r = np.linspace(Ri, Ro, 50)  # Radio (reducido)

    # Crear una cuadrícula 3D
    R, Z = np.meshgrid(r, z)
    Theta = np.meshgrid(theta)

    # Convertir a coordenadas cartesianas
    X = R * np.cos(Theta[0])  # Coordenada X
    Y = R * np.sin(Theta[0])  # Coordenada Y

    # Crear la figura para la visualización
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Seleccionar un paso de tiempo específico para la visualización
    frame = nt // 2  # Por ejemplo, el paso de tiempo en el medio

    # Obtener la concentración de hidrógeno en el tiempo actual
    C = H[:, frame]  # Usar los resultados de la simulación

    # Asegurarse de que C tenga la forma correcta
    C_expanded = np.repeat(C[:, np.newaxis], Z.shape[0], axis=1)  # Expandir C a la forma de Z

    # Normalizar C
    if np.max(C_expanded) > 0:
        normalized_C = C_expanded / np.max(C_expanded)
    else:
        normalized_C = np.zeros_like(C_expanded)  # Manejar el caso donde todos los valores son cero

    # Graficar la superficie
    surf = ax.plot_surface(X, Y, Z, facecolors=plt.cm.viridis(normalized_C), rstride=1, cstride=1, antialiased=True)

    ax.set_xlabel('X [m]')
    ax.set_ylabel('Y [m]')
    ax.set_zlabel('Z [m]')
    ax.set_title(f'Difusión de Hidrógeno en la Tubería P80 en t={frame * dt:.2f} s')
    plt.colorbar(surf, label='Concentración de Hidrógeno [mol/m³]')
    plt.show()

if __name__ == "__main__":
    simulate_diffusion()