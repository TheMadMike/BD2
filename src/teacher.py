class Teacher:
    id : str
    name : str
    surname : str
    telephone : str
    email : str
    address : str
    birthday : str
    pesel : str
    startDate : str
    maxWorkHoursWeekly : int
    availableHoursWeekly : int

    def __init__(self, name="", surname="", telephone="", email="", address="", birthday="", pesel="", startDate="", maxWorkHoursWeekly=0, availableHoursWeekly=0):
        self.name = name
        self.surname = surname
        self.telephone = telephone
        self.email = email
        self.address = address
        self.birthday = birthday
        self.pesel = pesel
        self.startDate = startDate
        self.availableHoursWeekly = availableHoursWeekly
        self.maxWorkHoursWeekly = maxWorkHoursWeekly
