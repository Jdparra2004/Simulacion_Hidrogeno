#librerias gui
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
from PyQt5 import uic
from simulations.combined_simulations import CombinedSimulation
from simulations.visualization_3d import generate_3d_image

class DifussionWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        uic.loadUi('resources/difussion_window.ui', self)
        self.main_window = main_window
        
        #botones
        self.buttonRunSimulation.clicked.connect(self.RunSimulation)
        self.buttonStopSimulation.clicked.connect(self.StopSimulation)
        self.returnToMenu.clicked.connect(self.VolverMenu)
        
        # Inicialización de la simulación
        self.simulation = None
        
        # Configurar área para la imagen 3D
        self.setup_3d_view()
    
    def setup_3d_view(self):
        # Configurar el área donde se mostrará la imagen 3D
        self.imageLabel = QLabel(self)
        self.imageLabel.setGeometry(50, 50, 400, 400) # ajustar al tamaño de la interfaz
        
        
    def RunSimulation(self):
        # Obtener parámetros de la interfaz
        params = self.get_parameters()
        
        # Iniciar simulación
        self.simulation = CombinedSimulation(params)
        
        # Instancia Difusión
        if isinstance(self, DifussionWindow):
            data = self.simulation.get_simulation_data(method="fd")
            image_path = generate_3d_image(data, type = "concentration")
            
        # Mostrar imagen
        sefl.display_3d_image(image_path)
    
    def get_parameters(self):
        return {
            'Ro'
            'Ri'
        }
    
    def display_3d_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setScaledContents(True)
    
    def StopSimulation(self):
        pass
    
    def VolverMenu(self):
        self.close()
        self.main_window.show()