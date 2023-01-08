import cx_Oracle

import config

class DbSession:
    def __init__(self, username, password):
        try:
            self.connection = cx_Oracle.connect(username, password,
                                                config.dsn, encoding=config.encoding)
            self.isOpen = True

        except cx_Oracle.Error as error:
            print(error)
            self.isOpen = False

    def query(self, query: str):
        if self.isOpen:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query)
            except cx_Oracle.Error as error:
                print(error)
                return []
            return cursor.fetchall()

    def close(self):
        self.isOpen = False
        self.connection.close()

    