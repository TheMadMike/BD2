from unittest.mock import patch
from unittest import TestCase

from teacher_service import TeacherService
from exceptions import TeacherNotFound
from teacher import Teacher

@patch("teacher_service.DbSession")
class TestTeacherService(TestCase):

    # should raise TeacherNotFound exception when no rows
    def test_getBasicTeacherDataByPesel_should_raiseException_when_noRows(self, DbSessionMock):
        # Setup DbSession mock
        session = DbSessionMock()

        # Given:
        uut = TeacherService(session)

        # When:
        session.query.return_value = []
        
        # Then:
        with self.assertRaises(TeacherNotFound) as exception:
            uut.getBasicTeacherDataByPesel('123')

    # should not raise any exceptions when one row with 7 columns fetched
    def test_getBasicTeacherDataByPesel_shouldNot_raiseExceptions_when_oneRow(self, DbSessionMock):
        # Setup DbSession mock
        session = DbSessionMock()

        # Given:
        uut = TeacherService(session)

        # When:
        expected_value = [ ("1", "TEST", "", "", "", "", "" ,"", "") ]
        session.query.return_value = expected_value
        student = uut.getBasicTeacherDataByPesel('123')

        # Then:
        assert student.name == "TEST"
