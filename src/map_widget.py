from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class MapWidget(QWidget):
    def __init__(self, data: dict):
        super().__init__()

        layout = QVBoxLayout()
        for key in data:
            layout.addWidget(QLabel(str(key) + ": " + str(data[key])))

        self.setLayout(layout)
