import math
from map_widget import MapWidget
from student_service import StudentService
from teacher_service import TeacherService, TeacherNotFound
from grade_dialog import GradeDialog, ModifyGradeDialog
from error_box import ErrorBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from strings import teacherViewStrings as strings
from strings import errorPrompt, teacherNotFoundPrompt

class TeacherController:
    def __init__(self, pesel, dbSession, gradesModel, selectedStudentLabel):
        self.pesel = pesel
        self.selectedStudent = None
        self.selectedGradeIndex = None
        self.students = None
        self.grades = None
        self.gradesModel = gradesModel
        self.selectedStudentLabel = selectedStudentLabel

        self.studentService = StudentService(dbSession)
        self.teacherService = TeacherService(dbSession)

        self.reloadTeacherData()


    def reloadTeacherData(self):
        try:
            self.teacher = self.teacherService.getBasicTeacherDataByPesel(self.pesel)
        except TeacherNotFound as exception:
            print(exception)
            self.teacher = None


    def addGrade(self):
        if self.selectedStudent is None:
            ErrorBox(strings["studentNotChosen"]).exec()
            return

        dialog = GradeDialog(self.teacherService.getTaughtSubjects(self.pesel))
        if dialog.exec():
            if dialog.selectedSubject is None:
                ErrorBox(strings["subjectNotChosen"]).exec()
                return
            try:
                if math.isnan(float(dialog.gradeField.text())):
                    ErrorBox(strings["invalidGrade"]).exec()
                    return

                self.studentService.gradeStudent(self.selectedStudent.pesel, dialog.selectedSubject, dialog.gradeField.text())
                self.reloadGradeList()
            except Exception as exception:
                ErrorBox(strings["invalidGrade"]).exec()


    def addFinalGrade(self):
        if self.selectedStudent is None:
            ErrorBox(strings["studentNotChosen"]).exec()
            return

        dialog = GradeDialog(self.teacherService.getTaughtSubjects(self.pesel), self.studentService, self.selectedStudent.id)
        if dialog.exec():
            if dialog.selectedSubject is None:
                ErrorBox(strings["subjectNotChosen"]).exec()
                return
            try:
            
                if math.isnan(float(dialog.gradeField.text())):
                    ErrorBox(strings["invalidGrade"]).exec()
                    return
            
                self.studentService.setFinalGrade(self.selectedStudent.pesel, dialog.selectedSubject, dialog.gradeField.text())
                self.selectedStudent = None
            except Exception as exception:
                ErrorBox(strings["invalidGrade"]).exec()
                print(exception)

    def modifyGrade(self):
        if self.selectedStudent is None:
            ErrorBox(strings["studentNotChosen"]).exec()
            return

        if self.selectedGradeIndex is None:
            ErrorBox(strings["gradeNotChosen"]).exec()
            return

        dialog = ModifyGradeDialog()
        if dialog.exec():
            try:
                if math.isnan(float(dialog.gradeField.text())) or dialog.gradeField.text() == "":
                    ErrorBox(strings["invalidGrade"]).exec()
                    return
            
                gradeIds = self.studentService.getAllGradeIdsByStudentPesel(self.selectedStudent.pesel)
                gradeId = gradeIds[self.selectedGradeIndex][0]
                
                self.studentService.modifyGrade(gradeId, dialog.gradeField.text())
                self.reloadGradeList()
                self.selectedStudent = None
            except Exception as exception:
                ErrorBox(strings["invalidGrade"]).exec()
                print(exception)
            


    def getTeacherNameAndSurname(self):
        return f"{self.teacher.name} {self.teacher.surname}"


    def findStudents(self, searchPhrase="") -> QStandardItemModel:
        try:
            self.students = self.studentService.findAllStudentsMatchingPhrase(searchPhrase, self.pesel)

            model = QStandardItemModel()
            for student in self.students:
                model.appendRow(QStandardItem(f"{student.name} {student.surname} ({student.classId})"))

            return model 
        except Exception as exception:
            print(exception)
            return QStandardItemModel()

        
    def selectStudent(self, index):
        self.selectedStudent = self.students[index.row()]
        self.selectedStudentLabel.setText(f"{self.selectedStudent.name} {self.selectedStudent.surname}")

        self.reloadGradeList()

    
    def reloadGradeList(self):
        self.gradesModel.clear()
        self.grades = self.studentService.getAllGradesByStudentPesel(self.selectedStudent.pesel)
        for grade in self.grades:
            lvlStr = strings["basicLevel"] if grade[1] == "podstawa" else strings["extendedLevel"]
            self.gradesModel.appendRow(QStandardItem(f"{grade[2]} - {grade[0]} {lvlStr} [{grade[3]}]"))
        

    def selectGrade(self, index):
        self.selectedGradeIndex = index.row()    

    
    def getBasicTeacherData(self) -> dict:
        if self.teacher is None:
            return { errorPrompt : teacherNotFoundPrompt }
        
        return {
            strings["nameLabel"] : self.teacher.name,
            strings["surnameLabel"] : self.teacher.surname,
            strings["startDateLabel"] : self.teacher.startDate
        }