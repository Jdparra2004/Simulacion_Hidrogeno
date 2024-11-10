#librerias gui
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
from PyQt5 import uic

from simulations.difussion import simulate_difussion  

class ComparisonWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        uic.loadUi('resources/comparison_window.ui', self)
        self.main_window = main_window
        
        #botones
        self.buttonDifFinitas.clicked.connect(self.DifFinitas)
        self.buttonHomotopia.clicked.connect(self.Homotopia)
        self.returnToMenu.clicked.connect(self.VolverMenu)
        
    def DifFinitas(self):
        pass
    
    def Homotopia(self):
        pass
    
    def VolverMenu(self):
        self.close()
        self.main_window.show()
