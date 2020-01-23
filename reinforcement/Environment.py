import gym
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
        self.initial_balance = 1000000
        self.pred_account = 1000000

        # 예상 이익, 누적 이익
        self.accum_benefit = 0
        self.pred_benefit = 0

        # 보유 현황
        # 1종목으로 테스트중
        self.stock = 0
        self.stock_value = 0

        # 현재 날짜
        self.date = 29

        # 주식 데이터
        self.dataset = []
        self.now_value = 0

        # 처음 데이터
        self.initial_env = None
        self.episode = 0
        self.batch = np.zeros((5, 60))
        self.tmp = None
        self.load_data()

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

        while tmp is not None:
            code = tmp[0]
            if tmp[1] == '20091007':
                while tmp is not None and tmp[0] == code:
                    lst.append(tmp)
                    tmp = cursor.fetchone()
                self.dataset.append(lst)
                lst = []
            tmp = cursor.fetchone()

        self.tmp = np.array(self.dataset[3], dtype=np.float)[:, 2::1]
        return

    # 주식 매도
    def sell(self, code):
        if self.stock > 0:
            self.stock -= 1
            self.balance += round(self.stock_value * .999, 0)
        return

    # 주식 매수
    def buy(self, code):
        if self.balance > self.stock_value:
            self.stock += 1
            self.balance -= self.stock_value
        return

    # 날짜 넘기기
    def next_step(self, action):
        self.date += 1

        if action == 0:
            self.sell(0)
            print("Action: Sell", end='\t')
        elif action == 1:
            self.buy(0)
            print("Action: Buy", end='\t\t')
        else:
            print("Action: Hold", end='\t')

        obs = self.make_data()
        tmp = self.balance + round(self.stock * self.batch[28, 3] * .999)
        reward = tmp/self.pred_account
        self.pred_account = tmp
        self.pred_benefit = self.pred_account - self.initial_balance

        done = True if self.date > 500 else False
        print(self.balance, self.stock, self.pred_account, reward, sep='\t')
        if self.episode == 20:
            self.value_history.append(self.stock_value)
            self.balance_history.append(self.pred_account)
        return obs, reward, done

    # 환경 초기화
    def reset(self):
        self.episode += 1
        tmp = self.episode
        self.__init__()
        self.episode = tmp
        print("reset", self.episode)
        return self.make_data()

    # 데이터 만들기
    def make_data(self):
        # 처음 시작할 때 batch 생성
        if self.date == 29:
            self.batch = self.tmp[0:30:1, :]

        # 이전 데이터 밀어내기
        self.stock_value = self.batch[29, 0]
        self.batch = np.vstack((self.batch[1:, :], self.tmp[self.date, :]))

        return np.vstack((np.hstack((self.batch[:, :3] * np.full((30, 3), 1/self.batch[29, 1]),
                          self.batch[:, 3:] * np.full((30, 1), 1/72800000*3))),
                          np.array([self.balance/self.pred_account, self.stock_value*self.stock/self.pred_account, 0., 0., 0.])))
