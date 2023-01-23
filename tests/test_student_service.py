from unittest.mock import patch, Mock
from unittest import TestCase

from student_service import StudentService
from exceptions import StudentNotFound
from student import Student

DbSessionMock = Mock()

@patch("student_service.DbSession", new=DbSessionMock)
class TestStudentService(TestCase):

    def setUp(self):
        self.session = DbSessionMock()

    ### getBasicStudentDataByPesel

    # should raise StudentNotFound exception when no rows
    def test_getBasicStudentDataByPesel_should_raiseException_when_noRows(self):
        # Given:
        uut = StudentService(self.session)

        # When:
        self.session.query.return_value = []
        
        # Then:
        with self.assertRaises(StudentNotFound) as exception:
            uut.getBasicStudentDataByPesel('123')

    # should not raise any exceptions when one row with 7 columns fetched
    def test_getBasicStudentDataByPesel_shouldNot_raiseExceptions_when_oneRow(self):
        # Given:
        uut = StudentService(self.session)

        # When:
        expected_value = [ ("1", "TEST", "", "", "", "", "" ,"", "") ]
        self.session.query.return_value = expected_value
        student = uut.getBasicStudentDataByPesel('123')

        # Then:
        assert student.name == "TEST"

    
    ### getAllGradesByPesel

    def test_getAllGradesByPesel_shouldReturn_emptyList_when_noRows(self):
        # Given:
        uut = StudentService(self.session)

        # When:
        expected_value = []
        self.session.query.return_value = expected_value
        grades = uut.getAllGradesByStudentPesel('123')

        # Then:
        assert grades == expected_value


    def test_getAllGradesByPesel_shouldReturn_nonEmptyList_when_oneOrMoreRows(self):
        # Given:
        uut = StudentService(self.session)

        # When:
        expected_value = [[], []]
        self.session.query.return_value = expected_value
        grades = uut.getAllGradesByStudentPesel('123')

        # Then:
        assert len(grades) != 0
        assert grades == expected_value


    ### findAllStudentsMatchingPhrase

    def test_findAllStudentsMatchingPhrase_shouldReturn_emptyList_when_noRows(self):
        # Given:
        uut = StudentService(self.session)

        # When:
        expected_value = []
        self.session.query.return_value = expected_value
        students = uut.findAllStudentsMatchingPhrase("phrase")

        # Then:
        assert students == expected_value

    
    def test_findAllStudentsMatchingPhrase_shouldReturn_studentList_when_matchingStudentsFound(self):
        # Given:
        uut = StudentService(self.session)

        # When:
        expected_value = [ [1, "Mike", "Tyson", "123", "", "", ""] ]
        self.session.query.return_value = expected_value
        students = uut.findAllStudentsMatchingPhrase("Mike")

        # Then:
        assert type(students[0]) == Student
        assert len(students) == 1
        assert students[0].name == "Mike" and students[0].surname == "Tyson"


    ### getFinalGrade

    def test_getFinalGrade_shouldThrow_StudentNotFound_when_noRowsFetched(self):
        # Given:
        uut = StudentService(self.session)
        
        # When:
        expected_value = []
        self.session.query.return_value = expected_value
        
        # Then:
        with self.assertRaises(StudentNotFound) as exception:
            uut.getFinalGrade('123', 'subject')


    def test_getFinalGrade_shouldReturn_float_when_studentExists(self):
        # Given:
        uut = StudentService(self.session)

        # When:
        expected_value = [[5.0]]
        self.session.query.return_value = expected_value
        grade = uut.getFinalGrade('123', 'subject')

        # Then:
        assert type(grade) == float
        assert grade == expected_value[0][0]
    
    
    ### gradeStudent

    def test_gradeStudent_shouldThrow_StudentNotFound_when_noRowsFetched(self):
        # Given:
        uut = StudentService(self.session)

        # When:
        expected_value = []
        self.session.query.return_value = expected_value

        # Then:
        with self.assertRaises(StudentNotFound) as exception:
            uut.getFinalGrade('123', 'subject')
    

    ### getGradesMeanForSubject

    def test_getGradesMeanForSubject_shouldThrow_when_noRowsFetched(self):
        # Given:
        uut = StudentService(self.session)

        # When:
        expected_value = []
        self.session.query.return_value = expected_value

        # Then:
        with self.assertRaises(Exception) as exception:
            uut.getGradesMeanForSubject('123', 'subject')


    def test_getGradesMeanForSubject_shouldReturnFloat_when_studentExists(self):
        # Given:
        uut = StudentService(self.session)

        # When:
        expected_value = [[5.0]]
        self.session.query.return_value = expected_value
        grade = uut.getGradesMeanForSubject('123', 'subject')

        # Then:
        assert type(grade) == float
        assert grade == expected_value[0][0]