import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

# Parámetros de la simulación
radio_tubo = 0.02  # Radio de la tubería en metros
longitud_tubo = 0.1  # Longitud de la tubería en metros
tiempo_total = 5.0  # Tiempo total de simulación en segundos
dt = 0.1  # Intervalo de tiempo para la animación

# Función de concentración de hidrógeno (puedes reemplazar con tu modelo)
def concentracion_hidrogeno(x, y, z, t):
    # Ejemplo de función de difusión simple, ajusta según tu modelo
    return np.exp(-((x**2 + y**2) / (2 * (0.02 + t * 0.001)))) * np.exp(-z / (0.02 + t * 0.1))

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

# Función de actualización para la animación
def actualizar(t):
    # Calcular concentración en función del tiempo para cada partícula
    concentraciones = concentracion_hidrogeno(x_particulas, y_particulas, z_particulas, t)
    colores = plt.cm.plasma(concentraciones)  # Usar un mapa de color para las partículas
    sc._facecolor3d = colores
    sc._edgecolor3d = colores
    ax.set_title(f"Simulación de Difusión de Hidrógeno en t = {t:.2f} s")

# Crear la animación
ani = animation.FuncAnimation(fig, actualizar, frames=np.arange(0, tiempo_total, dt), interval=100)

plt.colorbar(sc, label="Concentración de Hidrógeno [mol/m³]")
plt.show()
