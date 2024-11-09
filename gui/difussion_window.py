from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget
from PyQt5 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from simulations.difussion import simulate_difussion  

class DifussionWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        uic.loadUi('resources/difussion_window.ui', self)
        self.main_window = main_window
        
        # Asumir que WDifussion ya está definido en el archivo .ui
        self.graphWidget = self.WDifussion  # Conectar directamente al QWidget llamado WDifussion
        self.layout = QVBoxLayout(self.graphWidget)  # Crear un layout vertical para el widget

        # Inicializar estado de simulación
        self.simulation_running = False
        self.canvas = None  # Para almacenar el canvas de la simulación

        # Conectar botones con métodos
        self.buttonRunSimulation.clicked.connect(self.RunSimulation)
        self.buttonStopSimulation.clicked.connect(self.StopSimulation)
        self.returnToMenu.clicked.connect(self.VolverMenu)

    def RunSimulation(self):
        if not self.simulation_running:  # Solo iniciar si no hay una simulación en curso
            self.simulation_running = True
            # Llama a la función de simulación que retorna la gráfica
            self.canvas = simulate_difussion()  # Suponiendo que esta función retorna un objeto de tipo FigureCanvas
            self.plot_graph(self.canvas)  # Llama a la función para mostrar la gráfica

    def plot_graph(self, canvas):
        # Limpiar el layout antes de agregar nuevos gráficos
        for i in reversed(range(self.layout.count())): 
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # Eliminar el widget anterior

        # Agregar el canvas de la gráfica al layout
        self.layout.addWidget(canvas)  # Agregar el canvas al layout
        canvas.draw()  # Dibujar el canvas

    def StopSimulation(self):
        if self.simulation_running:  # Solo detener si hay una simulación en curso
            self.simulation_running = False
            # Limpiar el layout para borrar la gráfica
            self.plot_graph(None)  # Llama a la función para limpiar la gráfica

    def VolverMenu(self):
        self.close()
        self.main_window.show()