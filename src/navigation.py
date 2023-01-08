from PyQt5.QtWidgets import QWidget, QMainWindow

from start_view import StartView
from admin_view import AdminView
from student_view import StudentView
from teacher_view import TeacherView
from login_dialog import LoginDialog
from error_box import ErrorBox

from db_session import DbSession
from strings import invalidPasswordOrIdMessage

# TODO: delegate authentication to another class/set of classes
class NavigationController:
    def __init__(self, mainWindow: QMainWindow):
        self.mainWindow = mainWindow
        self.dbSession = None
        mainWindow.setCentralWidget(StartView(self))

    def openView(self, view):
        self.mainWindow.setCentralWidget(view)

    def navigateToStart(self):
        if self.dbSession is not None and self.dbSession.isOpen:
            self.dbSession.close()

        self.openView(StartView(self))

    def navigateToAdminPanel(self):
        dialog = LoginDialog(False)
        dialog.exec()
        self.openNewDbSession("system", dialog.passwordFiled.text())

        if self.dbSession.isOpen:
            self.openView(AdminView(self))
        else:
            ErrorBox(invalidPasswordOrIdMessage).exec()

    def navigateToStudentPanel(self):
        dialog = LoginDialog(True)
        dialog.exec()
        self.openNewDbSession("uczen", dialog.passwordFiled.text())

        if self.dbSession.isOpen:
            self.openView(StudentView(self))
        else:
            ErrorBox(invalidPasswordOrIdMessage).exec()

    def navigateToTeacherPanel(self):
        dialog = LoginDialog(True)
        dialog.exec()
        self.openNewDbSession("nauczyciel", dialog.passwordFiled.text())

        if self.dbSession.isOpen:
            self.openView(TeacherView(self))
        else:
            ErrorBox(invalidPasswordOrIdMessage).exec()

    def openNewDbSession(self, username, password):
        if self.dbSession is not None and self.dbSession.isOpen:
            self.dbSession.close()

        self.dbSession = DbSession(username, password)
    