from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QLineEdit, QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from strings import teacherViewStrings as strings
from strings import backButtonText
from view import View

from teacher_controller import TeacherController

class TeacherView(View):
    def __init__(self, navigator, pesel, dbSession):
        super().__init__()
        
        layout = QVBoxLayout()

        self.gradesModel = QStandardItemModel()

        self.selectedStudentLabel = QLabel("")

        self.controller = TeacherController(pesel, dbSession, self.gradesModel, self.selectedStudentLabel)

        self.studentSearchBar = QLineEdit()
        self.studentSearchBar.setPlaceholderText(strings["searchBarPlaceholder"])

        self.searchButton = QPushButton(strings["searchButtonText"])

        self.studentList = QListView()

        self.studentList.setModel(self.controller.findStudents())

        self.studentList.clicked.connect(self.controller.selectStudent)

        self.searchButton.clicked.connect(
            lambda: 
            self.studentList.setModel(self.controller.findStudents(self.studentSearchBar.text()))
        )

        self.addGradeButton = QPushButton(strings["addGradeText"])
        self.addGradeButton.clicked.connect(self.controller.addGrade)
        

        self.addFinalGradeButton = QPushButton(strings["addFinalGradeText"])
        self.addFinalGradeButton.clicked.connect(self.controller.addFinalGrade)

        self.modifyGradeButton = QPushButton(strings["modifyGradeText"])
        self.modifyGradeButton.clicked.connect(self.controller.modifyGrade)

        self.studentGradeList = QListView()
        self.studentGradeList.setModel(self.gradesModel)
        self.studentGradeList.clicked.connect(self.controller.selectGrade)

        self.widgets = [
            QLabel(strings["promptText"]),
            QLabel(strings["loggedAs"] + self.controller.getTeacherNameAndSurname()),
            self.studentSearchBar,
            self.searchButton,
            self.studentList,
            self.selectedStudentLabel,
            QLabel(strings["gradeTableTitle"]),
            self.studentGradeList,
            self.addGradeButton,
            self.addFinalGradeButton,
            self.modifyGradeButton,
            QPushButton(backButtonText)
        ]   

        self.widgets[len(self.widgets)-1].clicked.connect(lambda: navigator.navigateToStart())

        for widget in self.widgets:
            layout.addWidget(widget)

        self.setLayout(layout)