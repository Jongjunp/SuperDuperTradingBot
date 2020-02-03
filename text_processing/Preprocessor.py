import sqlite3

class Preprocessor:
    def __init__(self,DBloc,TableName):
        self.DBloc = DBloc
        self.TableName = TableName
        self.connection = sqlite3.connect(DBloc)

    def dbOpen(self):
        cur = self.connection.cursor()
        cur.execute()
