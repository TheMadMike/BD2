from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QLabel, QLineEdit
from student import Student
from datetime import date

from strings import studentFormStrings as strings 

class StudentForm(QDialog):
    def __init__(self, initialData : Student = Student()):
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
        self.classIdField = QLineEdit(initialData.classId)

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
            QLabel(strings["classIdLabel"]),
            self.classIdField
        ]

        for widget in self.widgets:
            self.layout.addWidget(widget)        
        
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    
    def getDataAsStudent(self) -> Student:
        return Student(
            self.nameField.text(),
            self.surnameField.text(),
            self.telephoneField.text(),
            self.emailField.text(),
            self.addressField.text(),
            self.birthdayField.text(),
            self.peselField.text(),
            self.startDateField.text(),
            self.classIdField.text(),
        )