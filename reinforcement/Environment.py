import gym
import datetime

from reinforcement.Parameter import *


class Env:
    def __init__(self):
        # 현재 잔고
        self.balance = 1000000

        # 예상 이익, 누적 이익
        self.accum_benefit = 0
        self.pred_benefit = 0

        # 보유 현황
        # 1종목으로 테스트중
        self.stock = [0]

        # 현재 날짜
        self.date = START_DATE

        # 주식 데이터
        self.stock_data = []

    # 데이터 받아오기
    def load_data(self, date):
        pass

    # 주식 매도
    def sell(self, code):
        pass

    # 주식 매수
    def buy(self, code):
        pass

    # 날짜 넘기기
    def next_step(self):
        pass
