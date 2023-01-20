from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QLabel, QLineEdit, QCheckBox, QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from strings import teacherViewStrings as strings

class GradeDialog(QDialog):
    def __init__(self, subjects : list, studentService = None, studentId = None):
        super().__init__()

        self.studentId = studentId
        self.studentService = studentService
        self.subjects = subjects
        self.selectedSubject = None

        self.setWindowTitle(strings["gradeDialogTitle"])

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.gradeField = QLineEdit()

        self.meanLabel = QLabel("")
        self.finalGradeLabel = QLabel("")
        if studentService is not None:
            self.layout.addWidget(self.finalGradeLabel)
            self.layout.addWidget(self.meanLabel)

        self.layout.addWidget(QLabel(strings["gradeLabel"]))
        self.layout.addWidget(self.gradeField)            

        self.subjectList = QListView()
        self.subjectModel = QStandardItemModel()

        for subject in subjects:
            self.subjectModel.appendRow(QStandardItem(subject[0]))
        
        self.subjectList.setModel(self.subjectModel)
        self.subjectList.clicked.connect(lambda index: self.setSubject(index.row()))

        self.layout.addWidget(QLabel(strings["subjectLabel"]))        
        self.layout.addWidget(self.subjectList)
        

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    
    def setSubject(self, index):
        self.selectedSubject = self.subjects[index][0]
        
        if self.studentService is not None:
            mean = self.studentService.getGradesMeanForSubject(self.studentId, self.selectedSubject)
            finalGrade = self.studentService.getFinalGrade(self.studentId, self.selectedSubject)
            self.meanLabel.setText(strings["meanLabel"] + f" {str(mean)}")
            self.finalGradeLabel.setText(strings["finalGradeLabel"] + f" {str(finalGrade)}")


class ModifyGradeDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(strings["gradeDialogTitle"])

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.gradeField = QLineEdit()

        self.layout.addWidget(QLabel(strings["gradeLabel"]))
        self.layout.addWidget(self.gradeField)            

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)