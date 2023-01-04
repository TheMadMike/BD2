from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel

from strings import adminViewStrings as strings
from strings import backButtonText
from view import View

# TODO: add admin view design
class AdminView(View):
    def __init__(self, navigator):
        super().__init__()
        
        layout = QVBoxLayout()

        self.widgets = [
            QLabel(strings["promptText"]),
            QPushButton(backButtonText)
        ]   

        self.widgets[1].clicked.connect(lambda: navigator.navigateToStart())

        for widget in self.widgets:
            layout.addWidget(widget)

        self.setLayout(layout)