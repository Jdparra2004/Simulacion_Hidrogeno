import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_3d_image(data, type='concentration'):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Dependiendo del tipo, generamos diferentes visualizaciones
    if type == 'concentration':
        # Código para generar imagen 3D de concentración
        pass
    elif type == 'radial_stress':
        # Código para generar imagen 3D de estrés radial
        pass
    elif type == 'tangential_stress':
        # Código para generar imagen 3D de estrés tangencial
        pass
    
    # Guardamos la figura en un archivo
    plt.savefig(f'3d_{type}.png')
    plt.close(fig)
    
    return f'3d_{type}.png'