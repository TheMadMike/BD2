# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

# TODO: view layer design
# app = QApplication([])
# window = QWidget()
# layout = QVBoxLayout()
# layout.addWidget(QPushButton('TEST'))
# window.setLayout(layout)
# window.show()
# app.exec()

# TODO: implement actual connection and SQL queries
import cx_Oracle

import config as cfg

try:
    # create a connection to the Oracle Database
    with cx_Oracle.connect(cfg.username,
                        cfg.password,
                        cfg.dsn,
                        encoding=cfg.encoding) as connection:
        print(connection)

except cx_Oracle.Error as error:
    print(error)

