import tensorflow as tf
import tensorflow.keras as keras
import tensorflow_probability as tfp


class Critic(keras.Model):
    def __init__(self):
        super(Critic, self).__init__()

        kernel_initializer = keras.initializers.VarianceScaling(scale=2.0)

        self.hidden_1 = keras.layers.Dense(
            units=64,
            activation=keras.activations.selu,
            kernel_initializer=kernel_initializer
        )
        self.hidden_2 = keras.layers.Dense(
            units=64,
            activation=keras.activations.selu,
            kernel_initializer=kernel_initializer
        )
        self.dense_value = keras.layers.Dense(
            units=1,
            activation=None,
            kernel_initializer=kernel_initializer
        )

    def call(self, inputs, training=False, masks=False):
        inputs = keras.utils.normalize(inputs, order=2)

        hidden = self.hidden_1(inputs)
        hidden = self.hidden_2(hidden)
        value = self.dense_value(hidden)

        return value[..., 0]