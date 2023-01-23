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

    # TODO: SQL injections
    def query(self, query: str, dml = False):
        if self.isOpen:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query)
            except cx_Oracle.Error as error:
                print(error)
                return []
            return cursor.fetchall()

    def getCursor(self):
        if self.isOpen:
            return self.connection.cursor()

        return None
    
    def commitChange(self):
        if self.isOpen:
            self.connection.commit()

    def close(self):
        self.isOpen = False
        self.connection.close()

    