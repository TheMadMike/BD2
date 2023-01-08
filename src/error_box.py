from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QLabel, QLineEdit

from strings import errorDialogTitle

class ErrorBox(QDialog):
    def __init__(self, message):
        super().__init__()

        self.setWindowTitle(errorDialogTitle)

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        msgLabel = QLabel(message)
        msgLabel.setStyleSheet("color: red")

        self.layout.addWidget(msgLabel)
        self.layout.addWidget(self.buttonBox)   
        self.setLayout(self.layout)
