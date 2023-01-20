class StudentNotFound(Exception):
    def __init__(self, pesel):
        super().__init__(f"Unable to find student with PESEL: {pesel}")
        self.pesel = pesel

class TeacherNotFound(Exception):
    def __init__(self, pesel):
        super().__init__(f"Unable to find teacher with PESEL: {pesel}")