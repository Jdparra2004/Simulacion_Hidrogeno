#librerias gui
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
from PyQt5 import uic

from simulations.difussion import simulate_difussion  

class TangentialStressWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        uic.loadUi('resources/tangential_stress_window.ui', self)
        self.main_window = main_window
        
        #botones
        self.buttonRunSimulation.clicked.connect(self.RunSimulation)
        self.returnToMenu.clicked.connect(self.VolverMenu)
        
    def RunSimulation(self):
        pass
    
    def VolverMenu(self):
        self.close()
        self.main_window.show()