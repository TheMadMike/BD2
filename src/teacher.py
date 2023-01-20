class Teacher:
    id : str
    name : str
    surname : str
    pesel : str
    startDate : str
    maxWorkHoursWeekly : int
    availableHoursWeekly : int

    def __init__(self, name="", surname="", pesel="", startDate="", maxWorkHoursWeekly=0, availableHoursWeekly=0):
        self.name = name
        self.surname = surname
        self.pesel = pesel
        self.startDate = startDate
        self.availableHoursWeekly = availableHoursWeekly
        self.maxWorkHoursWeekly = maxWorkHoursWeekly
