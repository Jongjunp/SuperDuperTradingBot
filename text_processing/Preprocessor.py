import sqlite3
import pandas as pd
import tensorflow
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

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
        data_result = self.dbOpen()
        #null character 제거
        data_result = data_result.dropna(how='any')
        data_result['document'] = data_result['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")

        #불용어 설정
        stopwords = [#설정하기]

        preprocessed_data = []
        for sentence in data_result:
            temp_sentence = []
            temp_sentence = okt.morphs(sentence, stem=True)
            temp_sentence = [word for word in temp_sentence if not word in stopwords]
            preprocessed_data.append(temp_sentence)

        max_words = 20000
        tokenizer = Tokenizer(num_words = max_words)
        tokenizer.fit_on_texts(preprocessed_data)
        preprocessed_data = tokenizer.texts_to_sequences(preprocessed_data)

        max_len = 1000
        preprocessed_data = pad_sequences(preprocessed_data, maxlen=max_len)






