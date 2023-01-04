from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel

from strings import teacherViewStrings as strings
from strings import backButtonText
from view import View

# TODO: add teacher view design

class TeacherView(View):
    def __init__(self, navigator):
        super().__init__()
        
        layout = QVBoxLayout()

        self.widgets = [
            QLabel(strings["promptText"]),
            QPushButton(backButtonText)
        ]   

        self.widgets[1].clicked.connect(lambda: navigator.openStartView())

        for widget in self.widgets:
            layout.addWidget(widget)

        self.setLayout(layout)