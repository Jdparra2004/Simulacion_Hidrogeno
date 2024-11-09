# simulations/difussion/difussion.py

import numpy as np
import matplotlib.pyplot as plt

# En diffusion.py
from simulations.difussion import (
    Ro, Ri, Cin, Cout, D, E, nu, Omega, C0, pin, n, dr, S, t_end, nt, dt,
    H, r, Cflux
)

def simulate_diffusion():
    # Reducir la resolución para evitar sobrecarga
    n_reduced = n // 10  # Reducir el número de nodos
    r_reduced = np.linspace(Ri, Ro, n_reduced)  # Radio reducido
    z = np.linspace(0, 1, 100)  # Longitud de la tubería
    time_steps_to_plot = range(0, nt + 1, 20)  # Graficar cada 20 pasos de tiempo

    # Crear una cuadrícula 2D para la visualización
    R, Z = np.meshgrid(r_reduced, z)

    # Simulación de la difusión
    for time_step in time_steps_to_plot:
        # Obtener la concentración de hidrógeno en el tiempo actual
        C = H[:, time_step]  # Usar los resultados de la simulación

        # Asegurarse de que C tenga la forma correcta
        if C.size != R.size:
            C = np.repeat(C[:, np.newaxis], Z.shape[0], axis=1)  # Expandir C a la forma de Z

        # Normalizar C
        if np.max(C) > 0:
            normalized_C = C / np.max(C)
        else:
            normalized_C = np.zeros_like(C)  # Manejar el caso donde todos los valores son cero

        # Visualizar la concentración en 2D
        plt.figure()
        plt.imshow(normalized_C, extent=[Ri, Ro, 0, 1], aspect='auto', origin='lower', cmap='viridis')
        plt.colorbar(label='Concentración de Hidrógeno [mol/m³]')
        plt.xlabel('Radio [m]')
        plt.ylabel('Longitud [m]')
        plt.title(f'Difusión de Hidrógeno en la Tubería P80 en t={time_step * dt:.2f} s')
        plt.show()

if __name__ == "__main__":
    simulate_diffusion()