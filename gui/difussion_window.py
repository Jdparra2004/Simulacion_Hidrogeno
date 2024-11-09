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

        # Conectar botones con métodos
        self.buttonRunSimulation.clicked.connect(self.RunSimulation)
        self.buttonStopSimulation.clicked.connect(self.StopSimulation)
        self.returnToMenu.clicked.connect(self.VolverMenu)

    def RunSimulation(self):
        # Llama a la función de simulación que retorna la gráfica
        canvas = simulate_difussion()  # Suponiendo que esta función retorna un objeto de tipo FigureCanvas
        self.plot_graph(canvas)  # Llama a la función para mostrar la gráfica

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
        # Aquí puedes agregar lógica para detener la simulación si es necesario
        pass
    
    def VolverMenu(self):
        self.close()
        self.main_window.show()