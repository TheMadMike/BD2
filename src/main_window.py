from PyQt5.QtWidgets import QWidget, QMainWindow
from view import View

from admin_view import AdminView
from start_view import StartView
from navigation import NavigationController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.navigator = NavigationController(self)