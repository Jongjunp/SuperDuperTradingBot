import sqlite3
import pandas as pd

class Preprocessor:
    def __init__(self,DBloc,TableName):
        self.DBloc = DBloc
        self.TableName = TableName
        self.connection = sqlite3.connect(DBloc)

    def dbOpen(self):
        cur = self.connection.cursor()
        dataList = cur.execute("SELECT * From "+ self.TableName)
        cols = [column[0]for column in dataList.description]
        data_result = pd.DataFrame.from_records(data=dataList.fetchall(),columns=cols)

        return data_result

    def CutWords(self):
        datalist = self.dbOpen()



