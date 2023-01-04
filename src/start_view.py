from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel

from strings import startViewStrings as strings
from view import View

class StartView(View):
    def __init__(self, navigator):
        super().__init__()
        
        layout = QVBoxLayout()

        self.widgets = [
            QLabel(strings["promptText"]),
            QPushButton(strings["adminButtonText"]),
            QPushButton(strings["studentButtonText"]),
            QPushButton(strings["teacherButtonText"])
        ]   

        self.widgets[1].clicked.connect(lambda: navigator.navigateToAdminPanel())
        self.widgets[2].clicked.connect(lambda: navigator.navigateToStudentPanel())
        self.widgets[3].clicked.connect(lambda: navigator.navigateToTeacherPanel())

        for widget in self.widgets:
            layout.addWidget(widget)

        self.setLayout(layout)