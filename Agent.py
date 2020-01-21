import tensorflow as tf
import tensorflow.keras as keras
import tensorflow_probability as tfp
import numpy as np
import pydot

from tensorflow.keras.utils import plot_model
from Model import PPOModel


class Agent:
    def __init__(self, state_size, action_size):
        # Parameters
        self.lr = .0005
        self.discount = .95
        self.lmbda = .95
        self.eps_clip = .1
        self.K_epoch = 3
        self.T_horizon = 20

        # action, state size
        self.action_size = 3
        self.state_size = (5, 60, )

        self.data = []

        self.model = PPOModel(self.action_size, self.state_size)

    def predict_policy(self):
        return self.model.actor.predict()

    def put_data(self, transition):
        self.data.append(transition)

    def make_batch(self):
        s_list, a_list, r_list, sp_list, pr_a_list, done_list = [], [], [], [], [], []
        for transition in self.data:
            s, a, r, sp, pr_a, done = transition

            s_list.append(s)
            a_list.append([a])
            r_list.append([r])
            sp_list.append(sp)
            pr_a_list.append([pr_a])
            done_list.append([0 if done else 1])

        s = tf.Variable(s_list, dtype=tf.float16)
        a = tf.Variable(a_list, dtype=tf.float16)
        r = tf.Variable(r_list, dtype=tf.float16)
        sp = tf.Variable(sp_list, dtype=tf.float16)
        done = tf.Variable(done_list, dtype=tf.float16)
        pr_a = tf.Variable(pr_a_list)

        return s, a, r, sp, done, pr_a

    def train(self):
        s, a, r, sp, done, pr_a = self.make_batch()

