from PyQt5.QtWidgets import QWidget, QMainWindow
from start_view import StartView
from admin_view import AdminView
from student_view import StudentView
from teacher_view import TeacherView

class NavigationController:
    def __init__(self, mainWindow: QMainWindow):
        self.mainWindow = mainWindow
        mainWindow.setCentralWidget(StartView(self))

    def openView(self, view):
        self.mainWindow.setCentralWidget(view)

    def navigateToStart(self):
        self.openView(StartView(self))

    def navigateToAdminPanel(self):
        self.openView(AdminView(self))

    def navigateToStudentPanel(self):
        self.openView(StudentView(self))

    def navigateToTeacherPanel(self):
        self.openView(TeacherView(self))