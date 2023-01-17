from db_session import DbSession
from student_service import StudentService
from exceptions import StudentNotFound

from strings import studentViewStrings as strings
from strings import errorPrompt, studentNotFoundPrompt

class StudentController:

    def __init__(self, pesel, session: DbSession):
        self.pesel = pesel
        self.service = StudentService(session)


    def getBasicStudentDataAsMap(self) -> dict:
        try:
            student = self.service.getBasicStudentDataByPesel(self.pesel)
            return {
                strings["nameLabel"] : student.name,
                strings["surnameLabel"] : student.surname,
                strings["classLabel"] : student.classId,
                strings["majorLabel"] : student.major,
                strings["startDateLabel"] : student.startDate
            }    
        except StudentNotFound as exception:
            return { errorPrompt : studentNotFoundPrompt }
        
    # TODO: implement fetching student grades
    def getStudentGradeTable(self, studentId):
        pass