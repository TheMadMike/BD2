from unittest.mock import patch
from unittest import TestCase

from student_service import StudentService
from exceptions import StudentNotFound

@patch("student_service.DbSession")
class TestStudentService(TestCase):

    # should raise StudentNotFound exception when no rows
    def test_getStudentDataByPesel_should_raiseException_when_noRows(self, DbSessionMock):
        # Setup DbSession mock
        session = DbSessionMock()

        # Given:
        uut = StudentService(session)

        # When:
        session.query.return_value = []
        
        # Then:
        with self.assertRaises(StudentNotFound) as exception:
            uut.getStudentDataByPesel('123')

    # should not raise any exceptions when one row with 7 columns fetched
    def test_getStudentDataByPesel_shouldNot_raiseExceptions_when_oneRow(self, DbSessionMock):
        # Setup DbSession mock
        session = DbSessionMock()

        # Given:
        uut = StudentService(session)

        # When:
        expected_value = [ ("1", "TEST", "", "", "", "", "" ,"", "") ]
        session.query.return_value = expected_value
        student = uut.getStudentDataByPesel('123')

        # Then:
        assert student.name == "TEST"
        
        