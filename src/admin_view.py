from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTableView, QFrame
from PyQt5 import uic

from strings import adminViewStrings as strings
from strings import backButtonText
from view import View

from admin_controller import AdminController

class AdminView(View):
    def __init__(self, navigator, dbSession):
        super().__init__()
        
        layout = QVBoxLayout()

        self.studentTable = QTableView()
        self.teacherTable = QTableView()

        self.controller = AdminController(dbSession, self.studentTable, self.teacherTable)

        # students
        self.studentSearchBar = QLineEdit()
        self.studentSearchBar.setPlaceholderText(strings['searchForStudents'])

        self.studentSearchButton = QPushButton(strings['searchButtonText'])

        
        self.studentTable.setModel(self.controller.getAllStudentsAsTable())
        self.studentSearchButton.clicked.connect( lambda:
            self.studentTable.setModel(
                self.controller.findAllStudentsMatchingPhrase(self.studentSearchBar.text())
            )
        )

        self.addNewStudentButton = QPushButton(strings['addNewStudentText'])
        self.modifyStudentButton = QPushButton(strings['modifyText'])
        self.deleteStudentButton = QPushButton(strings['deleteStudentText'])

        self.addNewStudentButton.clicked.connect(self.controller.addNewStudent)
        self.modifyStudentButton.clicked.connect(self.controller.modifySelectedStudent)
        self.deleteStudentButton.clicked.connect(self.controller.deleteSelectedStudent)

        self.studentTable.clicked.connect(self.controller.selectStudent)

        # teachers
        self.teacherSearchBar = QLineEdit()
        self.teacherSearchBar.setPlaceholderText(strings['searchForTeachers'])

        self.teacherSearchButton = QPushButton(strings['searchButtonText'])

        
        self.teacherTable.setModel(self.controller.getAllTeachersAsTable())
        self.teacherSearchButton.clicked.connect( lambda:
            self.teacherTable.setModel(
                self.controller.findAllTeachersMatchingPhrase(self.teacherSearchBar.text())
            )
        )

        self.addNewTeacherButton = QPushButton(strings['addNewTeacherText'])
        self.modifyTeacherButton = QPushButton(strings['modifyText'])
        self.deleteTeacherButton = QPushButton(strings['deleteTeacherText'])
        self.assignTeacherButton = QPushButton(strings['assignTeacherText'])

        self.addNewTeacherButton.clicked.connect(self.controller.addNewTeacher)
        self.modifyTeacherButton.clicked.connect(self.controller.modifySelectedTeacher)
        self.deleteTeacherButton.clicked.connect(self.controller.deleteSelectedTeacher)
        self.assignTeacherButton.clicked.connect(self.controller.assignTeacher)

        self.teacherTable.clicked.connect(self.controller.selectTeacher)

        # vertical separator
        verticalSeparator = QFrame()
        verticalSeparator.setFrameShape(QFrame.HLine)
        verticalSeparator.setFrameShadow(QFrame.Sunken)

        self.widgets = [
            QLabel(strings["promptText"]),
            verticalSeparator,

            QLabel(strings['teachersTitle']),

            self.teacherSearchBar,
            self.teacherSearchButton,
            self.teacherTable,
            self.addNewTeacherButton,
            self.modifyTeacherButton,
            self.deleteTeacherButton,
            self.assignTeacherButton,

            QLabel(strings['studentsTitle']),
            self.studentSearchBar,
            self.studentSearchButton,
            self.studentTable,
            self.addNewStudentButton,
            self.modifyStudentButton,
            self.deleteStudentButton
        ]

        for widget in self.widgets:
            layout.addWidget(widget)

        backButton = QPushButton(backButtonText)

        backButton.clicked.connect(lambda: navigator.navigateToStart())

        layout.addWidget(backButton)

        self.setLayout(layout)