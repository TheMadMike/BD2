from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QLineEdit, QListView, QTableView

from strings import teacherViewStrings as strings
from strings import backButtonText
from view import View


class TeacherView(View):
    def __init__(self, navigator):
        super().__init__()
        
        layout = QVBoxLayout()

        self.studentSearchBar = QLineEdit(strings["searchBarPlaceholder"])

        self.searchButton = QPushButton(strings["searchButtonText"])

        self.studentList = QListView()

        self.addGradeButton = QPushButton(strings["addGradeText"])

        self.addFinalGradeButton = QPushButton(strings["addFinalGradeText"])

        self.modifyGradeButton = QPushButton(strings["modifyGradeText"])

        self.studentGradeTable = QTableView()

        self.widgets = [
            QLabel(strings["promptText"]),
            self.studentSearchBar,
            self.searchButton,
            self.studentList,
            QLabel(strings["gradeTableTitle"]),
            self.studentGradeTable,
            self.addGradeButton,
            self.addFinalGradeButton,
            self.modifyGradeButton,
            QPushButton(backButtonText)
        ]   

        self.widgets[len(self.widgets)-1].clicked.connect(lambda: navigator.navigateToStart())

        for widget in self.widgets:
            layout.addWidget(widget)

        self.setLayout(layout)