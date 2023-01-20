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

        return self.__recordToStudent(record)

    
    def getAllGradeIdsByStudentPesel(self, pesel) -> list:
        try:
            rows = self.session.query(f"""
                SELECT \"Id oceny\"
                FROM system.v_oceny 
                WHERE \"pesel\"='{pesel}'
                """)
        except Exception as exception:
            print(exception)
            return []
        
        return rows


    def getFinalGrade(self, studentId, subject) -> float:
        try:
            rows = self.session.query(f"""
                SELECT ocena_koncowa
                FROM system.przedmioty_uczen
                JOIN system.przedmioty USING (id_przedmiotu)
                WHERE id_ucznia={studentId} AND nazwa_przedmiotu LIKE '{subject}%'  
            """)
        except Exception as exception:
            print(exception)
            raise StudentNotFound(pesel)
        
        return float(rows[0][0])


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


    def findAllStudentsMatchingPhrase(self, searchPhrase, teacherPesel = None) -> list:
        query = f"""
            SELECT *
            FROM system.v_uczniowie 
            WHERE \"Imie\" LIKE '%{searchPhrase}%'
            OR \"Nazwisko\" LIKE '%{searchPhrase}%'
        """

        if teacherPesel is not None:
            query = f"""
            SELECT *
            FROM system.v_uczniowie 
            WHERE (\"Imie\" LIKE '%{searchPhrase}%'
            OR \"Nazwisko\" LIKE '%{searchPhrase}%')
            AND \"Id klasy\" IN (SELECT id_klasy 
                    from system.przydzielone_godziny pg
                    join system.nauczyciel_przedmiot np ON pg.id_nauczyciel_przedmiot = np.id_nauczyciel_przedmiot
                    join system.przedmioty_klasy pk ON pg.id_przedmioty_klasy = pk.id_przedmioty_klasy
                    join system.v_nauczyciele n ON np.id_nauczyciela = n.id_nauczyciela
                    WHERE \"pesel\" = '{teacherPesel}')
            """

        rows = self.session.query(query)

        students = []

        for record in rows:
            students.append(self.__recordToStudent(record))

        return students

    #TODO: handle errors properly in GUI
    def gradeStudent(self, pesel, subject, grade):
        try:
            cursor = self.session.connection.cursor()
            cursor.callproc('system.wpisanie_oceny', [pesel, subject, float(grade)])
        except Exception as exception: 
            print(exception)
    

    def setFinalGrade(self, pesel, subject, grade):
        try:
            cursor = self.session.connection.cursor()
            cursor.callproc('system.wpisanie_oceny_koncowej', [pesel, subject, float(grade)])
        except Exception as exception:
            print(exception)

    
    def modifyGrade(self, gradeId, grade):
        try:
            cursor = self.session.connection.cursor()
            cursor.callproc('system.modyfikacja_oceny', [gradeId, grade])
        except Exception as exception:
            print(exception)


    def getGradesMeanForSubject(self, studentId, subject) -> float:
        try:
            rows = self.session.query(f"""
                SELECT srednia_ocen
                FROM system.przedmioty_uczen
                JOIN system.przedmioty USING (id_przedmiotu)
                WHERE id_ucznia={studentId} AND nazwa_przedmiotu LIKE '{subject}%'      
            """)

            return float(rows[0][0])

        except Exception as exception:
            print(exception)
            return 0.0

    def __recordToStudent(self, record) -> Student:
        student = Student()
        student.id = record[0]
        student.name = record[1]
        student.surname = record[2]
        student.pesel = record[3]
        student.startDate = record[4]
        student.classId = record[5]
        student.major = record[6]

        return student