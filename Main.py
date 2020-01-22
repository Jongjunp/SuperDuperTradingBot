from reinforcement.Agent import Agent
import tensorflow as tf
from reinforcement.Scrab import Scrab
from reinforcement.Environment import Env

if __name__ == "__main__":
    print("1. 종목 스크랩\n"
          "2. 모델 테스트\n")

    ans = input()

    if ans is "1":
        tmp = Scrab()
        tmp.scrab_all()

    elif ans is "2":
        a = Agent()
        a.train()

    elif ans is "3":
        a = Env()
        a.load_data()
        print(a.make_data())


