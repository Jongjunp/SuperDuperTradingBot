import datetime
import numpy as np
import tensorflow as tf
import sqlite3
import math

from reinforcement.Parameter import *


class Env:
    def __init__(self):
        # 현재 잔고
        self.balance = 1000000
        self.compute_balance = 1000000
        self.pred_account = 1000000
        self.previous_account = 1000000
        self.benefit = 0

        # 보유 현황
        # 1종목으로 테스트중
        self.stock = 0
        self.stock_value = 0
        self.stock_count = 0

        # 현재 날짜
        self.date = 0

        # 주식 데이터
        self.trading_amount = []
        self.dataset = self.load_data()

        # 처음 데이터
        self.episode = 0
        self.batch = np.zeros((5, 60))

        # history
        self.balance_history = []
        self.value_history = []

    # 데이터 받아오기
    def load_data(self):
        con = sqlite3.connect("data/stock.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM price")

        tmp = cursor.fetchone()
        lst = []
        inner_lst = []
        dataset = []

        while tmp is not None:
            code = tmp[0]
            while tmp is not None and tmp[0] == code:
                inner_lst.append(tmp)
                tmp = cursor.fetchone()
            lst.append(inner_lst)
            inner_lst = []
            tmp = cursor.fetchone()

        for element in lst:
            element = np.array(element, np.int)[:, 2:]
            self.trading_amount.append(np.max(element[:, 4:]))
            element = tf.data.Dataset.from_tensor_slices(element).window(STATE, 1, 1, True)
            dataset.append(iter(element.flat_map(lambda x: x.batch(STATE, True))))

        return dataset

    # 주식 매도
    def sell(self, code):
        tmp = 1
        while True:
            if self.stock < tmp:
                self.balance += round(self.stock * self.stock_value * .995, 0)
                self.stock = 0
                self.compute_balance = self.balance
                break
            elif self.pred_account * .1 < self.stock_value * tmp:
                self.stock -= tmp
                self.compute_balance = self.balance + self.stock * self.stock_value * .995
                self.balance += round(self.stock_value * tmp * .995, 0)
                break
            else:
                tmp += 1
        return

    # 주식 매수
    def buy(self, code):
        done = False
        tmp = 1
        while not done:
            if self.balance < self.stock_value * tmp:
                self.stock += tmp - 1
                self.balance -= self.stock_value * (tmp - 1)
                done = True
            elif self.pred_account * .1 < self.stock_value * tmp:
                self.stock += tmp
                self.balance -= self.stock_value * tmp
                done = True
            else:
                tmp += 1
        return

    # 날짜 넘기기
    def next_step(self, action):
        self.date += 1

        if action == 0:
            self.sell(0)
        elif action == 1:
            self.buy(0)

        obs = self.make_data()
        reward = (self.compute_balance - self.previous_account) / 10000
        self.previous_account = self.compute_balance
        self.pred_account = self.balance + (self.stock * self.stock_value * .995)

        done = True if self.date > 365 else False

        if done:
            print(self.balance, self.stock, self.pred_account, reward, sep='\t')
        if self.episode == EPISODE:
            self.value_history.append(self.stock_value)
            self.balance_history.append(self.pred_account)
        return obs, reward, done

    # 환경 초기화
    def reset(self):
        self.episode += 1
        print("reset", self.episode)
        # 현재 잔고
        self.balance = 1000000
        self.compute_balance = 1000000
        self.pred_account = 1000000
        self.previous_account = 1000000
        self.benefit = 0

        # 보유 현황
        # 1종목으로 테스트중
        self.stock = 0
        self.stock_value = 0
        self.stock_count = 0

        # 현재 날짜
        self.date = 0
        return self.make_data()

    # 데이터 만들기
    def make_data(self):
        def load_batch():
            try:
                return next(self.dataset[self.stock_count]).numpy()
            except StopIteration:
                self.stock_count += 1
                self.reset()
                return next(self.dataset[self.stock_count]).numpy()

        self.batch = load_batch()
        self.stock_value = self.batch[29, 0]
        self.batch = np.hstack(((self.batch[:, :4] * np.full((30, 4), 1/np.max(self.batch[:, :3]))),
                               self.batch[:, 4:] * np.full((30, 1), 1/self.trading_amount[self.stock_count])))

        return np.vstack((self.batch,
                          (self.balance/self.pred_account, self.stock*self.stock_value/self.pred_account, 0., 0., 0.)))
