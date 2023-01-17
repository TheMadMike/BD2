from db_session import DbSession 
from login_dialog import LoginDialog
from error_box import ErrorBox
from strings import invalidPasswordOrIdMessage

class AuthService:
    def __init__(self):
        self.pesel = None

    def askForPasswordAndAuth(self, username, requirePesel = False, peselView=None) -> DbSession | None:
        dialog = LoginDialog(requirePesel)
        if dialog.exec():
        
            dbSession = DbSession(username, dialog.passwordFiled.text())

            if not dbSession.isOpen:
                ErrorBox(invalidPasswordOrIdMessage).exec()
                return None

            self.pesel = dialog.peselField.text()

            if requirePesel:
                data = dbSession.query(f"SELECT * FROM system.{peselView} WHERE \"pesel\" = '{self.pesel}'")

                if len(data) != 1:
                    dbSession.close()
                    ErrorBox(invalidPasswordOrIdMessage).exec()
                    return None

            return dbSession
        
        return None