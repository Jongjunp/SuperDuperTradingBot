import sqlite3
import numpy as np
import tensorflow as tf


# 강화학습 환경 class
class Env:
    def __init__(self):
        self.money = Finance()              # 현재 보유 자산
        self.control_money = Finance()      # 대조군 자산

        self.date = 0           # 경과일
        self.stock_price = []   # 현재 주식 가격

        self.data = Data()      # 데이터 로딩 객체
        self.obs = None         # 관측 데이터

    # 주식 매도 함수 code: 주식 코드
    def sell(self, code, finance):
        # 주식을 1주 이상 보유하고 있는지 확인
        if finance.stock[code] > 0:
            try:
                # 보유 주식을 한 주 차감하고 잔고에 그 가격만큼을 합산.
                finance.change_stock(code, -1)
                finance.change_balance(self.stock_price[code])
            except Exception as e:
                print(e)

    # 주식 매수 함수 code: 주식 코드
    def buy(self, code, finance):
        if finance.balance >= self.stock_price[code]:
            try:
                # 보유 주식을 한 주 늘리고 잔고에 주식 가격만큼 차감.
                finance.change_stock(code, 1)
                finance.change_balance(-self.stock_price[code])
            except Exception as e:
                print(e)

    # 스텝 넘기는 함수 | action : 행동(list)
    def next_step(self, action):
        # 행동 별로 매도, 매수 함수 호출
        for count, act in enumerate(action):
            if act == 0:
                self.sell(count, self.money)
            elif act == 1:
                self.buy(count, self.money)

        # 현재 데이터 받아오기
        done, obs = self.data.load_data()
        self.stock_price = self.data.load_price()
        reward = self.get_reward()

        # 365일 경과시 에피소드 종료
        done = True if self.date >= 365 and done is True else False

        # 환경, reward, 완료 여부 반환
        return obs, reward, done

    # Reward 반환 함수
    def get_reward(self):
        return None

    # episode 종료 시 reset 함수
    def reset(self):
        return


class Finance:
    def __init__(self):
        self.balance = 1000000      # 현재 잔고
        self.stock = []             # 현재 주식 보유량
        self.estimated = self.balance

    # 잔고 보유량 변동
    def change_balance(self, amount):
        self.balance += amount
        return

    # 주식 보유량 변동
    def change_stock(self, code, amount):
        self.stock[code] += amount
        return

    # 현재 예상 자산 예측
    def estimate_account(self, price):
        sum_stock = 0
        for count, stock in enumerate(self.stock):
            sum_stock += stock * price[count]

        self.estimated = self.balance + sum_stock
        return sum_stock


# Data load class
class Data:
    def __init__(self):
        self.trading_amount = []

        self.dataset = self.load_initial_data()
        self.batch = None
        self.next_batch = self.load_data()
        self.count = 0

    # 초기 데이터 불러오기 함수
    def load_initial_data(self):
        con = sqlite3.connect("D:\SuperDuperTradingBot\data\stock.db")     # 데이터베이스 조회
        cursor = con.cursor()
        cursor.execute("SELECT * FROM price")
        temp_data = cursor.fetchone()

        # 데이터 베이스에서 데이터 불러오기
        initial_data = []
        while temp_data is not None:
            inner_lst = []
            code = temp_data[0]
            while temp_data is not None and temp_data[0] == code:
                inner_lst.append(temp_data)
                temp_data = cursor.fetchone()
            initial_data.append(inner_lst)
            temp_data = cursor.fetchone()

        # 불러온 데이터로 가공해서 batch 형식으로 만들기
        dataset = []
        for element in initial_data:
            element = np.array(element, np.int)[:, 2:]
            self.trading_amount.append(np.max(element[:, 4:]))
            element = tf.data.Dataset.from_tensor_slices(element).window(120, 1, 1, False)
            dataset.append(iter(element.flat_map(lambda x: x.batch(120, False))))

        return dataset

    # 학습 데이터 불러오기 함수 | stock_data : 현재 환경 [0] : 현재 예상 자산, [1] 주식 가격, [2] 주식 수
    def load_data(self, finance):
        # 배치 불러오기
        def load_batch():
            try:
                return False, next(self.dataset[self.count]).numpy()
            except StopIteration:
                self.count += 1
                return True, next(self.dataset[self.count]).numpy()

        done, self.batch = self.next_batch
        self.next_batch = load_batch()

        output = np.hstack(((self.batch[:, :4] * np.full((120, 4), 1 / np.max(self.batch[:, :3]))),
                            self.batch[:, 4:] * np.full((120, 1), 1 / self.trading_amount[self.count])))

        return done, np.vstack(output, (finance[1] * finance[2]) / finance[0], 0., 0., 0.)

    # 현재 가격 불러오기
    def load_price(self):
        return self.batch[119, 4]


# 대조군 class
class ControlAgent:
    def __init__(self):
        pass

    def get_action(self):
        pass

