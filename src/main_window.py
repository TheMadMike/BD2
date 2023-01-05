from PyQt5.QtWidgets import QWidget, QMainWindow
from view import View
from navigation import NavigationController

from strings import mainWindowTitle

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(mainWindowTitle)
        self.navigator = NavigationController(self)