from db_session import DbSession 
from login_dialog import LoginDialog
from error_box import ErrorBox
from strings import invalidPasswordOrIdMessage

class AuthService:
    def __init__(self):
        self.id = None

    def askForPasswordAndAuth(self, username, requireId = False, idView=None) -> DbSession | None:
        dialog = LoginDialog(requireId)
        dialog.exec()

        dbSession = DbSession(username, dialog.passwordFiled.text())

        if not dbSession.isOpen:
            ErrorBox(invalidPasswordOrIdMessage).exec()
            return None

        self.id = dialog.idField.text()

        if requireId:
            data = dbSession.query(f"SELECT * FROM system.{idView} WHERE \"pesel\" = '{self.id}'")

            if len(data) != 1:
                dbSession.close()
                ErrorBox(invalidPasswordOrIdMessage).exec()
                return None

        return dbSession