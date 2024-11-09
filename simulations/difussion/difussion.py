# simulations/difussion/difussion.py

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Importar los resultados de los cálculos desde el módulo difussion
from simulations.difussion import (
    Ro, Ri, Cin, Cout, D, E, nu, Omega, C0, pin, n, dr, S, t_end, nt, dt,
    H, r, Cflux
)

def simulate_diffusion():
    # Definir la malla 3D para la tubería P80
    z = np.linspace(0, 1, n)  # Longitud de la tubería
    theta = np.linspace(0, 2 * np.pi, n)  # Ángulo
    r = np.linspace(Ri, Ro, n)  # Radio

    # Crear una cuadrícula 3D
    R, Z = np.meshgrid(r, z)
    Theta = np.meshgrid(theta)

    # Convertir a coordenadas cartesianas
    X = R * np.cos(Theta)
    Y = R * np.sin(Theta)

    # Simulación de la difusión
    for time_step in range(nt + 1):
        # Obtener la concentración de hidrógeno en el tiempo actual
        C = H[:, time_step]  # Usar los resultados de la simulación

        # Visualizar la concentración en el espacio 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(X, Y, Z, facecolors=plt.cm.viridis(C / np.max(C)), rstride=1, cstride=1, antialiased=True)

        ax.set_xlabel('X [m]')
        ax.set_ylabel('Y [m]')
        ax.set_zlabel('Z [m]')
        ax.set_title(f'Difusión de Hidrógeno en la Tubería P80 en t={time_step * dt:.2f} s')
        plt.colorbar(surf, label='Concentración de Hidrógeno [mol/m³]')
        plt.show()

if __name__ == "__main__":
    simulate_diffusion()