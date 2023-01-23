from unittest.mock import patch, Mock
from unittest import TestCase

from teacher_service import TeacherService
from exceptions import TeacherNotFound
from teacher import Teacher

DbSessionMock = Mock()

@patch("teacher_service.DbSession", new=DbSessionMock)
class TestTeacherService(TestCase):

    def setUp(self):
        self.session = DbSessionMock()


    ### getBasicTeacherDataByPesel

    # should raise TeacherNotFound exception when no rows
    def test_getBasicTeacherDataByPesel_should_raiseException_when_noRows(self):
        # Given:
        uut = TeacherService(self.session)

        # When:
        self.session.query.return_value = []
        
        # Then:
        with self.assertRaises(TeacherNotFound) as exception:
            uut.getBasicTeacherDataByPesel('123')

    # should not raise any exceptions when one row with 7 columns fetched
    def test_getBasicTeacherDataByPesel_shouldNot_raiseExceptions_when_oneRow(self):
        # Given:
        uut = TeacherService(self.session)

        # When:
        expected_value = [ ("1", "TEST", "", "", "", "", "" ,"", "") ]
        self.session.query.return_value = expected_value
        student = uut.getBasicTeacherDataByPesel('123')

        # Then:
        assert student.name == "TEST"


    ### getTaughtSubjects

    def test_getTaughtSubjects_shouldReturnAList(self):
        # Given:
        uut = TeacherService(self.session)

        # When:
        expected_value = [["A"], ["B"], ["C"]]
        self.session.query.return_value = expected_value
        subjects = uut.getTaughtSubjects('123')

        # Then:
        assert subjects == expected_value


    ### getAllTeachers

    def test_getAllTeachers_shouldReturn_anEmptyList_when_noRowsFetched(self):
        # Given:
        uut = TeacherService(self.session)

        # When:
        expected_value = []
        self.session.query.return_value = expected_value
        teachers = uut.getAllTeachers()

        # Then:
        assert teachers == expected_value

    def test_getAllTeachers_shouldAlwaysReturn_aTeacherList(self):
        # Given:
        uut = TeacherService(self.session)

        # When:
        rows = [[123, "", "", "", "", "", ""]]
        self.session.query.return_value = rows
        teachers = uut.getAllTeachers()

        # Then:
        assert type(teachers[0]) == Teacher
        assert teachers[0].id == 123


    ### deleteTeacher

    def test_deleteTeacher_shouldThrow_TeacherNotFound_when_teacherDoesNotExist(self):
        # setup mocks
        self.session.reset_mock()
        CursorMock = Mock()
        CursorMock.return_value.execute = Mock(side_effect=Exception("DB error"))
        
        # Given:
        uut = TeacherService(self.session)

        # When:
        self.session.getCursor.return_value = CursorMock()
        with self.assertRaises(TeacherNotFound) as exception:
            uut.deleteTeacher('123')

        # Then:
        assert not self.session.commitChange.called


    def test_deleteTeacher_should_deleteTheTeacher_and_commitTheChange(self):
        # setup mocks
        self.session.reset_mock()
        CursorMock = Mock()
        
        # Given:
        uut = TeacherService(self.session)

        # When:
        self.session.getCursor.return_value = CursorMock()
        uut.deleteTeacher('123')

        # Then:
        self.session.getCursor.assert_called_once()
        CursorMock.return_value.execute.assert_called_once()
        self.session.commitChange.assert_called_once()
