from db_session import DbSession
from student import Student
from exceptions import StudentNotFound

class StudentService:
    def __init__(self, dbSession : DbSession):
        self.session = dbSession


    def getBasicStudentDataByPesel(self, pesel) -> Student:
        rows = self.session.query(f"SELECT * FROM system.v_uczniowie WHERE \"pesel\"='{pesel}'")
        if len(rows) != 1:
            raise StudentNotFound(pesel)
        
        record = rows[0]

        student = Student()
        student.id = record[0]
        student.name = record[1]
        student.surname = record[2]
        student.pesel = record[3]
        student.startDate = record[4]
        student.classId = record[5]
        student.major = record[6]

        return student

    def getAllGradesByStudentPesel(self, pesel) -> list:
        try:
            rows = self.session.query(f"""
                SELECT \"Przedmiot\", \"rozszerzony?\", \"Ocena\", \"Data wystawienia oceny\"  
                FROM system.v_oceny 
                WHERE \"pesel\"='{pesel}'
                """)
        except Exception as exception:
            print(exception)
            return []
        
        return rows