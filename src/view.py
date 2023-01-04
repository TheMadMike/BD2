from PyQt5.QtWidgets import QWidget

class View(QWidget):
    widgets : list = []
    def __init__(self):
        super().__init__()