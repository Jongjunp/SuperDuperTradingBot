from bs4 import BeautifulSoup
import requests
import datetime
import pandas as pd
import sqlite3
import csv


class Scrab:
    # 네이버 금융 일봉 URL (사이에 종목코드 입력)
    first_url = "https://fchart.stock.naver.com/sise.nhn?symbol="
    last_url = "&timeframe=day&count=5000&requestType=0"

    def __init__(self):
        self.connection = sqlite3.connect("data/stock.db")
        print('hello')

    def scrab(self, code: str, name: str) -> list:
        url = self.first_url + code + self.last_url
        data_request = requests.get(url)                        # 데이터 요청

        soup = BeautifulSoup(data_request.text, "html.parser")  # html 파싱
        keys = soup.select("item")                              # 일봉 데이터 가져오기

        data = []
        for key in keys:
            # 적절하게 데이터 가공
            temp = str(key).split('|')
            temp[0] = temp[0][12:]
            temp[5] = temp[5][:-9]

            temp = list(map(int, temp))
            # [날짜, 시가, 고가, 저가, 종가, 거래량]
            data.append(temp)
        return data

    def scrab_all(self):
        cur = self.connection.cursor()

        # 테이블 만들기. 귀찮아서 오류로 땜빵.
        cur.execute("create table price (code text, stock_date text,"
                    "start_price int, high_price int, low_price int, end_price int, trade_amount int,"
                    "primary key(code, stock_date))")

        code_data = open('data/code.csv', 'r', encoding='utf-8')
        reader = csv.reader(code_data)

        a = 0

        for count, line in enumerate(reader):
            print(f"{count}/2310 {line[1]}\t|", end='')
            price_data = self.scrab(line[0], line[1])

            inner_count = 0
            for price in price_data:
                inner_count += 1
                if inner_count > len(price_data) / 10:
                    inner_count = 0
                    print('=', end='')

                cur.execute("insert into price values (?, ?, ?, ?, ?, ?, ?)",
                            (line[0], price[0], price[1], price[2], price[3], price[4], price[5]))

                self.connection.commit()

            print()

        return
