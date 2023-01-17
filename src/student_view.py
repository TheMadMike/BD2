from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QTableView, QHeaderView

from strings import studentViewStrings as strings
from strings import backButtonText
from view import View
from map_widget import MapWidget
from student_controller import StudentController

class StudentView(View):
    def __init__(self, navigator, pesel, session):
        super().__init__()

        self.controller = StudentController(pesel, session)
        
        layout = QVBoxLayout()  
        studentData = MapWidget(self.controller.getBasicStudentDataAsMap())
        
        gradeTable = QTableView()
        gradeTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        gradeTable.setModel(self.controller.getStudentGradeTable())

        self.widgets = [
            QLabel(strings["promptText"]),
            studentData,
            QLabel(strings["gradeTableTitle"]),
            gradeTable
        ]   

        backButton = QPushButton(backButtonText)
        
        backButton.clicked.connect(lambda: navigator.navigateToStart())

        for widget in self.widgets:
            layout.addWidget(widget)

        layout.addWidget(backButton)

        self.setLayout(layout)
    