from reinforcement.Agent import Agent
import tensorflow as tf
from reinforcement.Scrab import Scrab

if __name__ == "__main__":
    print("1. 종목 스크랩\n"
          "2. 모델 테스트\n")

    ans = input()

    if ans is "1":
        tmp = Scrab()
        tmp.scrab_all()


