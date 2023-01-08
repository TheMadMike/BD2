from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QLabel, QLineEdit

from strings import loginDialogTitle, loginDialogIdText, loginDialogPasswordText

class LoginDialog(QDialog):
    def __init__(self, requirePESEL):
        super().__init__()

        self.setWindowTitle(loginDialogTitle)

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.peselField = QLineEdit()
        if requirePESEL:
            self.layout.addWidget(QLabel(loginDialogIdText))
            self.layout.addWidget(self.peselField)            

        self.passwordFiled = QLineEdit()
        self.passwordFiled.setEchoMode(QLineEdit.Password)

        self.layout.addWidget(QLabel(loginDialogPasswordText))        
        self.layout.addWidget(self.passwordFiled)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

