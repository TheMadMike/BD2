from PyQt5.QtWidgets import QWidget, QMainWindow

from start_view import StartView
from admin_view import AdminView
from student_view import StudentView
from teacher_view import TeacherView

from db_session import DbSession
from strings import invalidPasswordOrIdMessage

from auth_service import AuthService

class NavigationController:
    def __init__(self, mainWindow: QMainWindow):
        self.mainWindow = mainWindow
        self.dbSession = None
        self.authService = AuthService()
        mainWindow.setCentralWidget(StartView(self))


    def openView(self, view):
        self.mainWindow.setCentralWidget(view)


    def navigateToStart(self):
        if self.dbSession is not None and self.dbSession.isOpen:
            self.dbSession.close()

        self.openView(StartView(self))
    

    def navigateToAdminPanel(self):
        self.dbSession = self.authService.askForPasswordAndAuth("sekretariat")

        if self.dbSession is not None:
            self.openView(AdminView(self))


    def navigateToStudentPanel(self):
        self.dbSession = self.authService.askForPasswordAndAuth("uczen", True, "v_uczniowie")

        if self.dbSession is not None:
            self.openView(StudentView(self, self.authService.pesel))


    def navigateToTeacherPanel(self):
        self.dbSession = self.authService.askForPasswordAndAuth("nauczyciel", True, "dane_osobowe")

        if self.dbSession is not None:
            self.openView(TeacherView(self))
    
    