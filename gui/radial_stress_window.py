from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from PyQt5 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from utils import generar_graficas, r, historial_esfuerzo_radial, historial_esfuerzo_tangencial, dt, n_tiempos

class RadialStressWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        uic.loadUi('resources/radial_stress_window.ui', self)
        self.main_window = main_window

        # Conectar directamente al QWidget llamado WRadial en el archivo .ui
        self.graphWidget = self.WRadial
        self.layout = QVBoxLayout(self.graphWidget)  # Crear un layout vertical para el widget

        # Inicializar el canvas
        self.canvas = None

        # Conectar botones con métodos
        self.buttonRunSimulation.clicked.connect(self.RunSimulation)
        self.returnToMenu.clicked.connect(self.VolverMenu)

    def RunSimulation(self):
        try:
            # Llamar a la función generar_graficas para obtener las figuras
            figuras = generar_graficas(r, historial_esfuerzo_radial, historial_esfuerzo_tangencial, dt, n_tiempos)

            # Verificar que figuras no esté vacío
            if figuras:
                # Seleccionar la figura radial (figuras[0]) 
                fig_radial = figuras[0]

                # Mostrar fig_radial en el QWidget de la interfaz
                self.display_graph(fig_radial)
            else:
                print("Error: No se generaron gráficos.")
        except Exception as e:
            print(f"Error al generar gráficos: {e}")

    def display_graph(self, fig):
        # Limpiar el layout antes de agregar nuevos gráficos
        for i in reversed(range(self.layout.count())): 
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # Eliminar el widget anterior

        # Crear un nuevo canvas para el gráfico
        self.canvas = FigureCanvas(fig)
        self.layout.addWidget(self.canvas)  # Agregar el canvas al layout
        self.canvas.draw()  # Dibujar el canvas

    def VolverMenu(self):
        self.close()
        self.main_window.show()