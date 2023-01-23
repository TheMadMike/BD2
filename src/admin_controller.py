from db_session import DbSession
from student_service import StudentService
from teacher_service import TeacherService
from table import TableModel
from teacher import Teacher
from error_box import ErrorBox

from strings import studentViewStrings, teacherViewStrings

from student_form import StudentForm
from teacher_form import TeacherForm, AssignTeacherForm

class AdminController:
    def __init__(self, dbSession, studentTable, teacherTable):
        self.studentService = StudentService(dbSession)
        self.teacherService = TeacherService(dbSession)
        self.studentTable = studentTable
        self.teacherTable = teacherTable

        self.studentList = None
        self.teacherList = None
        self.selectedStudent = None
        self.selectedTeacher = None

    
    def getAllStudentsAsTable(self) -> TableModel:
        self.studentList = self.studentService.getAllStudents()

        tableData = []
        for student in self.studentList:
            tableData.append([student.name, student.surname, student.pesel, student.classId, student.major])

        tableHeader = [
            studentViewStrings["nameLabel"],
            studentViewStrings["surnameLabel"],
            studentViewStrings["peselLabel"],
            studentViewStrings["classLabel"],
            studentViewStrings["majorLabel"]
        ]

        return TableModel(tableData, tableHeader)

    
    def reloadStudentTable(self):
        self.studentTable.setModel(self.getAllStudentsAsTable())


    def reloadTeacherTable(self):
        self.teacherTable.setModel(self.getAllTeachersAsTable())


    def addNewStudent(self):
        dialog = StudentForm()
        if dialog.exec():
            self.studentService.addNewStudent(dialog.getDataAsStudent())
            self.reloadStudentTable()


    def modifySelectedStudent(self):
        if self.selectedStudent is None:
            ErrorBox(teacherViewStrings["studentNotChosen"]).exec()
            return

        dialog = StudentForm(self.studentService.getFullStudentData(self.selectedStudent.pesel))
        dialog.peselField.setReadOnly(True)
        if dialog.exec():
            self.studentService.updateStudent(dialog.getDataAsStudent())
            self.reloadStudentTable()
            self.selectedStudent = None

    
    def deleteSelectedStudent(self):
        if self.selectedStudent is None:
            ErrorBox(teacherViewStrings["studentNotChosen"])
            return

        self.studentService.deleteStudent(self.selectedStudent.pesel)
        self.reloadStudentTable()
        self.selectedStudent = None


    def selectStudent(self, index):
        self.selectedStudent = self.studentList[index.row()]


    def findAllStudentsMatchingPhrase(self, phrase):
        self.studentList = self.studentService.findAllStudentsMatchingPhrase(phrase)

        tableData = []
        for student in self.studentList:
            tableData.append([student.name, student.surname, student.pesel, student.classId, student.major])

        tableHeader = [
            studentViewStrings["nameLabel"],
            studentViewStrings["surnameLabel"],
            studentViewStrings["peselLabel"],
            studentViewStrings["classLabel"],
            studentViewStrings["majorLabel"]
        ]

        if len(tableData) < 1:
            return None

        return TableModel(tableData, tableHeader)



    def getAllTeachersAsTable(self) -> TableModel:
        self.teacherList = self.teacherService.getAllTeachers()

        return self.__teacherListToTable()


    def __teacherListToTable(self) -> TableModel:
        tableData = []
        for teacher in self.teacherList:
            tableData.append([teacher.name, teacher.surname, teacher.pesel, teacher.availableHoursWeekly])

        tableHeader = [
            studentViewStrings["nameLabel"],
            studentViewStrings["surnameLabel"],
            studentViewStrings["peselLabel"],
            teacherViewStrings["availableHoursLabel"]
        ]

        if len(tableData) < 1:
            return None

        return TableModel(tableData, tableHeader)


    def addNewTeacher(self):
        dialog = TeacherForm()

        if dialog.exec():
            self.teacherService.addNewTeacher(dialog.getDataAsTeacher())
            self.reloadTeacherTable()


    def modifySelectedTeacher(self):
        if self.selectedTeacher is None:
            ErrorBox(teacherViewStrings["teacherNotChosen"]).exec()
            return

        dialog = TeacherForm(self.teacherService.getFullTeacherData(self.selectedTeacher.pesel))
        dialog.peselField.setReadOnly(True)

        if dialog.exec():
            self.teacherService.updateTeacher(dialog.getDataAsTeacher())
            self.reloadTeacherTable()    

    
    def deleteSelectedTeacher(self):
        if self.selectedTeacher is None:
            ErrorBox(teacherViewStrings["teacherNotChosen"]).exec()
            return

        self.teacherService.deleteTeacher(self.selectedTeacher.pesel)
        self.reloadTeacherTable()
        self.selectedTeacher = None

    def selectTeacher(self, index):
        self.selectedTeacher = self.teacherList[index.row()]


    def findAllTeachersMatchingPhrase(self, phrase):
        self.teacherList = self.teacherService.findAllTeachersMatchingPhrase(phrase)
        return self.__teacherListToTable()


    def assignTeacher(self):
        if self.selectedTeacher is None:
            ErrorBox(teacherViewStrings["teacherNotChosen"]).exec()
            return
        subjects = self.teacherService.getTaughtSubjects(self.selectedTeacher.pesel)

        availableHours = self.selectedTeacher.availableHoursWeekly
        hoursTeaching = self.selectedTeacher.maxWorkHoursWeekly - availableHours

        dialog = AssignTeacherForm(subjects, hoursTeaching, self.selectedTeacher.maxWorkHoursWeekly, self.teacherService, self.selectedTeacher.id)

        if dialog.exec():
            self.teacherService.assignTeacher(self.selectedTeacher.id, dialog.selectedSubject, dialog.selectedClass)
            self.reloadTeacherTable()