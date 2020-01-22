import tensorflow as tf
import tensorboard

from reinforcement.Model import PPOModel
from reinforcement.Parameter import *
from reinforcement.Environment import Env


class Agent:
    def __init__(self):
        self.model = PPOModel()     # 모델
        self.env = Env()            # 환경
        self.reward = []            # 이익
        self.observation = self.env.reset()
        self.val = False            # Validating

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
                self.env.reset()

        obs, action, pred, reward = np.array(batch[0]), np.array(batch[1]), np.array(
            batch[2]), np.reshape(np.array(batch[3]), (len(batch[3]), 1))

        pred = np.reshape(pred, (pred.shape[0], pred.shape[2]))
        return obs, action, pred, reward

    def transform_reward(self):
        if self.val is True:
            pass

    # GAE 이용 Advantage 계산
    def calculate_advantage(self):
        pass

    # 모델 학습 함수
    def train(self):
        while self.env.episode < EPISODE:
            obs, action, pred, reward = self.get_batch()
            obs, action, pred, reward = obs[:BUFFER_SIZE], action[:BUFFER_SIZE], pred[:BUFFER_SIZE], reward[:BUFFER_SIZE]
            old_prediction = pred
            pred_values = self.model.critic.predict(obs)

            advantage = reward - pred_values

            actor_loss = self.model.actor.fit([obs, advantage, old_prediction], [action],
                                              batch_size=BATCH_SIZE, shuffle=True, epochs=K_EPOCH)
            critic_loss = self.model.critic.fit([obs], [reward], batch_size=BATCH_SIZE, shuffle=True, epochs=K_EPOCH)

        return
