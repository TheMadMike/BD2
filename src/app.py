# University project on databases
# Copyright 2022 (c) Michał Gibas & Patryk Polkowski

from PyQt5.QtWidgets import QApplication, QMainWindow
from main_window import MainWindow

app = QApplication([])

window = MainWindow()
window.show()

app.exec()