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


    #TODO: write tests for those methods:
    def test_methodsNotCovered(self):
        raise Exception("Some StudentService methods are not covered yet!")

    ### getAllGradeIdsByStudentPesel

    ### getFinalGrade

    ### gradeStudent

    ### setFinalGrade

    ### modifyGrade

    ### getGradesMeanForSubject