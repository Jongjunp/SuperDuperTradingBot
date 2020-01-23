import tensorflow as tf
import tensorflow.keras as keras
from reinforcement.Parameter import *


class PPOModel:
    def __init__(self):
        # validating
        self.val = False

        self.critic = self.make_critic()
        self.actor = self.make_actor()

        self.critic.summary()
        self.actor.summary()

    @staticmethod
    # 지수 이동 평균 식.
    def exponential_average(old, new, b1):
        return old * b1 + (1 - b1) * new

    # Critic(v) 모델 생성 함수
    @staticmethod
    def make_critic():
        inputs = keras.Input(shape=STATE_SIZE, name="Stock_data")
        layer = keras.layers.Flatten(name="Flatten")(inputs)
        layer = keras.layers.Dense(300, activation='tanh', name="Dense_1")(layer)
        layer = keras.layers.Dense(150, activation='tanh', name="Dense_2")(layer)
        outputs = keras.layers.Dense(1, activation=None, name="Value")(layer)

        model = keras.Model(inputs=inputs, outputs=outputs, name="Critic")
        model.compile(optimizer=keras.optimizers.Adam(lr=LEARNING_RATE),
                      loss='mse', experimental_run_tf_function=False)
        model.summary()
        return model

    # Actor(Q) 모델 생성 함수
    @staticmethod
    def make_actor():
        inputs = keras.Input(shape=STATE_SIZE, name="Data")
        advantage = keras.Input(shape=(1, ))
        old_prediction = keras.Input(shape=(ACTION_SIZE,))
        layer = keras.layers.Flatten(name="Flatten")(inputs)

        layer = keras.layers.Dense(300, activation='selu', name="Dense_1")(layer)
        layer = keras.layers.Dense(150, activation='selu', name="Dense_2")(layer)
        outputs = keras.layers.Dense(ACTION_SIZE, activation='softmax', name="Policy",
                                     kernel_initializer=keras.initializers.VarianceScaling(scale=2.0))(layer)

        model = keras.Model(inputs=[inputs, advantage, old_prediction], outputs=[outputs], name="Actor")
        model.compile(optimizer=keras.optimizers.Adam(lr=LEARNING_RATE),
                      loss=PPOModel.proximal_policy_optimization_loss(advantage, old_prediction),
                      experimental_run_tf_function=False)

        model.summary()
        return model

    # PPO의 Loss 함수
    @staticmethod
    def proximal_policy_optimization_loss(advantage, old_pred):
        def loss(true, pred):
            prob = keras.backend.sum(true * pred, axis=-1)
            old_prob = keras.backend.sum(true * old_pred, axis=-1)
            r = keras.backend.log(prob)/(keras.backend.log(old_prob) + 1e-4)

            tmp = keras.backend.mean(keras.backend.minimum(r * advantage, keras.backend.clip(r, 1-EPS, 1+EPS) * advantage))
            return -keras.backend.log(prob + 1e-4) * tmp

        return loss

    # 모델로부터 행동 선택
    def get_action(self, observation):
        p = self.actor.predict([observation.reshape(1, 31, 5), DUMMY_VALUE, DUMMY_ACTION])
        if self.val is False:
            action = np.random.choice(ACTION_SIZE, p=np.nan_to_num(p[0]))
        else:
            action = np.argmax(p[0])

        action_matrix = np.zeros(ACTION_SIZE)
        action_matrix[action] = 1

        return action, action_matrix, p


