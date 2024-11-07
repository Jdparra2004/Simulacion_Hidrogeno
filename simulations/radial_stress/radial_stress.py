import numpy as np

def calculate_radial_stress(L, T, D, nx, nt):
    # Constantes del problema
    dx = L / (nx - 1)  # Tamaño del paso en el espacio
    dt = T / (nt - 1)  # Tamaño del paso en el tiempo

    # Condición inicial
    u = np.zeros(nx)
    u[int(0.5 / dx):int(1 / dx + 1)] = 1

    # Coeficiente de estabilidad
    alpha = D * dt / dx**2
    if alpha > 0.5:
        print("Advertencia: El coeficiente de estabilidad es mayor a 0.5")

    # Solución numérica usando el método de diferencias finitas
    for n in range(1, nt):
        un = u.copy()
        for i in range(1, nx - 1):
            u[i] = un[i] + alpha * (un[i + 1] - 2 * un[i] + un[i - 1])

    return np.linspace(0, L, nx), u
