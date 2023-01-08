class Student:
    id : str
    name : str
    surname : str
    telephone : str
    email : str
    address : str
    birthday : str
    pesel : str
    startDate : str
    classId : str
    major : str

    def __init__(self, name="", surname="", telephone="", email="", address="", birthday="", pesel="", startDate="", classId=""):
        self.name = name
        self.surname = surname
        self.telephone = telephone
        self.email = email
        self.address = address
        self.birthday = birthday
        self.pesel = pesel
        self.startDate = startDate
        self.classId = classId