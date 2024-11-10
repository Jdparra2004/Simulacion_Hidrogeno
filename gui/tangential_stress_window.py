# librerías gui
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from PyQt5 import uic
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from utils.difussionH2_stress_DF import (
    initialize_parameters,
    initialize_arrays,
    setup_diffusion_matrix,
    solve_diffusion,
    solve_disp,
    post_processing
)

class TangentialStressWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        uic.loadUi('resources/tangential_stress_window.ui', self)
        self.main_window = main_window
        
        # Asumir que WTangencial ya está definido en el archivo .ui
        self.graphWidget = self.WTangencial  # Conectar directamente al QWidget llamado WTangencial
        self.layout = QVBoxLayout(self.graphWidget)  # Crear un layout vertical para el widget

        # Inicializar el canvas
        self.canvas = None

        # Conectar botones con métodos
        self.buttonRunSimulation.clicked.connect(self.RunSimulation)
        self.returnToMenu.clicked.connect(self.VolverMenu)

    def RunSimulation(self):
        # Inicializar parámetros y arreglos
        Ro, Ri, Cin, Cout, D, E, nu, Omega, C0, pin, n, dr, S, t_end, nt, dt = initialize_parameters()
        Cold, C, Disp, sigma_r, sigma_t, epsi_r, epsi_t, A, ADisp, rhs, rhsDisp, r, t, H, Cflux, Hflux, HDisp, HStress_r, HStress_t, HStrain_r, HStrain_t = initialize_arrays(n, nt, C0, Ri, Ro)
        
        # Configurar la matriz de difusión
        A, ADisp = setup_diffusion_matrix(A, ADisp, n, dr, D, S, dt, r, nu)

        # Resolver la difusión
        solve_diffusion(A, rhs, Cold, dt, nt, Cin, Cout, dr, D, r, S, H, Cflux, n)

        # Resolver el desplazamiento
        solve_disp(ADisp, rhsDisp, Disp, H, HDisp, n, nt, dt, dr, Omega, pin, E, nu)

        # Procesamiento posterior para obtener los resultados necesarios
        post_processing(n, nt, r, H, Cflux, Disp, HDisp, HStress_r, HStress_t, HStrain_r, HStrain_t, dt)

        # Crear el gráfico de estrés tangencial
        self.plot_stress_graph(r, HStress_t, nt, dt)  # Llama a la función para graficar

    def plot_stress_graph(self, r, HStress_t, nt, dt):
        # Limpiar el layout antes de agregar nuevos gráficos
        for i in reversed(range(self.layout.count())): 
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # Eliminar el widget anterior

        # Crear un nuevo canvas para el gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Graficar el estrés tangencial para diferentes tiempos
        for i in range(0, nt + 1, 100):  # Graficar cada 100 pasos de tiempo
            ax.plot(r * 1e3, HStress_t[:, i], label=f't={i * dt:.1f} años')  # Convertir r a mm
        
        ax.set_xlabel('r [mm]')
        ax.set_ylabel(r'$\sigma_\theta$ [Pa]')  # Etiqueta para el estrés tangencial
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        ax.set_title('Estrés Tangencial vs radio (5 años)')
        ax.grid()

        # Crear un canvas y agregarlo al layout
        self.canvas = FigureCanvas(fig)
        self.layout.addWidget(self.canvas)  # Agregar el canvas al layout
        self.canvas.draw()  # Dibujar el canvas

    def VolverMenu(self):
        self.close()
        self.main_window.show()