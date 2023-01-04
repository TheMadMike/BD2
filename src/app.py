# University project on databases
# Copyright 2022 (c) Michał Gibas & Patryk Polkowski

from PyQt5.QtWidgets import QApplication, QMainWindow
from main_window import MainWindow

app = QApplication([])

window = MainWindow()
window.show()

app.exec()

# TODO: implement actual connection and SQL queries
# import cx_Oracle

# import config as cfg

# try:
#     # create a connection to the Oracle Database
#     with cx_Oracle.connect(cfg.username,
#                         cfg.password,
#                         cfg.dsn,
#                         encoding=cfg.encoding) as connection:
#         cursor = connection.cursor()
#         cursor.execute("SELECT * FROM dane_osobowe WHERE nazwisko = 'Gibas'")
#         rows = cursor.fetchall()

#         for row in rows:
#             print(row)


# except cx_Oracle.Error as error:
#     print(error)

