#librerias gui
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
from PyQt5 import uic

class RadialStressWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        uic.loadUi('resources/radial_stress_window.ui', self)
        self.main_window = main_window
        
        #botones
        self.buttonRunSimulation.clicked.connect(self.RunSimulation)
        self.buttonStopSimulation.clicked.connect(self.StopSimulation)
        self.returnToMenu.clicked.connect(self.VolverMenu)
        
    def RunSimulation(self):
        pass
    
    def StopSimulation(self):
        pass
    
    def VolverMenu(self):
        self.close()
        self.main_window.show()
