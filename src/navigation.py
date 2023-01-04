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

    def openStartView(self):
        self.openView(StartView(self))

    def openAdminView(self):
        self.openView(AdminView(self))

    def openStudentView(self):
        self.openView(StudentView(self))

    def openTeacherView(self):
        self.openView(TeacherView(self))