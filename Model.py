import tensorflow as tf
import tensorflow.keras as keras
import tensorflow_probability as tfp


class PPOModel:
    def __init__(self, action_size, state_size, lr, noise):
        self.action_size = action_size
        self.state_size = state_size
        self.lr = lr
        self.noise = noise

        self.critic = self.make_critic()
        self.actor = self.make_actor()

        self.critic.summary()
        self.actor.summary()

    def make_critic(self):
        inputs = keras.Input(shape=self.state_size, name="Stock_data")
        layer = keras.layers.Flatten(name="Flatten")(inputs)
        layer = keras.layers.Dense(300, activation='selu', name="Dense_1")(layer)
        layer = keras.layers.Dense(300, activation='selu', name="Dense_2")(layer)
        outputs = keras.layers.Dense(1, activation=None, name="Value")(layer)

        model = keras.Model(inputs=inputs, outputs=outputs, name="Critic")
        model.compile(optimizer=keras.optimizers.Adam(lr=self.lr), loss='mse')
        return model

    def make_actor(self):
        inputs = keras.Input(shape=self.state_size, name="Data")
        layer = keras.layers.Flatten(name="Flatten")(inputs)
        layer = keras.layers.Dense(300, activation='selu', name="Dense_1")(layer)
        layer = keras.layers.Dense(300, activation='selu', name="Dense_2")(layer)
        outputs = keras.layers.Dense(self.action_size, activation='softmax', name="Policy")(layer)

        model = keras.Model(inputs=inputs, outputs=outputs, name="Actor")
        model.compile(optimizer=keras.optimizers.Adam(lr=self.lr), loss='mse')
        return model

    @staticmethod
    def proximal_policy_optimization_loss(advantage, old_pred):
        def loss(true, pred):
            prob = keras.backend.sum(true * pred, axis=-1)
            old_prob = keras.backend.sum(true * old_pred, axis=-1)
            ratio = prob/(old_prob + 1e-10)

            return

