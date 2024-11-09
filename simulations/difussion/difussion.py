import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
from simulations.difussion import (
    initialize_parameters,
    initialize_arrays,
    setup_diffusion_matrix,
    solve_diffusion,
    solve_disp,
    post_processing
)

# Inicializar parámetros desde el archivo de simulación
Ro, Ri, Cin, Cout, D, E, nu, Omega, C0, pin, n, dr, S, t_end, nt, dt = initialize_parameters()
Cold, C, Disp, sigma_r, sigma_t, epsi_r, epsi_t, A, ADisp, rhs, rhsDisp, r, t, H, Cflux, Hflux, HDisp, HStress_r, HStress_t, HStrain_r, HStrain_t = initialize_arrays(n, nt, C0, Ri, Ro)

# Configurar matriz de difusión y resolverla
A, ADisp = setup_diffusion_matrix(A, ADisp, n, dr, D, S, dt, r, nu)
solve_diffusion(A, rhs, Cold, dt, nt, Cin, Cout, dr, D, r, S, H, Cflux, n)

# Parámetros de la simulación de visualización
radio_tubo = 0.02  # Radio de la tubería en metros
longitud_tubo = 1.0  # Longitud de la tubería en metros
desplazamiento_max = 0.001  # Desplazamiento máximo por paso

# Configuración de la figura
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-longitud_tubo / 2, longitud_tubo / 2)
ax.set_ylim(-radio_tubo, radio_tubo)
ax.set_zlim(-radio_tubo, radio_tubo)
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
ax.set_zlabel("z [m]")

# Orientación horizontal de la tubería
ax.view_init(elev=0, azim=90)

# Generación inicial de partículas
num_particulas = 1000
x_particulas = np.random.uniform(-longitud_tubo / 2, longitud_tubo / 2, num_particulas)
y_particulas = np.random.uniform(-radio_tubo, radio_tubo, num_particulas)
z_particulas = np.random.uniform(-radio_tubo, radio_tubo, num_particulas)

# Filtrar partículas dentro del radio del tubo
mascara_tubo = (y_particulas**2 + z_particulas**2) <= radio_tubo**2
x_particulas = x_particulas[mascara_tubo]
y_particulas = y_particulas[mascara_tubo]
z_particulas = z_particulas[mascara_tubo]

# Crear dispersión de partículas
sc = ax.scatter(x_particulas, y_particulas, z_particulas, c='yellow', marker='o', alpha=0.6)

# Calcular el tiempo total de simulación en años
segundos_a_anos = 365 * 24 * 3600  # Conversión de segundos a años

# Función de actualización para la animación
def actualizar(frame):
    # Calcular el tiempo de simulación en años para este cuadro
    tiempo_simulacion_anos = frame * dt / segundos_a_anos

    # Obtener la concentración de hidrógeno en el tiempo correspondiente
    concentracion_actual = H[:, frame]  # Usamos la columna correspondiente en `H`

    # Movimiento aleatorio para simular difusión visual
    dx = np.random.uniform(-desplazamiento_max, desplazamiento_max, len(x_particulas))
    dy = np.random.uniform(-desplazamiento_max, desplazamiento_max, len(y_particulas))
    dz = np.random.uniform(-desplazamiento_max, desplazamiento_max, len(z_particulas))

    # Actualizar posiciones de partículas
    x_particulas[:] += dx
    y_particulas[:] += dy
    z_particulas[:] += dz

    # Mantener partículas dentro de la longitud del tubo
    x_particulas[:] = np.clip(x_particulas, -longitud_tubo / 2, longitud_tubo / 2)

    # Mantener partículas dentro del radio del tubo (en el plano yz)
    distancia_al_centro = np.sqrt(y_particulas**2 + z_particulas**2)
    mascara_fuera = distancia_al_centro > radio_tubo
    y_particulas[mascara_fuera] -= dy[mascara_fuera]  # Revertir movimiento fuera del radio
    z_particulas[mascara_fuera] -= dz[mascara_fuera]

    # Asignar colores a las partículas según la concentración
    colores = plt.cm.plasma(concentracion_actual)  # Mapear concentración a colores
    sc._offsets3d = (x_particulas, y_particulas, z_particulas)
    sc._facecolor3d = colores
    sc._edgecolor3d = colores

    # Actualizar el título con el tiempo simulado en años
    ax.set_title(f"Simulación de Difusión de Hidrógeno")

# Crear la animación
frames = nt  # Usamos el número de pasos de tiempo total
ani = animation.FuncAnimation(fig, actualizar, frames=frames, interval=100)

plt.colorbar(sc, label="Concentración de Hidrógeno [mol/m³]")
plt.show()
