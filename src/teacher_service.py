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


    def getAllTeachers(self) -> list:
        try:
            rows = self.session.query(f"""
                SELECT *
                FROM system.v_nauczyciele
            """)

            teachers = []

            for record in rows:
                teachers.append(self.__recordToTeacher(record))
            
            return teachers
        except Exception as exception:
            print(exception)
            return []


    def getFullTeacherData(self, pesel):
        teacher = Teacher()
        try:
            teacherViewRows = self.session.query(f"""
                SELECT *
                FROM system.v_nauczyciele
                WHERE \"pesel\"='{pesel}'
            """)

            if len(teacherViewRows) < 1:
                raise Exception()

            teacher = self.__recordToTeacher(teacherViewRows[0])

            personalDataRows = self.session.query(f"""
                SELECT numer_telefonu, email, adres_zamieszkania, data_urodzenia
                FROM system.dane_osobowe
                WHERE pesel='{pesel}'
            """)

            teacher.telephone = personalDataRows[0][0]
            teacher.email = personalDataRows[0][1]
            teacher.address = personalDataRows[0][2]
            teacher.birthday = personalDataRows[0][3]


        except Exception as exception:
            raise TeacherNotFound(pesel)

        return teacher


    def updateTeacher(self, teacher: Teacher):
        try:
            cursor = self.session.getCursor()
            cursor.callproc('system.aktualizuj_dane_nauczyciela', [
                teacher.name,
                teacher.surname,
                teacher.telephone,
                teacher.email,
                teacher.address,
                teacher.birthday,
                teacher.pesel,
                teacher.startDate,
            ])
        except Exception as exception:
            print(exception)


    def addNewTeacher(self, teacher: Teacher):
        try:
            cursor = self.session.getCursor()
            cursor.callproc('system.dodaj_nauczyciela', [
                teacher.name,
                teacher.surname,
                teacher.telephone,
                teacher.email,
                teacher.address,
                teacher.birthday,
                teacher.pesel,
                teacher.startDate,
            ])
        except Exception as exception:
            print(exception)


    def findAllTeachersMatchingPhrase(self, phrase):
        query = f"""
            SELECT *
            FROM system.v_nauczyciele
            WHERE \"Imie\" LIKE '%{phrase}%'
            OR \"Nazwisko\" LIKE '%{phrase}%'
            OR \"pesel\" LIKE '{phrase}%'
        """

        rows = self.session.query(query)

        teachers = []

        for record in rows:
            teachers.append(self.__recordToTeacher(record))

        return teachers

    def deleteTeacher(self, pesel):
        try:
            cursor = self.session.getCursor()
            cursor.execute(f"""
                DELETE FROM system.dane_osobowe
                WHERE pesel='{pesel}'
            """)
            self.session.commitChange()
        except Exception as exception:
            print(exception)
            raise TeacherNotFound(pesel)


    def __recordToTeacher(self, record) -> Teacher:
        teacher = Teacher()
        teacher.id = record[0]
        teacher.name = record[1]
        teacher.surname = record[2]
        teacher.pesel = record[3]
        teacher.startDate = record[4]
        teacher.maxWorkHoursWeekly = record[5]
        teacher.availableHoursWeekly = record[6]

        return teacher

    
    def getClassesForSubject(self, subject, teacherId) -> list:
        try:
            return self.session.query(f"""
            SELECT id_klasy 
            FROM system.przedmioty_klasy 
            JOIN system.przedmioty USING (id_przedmiotu)
            JOIN system.przydzielone_godziny USING (id_przedmioty_klasy)
            JOIN system.nauczyciel_przedmiot USING (id_nauczyciel_przedmiot)
            WHERE nazwa_przedmiotu LIKE '{subject}%' AND id_nauczyciela <> {teacherId}
            """)
        except Exception as exception:
            print(exception)

        return []


    def getHoursForClassAndSubject(self, subject, classId) -> int:
        try:
            rows = self.session.query(f"""
            SELECT ilosc_godzin_przedmiotu
            FROM system.przedmioty_klasy JOIN system.przedmioty USING (id_przedmiotu)
            WHERE id_klasy = '{classId}' AND nazwa_przedmiotu LIKE '{subject}%'
            """)
            if len(rows) < 1:
                raise Exception()
            
            return int(rows[0][0])

        except Exception as exception:
            print(exception)

        return 0


    def assignTeacher(self, teacherId, subject, classId):
        try:
            print(teacherId)
            print(subject)
            print(classId)
            cursor = self.session.getCursor()
            cursor.callproc('system.przydziel_godziny', [
                teacherId,
                subject,
                classId
            ])
        except Exception as exception:
            print(exception)