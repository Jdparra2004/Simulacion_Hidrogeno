import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Parámetros del cilindro
radius = 1
length = 5
num_particles = 100
time_steps = 100

# Generar partículas aleatorias dentro del cilindro
theta = np.random.uniform(0, 2 * np.pi, num_particles)
z = np.random.uniform(-radius, radius, num_particles)
r = np.sqrt(radius**2 - z**2)
x = np.random.uniform(0, length, num_particles)
y = r * np.sin(theta)

# Velocidades aleatorias de las partículas
vx = np.random.uniform(-0.1, 0.1, num_particles)
vy = np.random.uniform(-0.1, 0.1, num_particles)
vz = np.random.uniform(-0.1, 0.1, num_particles)

# Crear la figura y los ejes 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Dibujar el cilindro
theta_cylinder = np.linspace(0, 2 * np.pi, 100)
z_cylinder = np.linspace(-radius, radius, 100)
theta_cylinder, z_cylinder = np.meshgrid(theta_cylinder, z_cylinder)
x_cylinder = length * np.ones_like(z_cylinder)
y_cylinder = radius * np.sin(theta_cylinder)
z_cylinder = z_cylinder

# Superficies de los extremos del cilindro
x_end1 = np.zeros_like(theta_cylinder)
x_end2 = length * np.ones_like(theta_cylinder)
y_end = radius * np.sin(theta_cylinder)
z_end = radius * np.cos(theta_cylinder)

# Función de actualización para la animación
def update(num):
    global x, y, z, vx, vy, vz
    
    # Actualizar posiciones
    x += vx
    y += vy
    z += vz
    
    # Reflejar partículas en las paredes del cilindro
    x = np.where(x > length, length, x)
    x = np.where(x < 0, 0, x)
    y = np.where(y > radius, radius, y)
    y = np.where(y < -radius, -radius, y)
    z = np.where(z > radius, radius, z)
    z = np.where(z < -radius, -radius, z)
    
    # Limpiar el eje
    ax.cla()
    
    # Dibujar la superficie del cilindro (superior e inferior)
    ax.plot_surface(z_cylinder, y_cylinder, x_cylinder, alpha=0.3, color='blue')
    ax.plot_surface(z_cylinder, -y_cylinder, x_cylinder, alpha=0.3, color='blue')
    
    # Dibujar los extremos del cilindro
    ax.plot_surface(z_end, y_end, x_end1, alpha=0.3, color='blue')
    ax.plot_surface(z_end, y_end, x_end2, alpha=0.3, color='blue')
    
    # Dibujar partículas de gas
    ax.scatter(z, y, x, color='red')
    
    # Configuración de los ejes
    ax.set_xlim([-radius, radius])
    ax.set_ylim([-radius, radius])
    ax.set_zlim([0, length])
    ax.set_xlabel('Z')
    ax.set_ylabel('Y')
    ax.set_zlabel('X')
    ax.set_title('Simulación de Cilindro Horizontal con Gas en Movimiento')

# Crear la animación
ani = FuncAnimation(fig, update, frames=time_steps, interval=50)

plt.show()
