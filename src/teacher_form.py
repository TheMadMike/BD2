from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QLabel, QLineEdit, QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from teacher import Teacher
from datetime import date

from strings import teacherFormStrings as strings 

class TeacherForm(QDialog):
    def __init__(self, initialData : Teacher = Teacher()):
        super().__init__()

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.nameField = QLineEdit(initialData.name)
        self.surnameField = QLineEdit(initialData.surname)
        self.telephoneField = QLineEdit(initialData.telephone)
        self.emailField = QLineEdit(initialData.email)
        self.addressField = QLineEdit(initialData.address)

        if initialData.birthday == "":
            initialData.birthday = date.today()
            initialData.startDate = date.today()

        self.birthdayField = QLineEdit(str(initialData.birthday.strftime("%d-%m-%Y")))
        self.peselField = QLineEdit(initialData.pesel)
        self.startDateField = QLineEdit(str(initialData.startDate.strftime("%d-%m-%Y")))

        self.layout = QVBoxLayout()

        self.widgets = [
            QLabel(strings["nameLabel"]),
            self.nameField,
            QLabel(strings["surnameLabel"]),
            self.surnameField,
            QLabel(strings["telephoneLabel"]),
            self.telephoneField,
            QLabel(strings["emailLabel"]),
            self.emailField,
            QLabel(strings["addressLabel"]),
            self.addressField,
            QLabel(strings["birthdayLabel"]),
            self.birthdayField,
            QLabel(strings["peselLabel"]),
            self.peselField,
            QLabel(strings["startDateLabel"]),
            self.startDateField,
        ]

        for widget in self.widgets:
            self.layout.addWidget(widget)        
        
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    
    def getDataAsTeacher(self) -> Teacher:
        return Teacher(
            self.nameField.text(),
            self.surnameField.text(),
            self.telephoneField.text(),
            self.emailField.text(),
            self.addressField.text(),
            self.birthdayField.text(),
            self.peselField.text(),
            self.startDateField.text(),
        )


class AssignTeacherForm(QDialog):
    def __init__(self, subjects: list, hours, maxHours, teacherService, teacherId):
        super().__init__()

        self.teacherId = teacherId
        self.service = teacherService

        self.subjects = subjects

        self.hours = hours
        self.maxHours = maxHours

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.selectedSubject = None

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        self.hoursTaughtLabel = QLabel(f"{hours} / {maxHours}")
        self.subjectList = QListView()
        self.subjectModel = QStandardItemModel()

        for subject in subjects:
            self.subjectModel.appendRow(QStandardItem(subject[0]))
        
        self.subjectList.setModel(self.subjectModel)
        self.subjectList.clicked.connect(lambda index: self.setSubject(index.row()))

        self.classList = QListView()
        self.classList.clicked.connect(lambda index: self.setClass(index.row()))
        self.classModel = QStandardItemModel()
        self.classList.setModel(self.classModel)

        self.widgets = [
            QLabel(strings["subjectLabel"]),
            self.subjectList,
            QLabel(strings["classIdLabel"]),
            self.classList,
            QLabel(strings["hoursTaughtLabel"]),
            self.hoursTaughtLabel
        ]

        for widget in self.widgets:
            self.layout.addWidget(widget)        
        
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.classes = None


    def setSubject(self, index):
        self.selectedSubject = self.subjects[index][0]
        self.classes = self.service.getClassesForSubject(self.selectedSubject, self.teacherId)
        
        for c in self.classes:
            self.classModel.appendRow(QStandardItem(c[0]))

    
    def setClass(self, index):
        self.selectedClass = self.classes[index][0]

        additionalHours = self.service.getHoursForClassAndSubject(self.selectedSubject, self.selectedClass)

        self.hoursTaughtLabel.setText(f"{self.hours + additionalHours} / {self.maxHours}")

        if (self.hours + additionalHours) > self.maxHours:
            self.hoursTaughtLabel.setStyleSheet("color: red")
            self.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)
        else:
            self.buttonBox.button(QDialogButtonBox.Ok).setDisabled(False)
            self.hoursTaughtLabel.setStyleSheet("color: black")
        
