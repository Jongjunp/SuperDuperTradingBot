import tensorflow as tf
import tensorboard
import matplotlib.pyplot as plt
import random
from PyQt5 import uic, QtCore

from old_model.Model import PPOModel
from old_model.Parameter import *
from old_model.Environment import Env


class Agent(QtCore.QThread):
    done_interval = QtCore.pyqtSignal(list)
    episode_start = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.model = PPOModel()     # 모델
        self.env = Env()            # 환경
        self.reward = []            # 이익
        self.val = False            # Validating
        self.transition = []        # Buffer Data

    # 배치 생성 함수
    def get_batch(self):
        batch = [[], [], [], []]

        tmp_batch = [[], [], []]
        while len(batch[0]) < BUFFER_SIZE:
            action, action_matrix, pred_action = self.model.get_action(self.observation)
            observation, reward, done = self.env.next_step(action)
            self.reward.append(reward)

            tmp_batch[0].append(self.observation)
            tmp_batch[1].append(action_matrix)
            tmp_batch[2].append(pred_action)
            self.observation = observation

            if done:
                self.transform_reward()

                for i in range(len(tmp_batch[0])):
                    obs, action, pred = tmp_batch[0][i], tmp_batch[1][i], tmp_batch[2][i]
                    r = self.reward[i]
                    batch[0].append(obs)
                    batch[1].append(action)
                    batch[2].append(pred)
                    batch[3].append(r)
                self.env.reset()

                for i in range(4):
                    random.shuffle(batch[i])
        obs, action, pred, reward = np.array(batch[0]), np.array(batch[1]), np.array(
            batch[2]), np.reshape(np.array(batch[3]), (len(batch[3]), 1))

        pred = np.reshape(pred, (pred.shape[0], pred.shape[2]))
        return obs, action, pred, reward

    # 배치 만드는 함수
    def make_batch(self):
        # s, a, r, s', pr(a), done 리스트 생성
        s_lst, a_lst, r_lst, s_prime_lst, prob_a_lst, done_lst = [], [], [], [], [], []

        # Buffer 리스트 안에 있는 데이터에 대하여 리스트 추가
        for item in self.transition:
            s, a, r, s_prime, prob_a, done = item

            s_lst.append(s)
            a_lst.append(a)
            r_lst.append(r)
            s_prime_lst.append(s_prime)
            prob_a_lst.append(prob_a)
            done_lst.append(done)

        # numpy array 로 변환후 반환
        return np.array(s_lst), np.array(a_lst).reshape(-1, 3), \
               np.array(r_lst), np.array(s_prime_lst), np.array(done_lst), np.array(prob_a_lst).reshape(-1, 3)

    def train(self):
        # 배치 데이터 받아오기
        s, a, r, s_prime, done, prob_a = self.make_batch()

        td_target = r + DISCOUNT * self.model.critic.predict(s_prime) * done
        delta = td_target - self.model.critic.predict(s)

        advantage_lst = []
        advantage = .0

        for delta_t in delta[::-1]:
            advantage = DISCOUNT * LMBDA * advantage + delta_t[0]
            advantage_lst.append([advantage])

        advantage_lst.reverse()
        advantage = np.array(advantage_lst)
        actor_loss = self.model.actor.fit([s, advantage, prob_a], [a], verbose=False,
                                          batch_size=BATCH_SIZE, shuffle=True, epochs=K_EPOCH)
        critic_loss = self.model.critic.fit([s], [r], batch_size=BATCH_SIZE, shuffle=True, epochs=K_EPOCH, verbose=False)

    def run(self):
        score = .0
        print_interval = 20

        # Episode 만큼 돌림
        for episode in range(EPISODE):
            # 환경 초기화
            s = self.env.reset()
            done = False
            self.episode_start.emit(episode+1)

            # 에피소드가 끝나기 전까지
            while not done:
                # 학습 데이터 수집
                for t in range(T_HORIZON):
                    # Actor로 부터 행동 추측 후 다음 스텝
                    action, action_matrix, predict_action = self.model.get_action(s)
                    s_prime, r, done = self.env.next_step(action)

                    # Buffer 리스트에 추가
                    self.transition.append((s, action_matrix, r, s_prime, predict_action, done))
                    if len(self.transition) > BUFFER_SIZE:
                        self.transition.pop(0)
                    s = s_prime

                    score += r
                    if done:
                        break

                env_data = [self.env.compute_balance, self.env.stock]
                self.done_interval.emit(env_data)

                self.train()
