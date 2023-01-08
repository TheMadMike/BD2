from unittest.mock import patch, call
from unittest import TestCase
from auth_service import AuthService
import pytest

@patch('auth_service.DbSession')
@patch('auth_service.ErrorBox')
@patch('auth_service.LoginDialog')
class TestAuthService(TestCase):
    def test_authService_always_asksForPassword(self, LoginDialogMock, ErrorBoxMock, DbSessionMock):
        # Given:
        uut = AuthService()

        # When:
        # Scenario 1: ask for password only
        uut.askForPasswordAndAuth('testuser')

        # Then:
        # Expect login dialog created once and exec called
        LoginDialogMock.assert_called_once()
        LoginDialogMock.return_value.exec.assert_called_once()

        # When:
        # Scenario 2: ask for both password and id
        uut.askForPasswordAndAuth('testuser', True)

        # Then:
        # Expect login dialog created twice and exec called twice
        assert LoginDialogMock.return_value.exec.call_count == 2
        assert LoginDialogMock.call_count == 2


    def test_authService_runs_SqlQuery_when_idRequired(self, LoginDialogMock, ErrorBoxMock, DbSessionMock):
        # Setup mocks
        # setup fake ID value
        LoginDialogMock.return_value.idField.text.return_value = '123'
        # setup DbSession.isOpen
        DbSessionMock.return_value.isOpen = True

        # Given:
        uut = AuthService()

        # When:
        # asked for password and login
        uut.askForPasswordAndAuth('test', True, 'testView')
        
        # Then:
        # DbSession object created
        DbSessionMock.assert_called_once()
        # DbSession.query called
        DbSessionMock.return_value.query.assert_called_once_with("SELECT * FROM system.testView WHERE \"pesel\" = '123'")