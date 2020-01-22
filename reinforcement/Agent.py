import tensorflow as tf

from reinforcement.Model import PPOModel
from reinforcement.Parameter import *


class Agent:
    def __init__(self):
        self.data = []

        self.model = PPOModel()

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
        pass


