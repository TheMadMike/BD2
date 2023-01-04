from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel

from strings import studentViewStrings as strings
from strings import backButtonText
from view import View

# TODO: add student view design

class StudentView(View):
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