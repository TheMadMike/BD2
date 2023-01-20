from teacher import Teacher
from exceptions import TeacherNotFound
from db_session import DbSession

class TeacherService:
    def __init__(self, dbSession : DbSession):
        self.session = dbSession
    

    def getBasicTeacherDataByPesel(self, pesel) -> Teacher:
        rows = self.session.query(f""" 
            SELECT *
            FROM system.v_nauczyciele
            WHERE \"pesel\"='{pesel}'
        """)

        if len(rows) < 1:
            raise TeacherNotFound(pesel)

        return self.__recordToTeacher(rows[0])


    def getTaughtSubjects(self, pesel) -> list:
        return self.session.query(f"""
            SELECT DISTINCT SUBSTR("przedmiot", 0, length("przedmiot")-2)
            FROM system.v_nauczyciel_przedmiot
            WHERE \"pesel\"='{pesel}'
        """)   


    def __recordToTeacher(self, record) -> Teacher:
        teacher = Teacher(record[1], record[2], record[3], record[4], record[5], record[6])
        teacher.id = record[0]

        return teacher