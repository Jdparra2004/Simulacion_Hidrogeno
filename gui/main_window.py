# librerias gui
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
from PyQt5 import uic
import sys

# funciones para cada interfaz
from gui.difussion_window import DifussionWindow
from gui.radial_stress_window import RadialStressWindow
from gui.tangential_stress_window import TangentialStressWindow
from gui.comparison_window import ComparisonWindow
from simulations.difussion import simulate_difussion 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('resources/main_window.ui', self)
        
        # Conectar botones con métodos
        self.buttonDifussion.clicked.connect(self.open_difussion_window)
        self.buttonTangentialStress.clicked.connect(self.open_tangential_stress_window)
        self.buttonRadialStress.clicked.connect(self.open_radial_stress_window)
        self.buttonComparison.clicked.connect(self.open_comparison_window)
        
    def open_difussion_window(self):
        self.hide()
        self.diffusion_window = DifussionWindow(self)
        self.diffusion_window.show()
    
    def open_tangential_stress_window(self):
        self.hide()
        self.tangential_stress_window = TangentialStressWindow(self)
        self.tangential_stress_window.show()
    
    def open_radial_stress_window(self):
        self.hide()
        self.radial_stress_window = RadialStressWindow(self)
        self.radial_stress_window.show()
        
    def open_comparison_window(self):
        self.hide()
        self.comparison_window = ComparisonWindow(self)
        self.comparison_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
