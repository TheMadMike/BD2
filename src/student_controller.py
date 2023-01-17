from db_session import DbSession
from student_service import StudentService
from exceptions import StudentNotFound
from table import TableModel

from strings import studentViewStrings as strings
from strings import errorPrompt, studentNotFoundPrompt

class StudentController:

    def __init__(self, pesel, session: DbSession):
        self.pesel = pesel
        self.service = StudentService(session)
        self.reloadStudentData()

    def reloadStudentData(self):
        try:
            self.student = self.service.getBasicStudentDataByPesel(self.pesel)
        except StudentNotFound as exception:
            self.student = None
            print(exception)

    def getBasicStudentDataAsMap(self) -> dict:
        if self.student is None:
            return { errorPrompt : studentNotFoundPrompt }                

        return {
            strings["nameLabel"] : self.student.name,
            strings["surnameLabel"] : self.student.surname,
            strings["classLabel"] : self.student.classId,
            strings["majorLabel"] : self.student.major,
            strings["startDateLabel"] : self.student.startDate
        }    

        
    def getStudentGradeTable(self) -> TableModel:
        if self.student is None:
            return TableModel([], [])

        grades = self.service.getAllGradesByStudentPesel(self.pesel)
        return TableModel(grades, [strings["subjectHeader"], strings["levelHeader"], strings["gradeHeader"], strings["gradeDateHeader"]])