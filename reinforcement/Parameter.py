import datetime
import numpy as np

# Hyperparameter
EPS           = .2
LEARNING_RATE = .005
LMBDA         = .95
T_HORIZON     = 20
DISCOUNT      = .95
ENTROPY_LOSS  = 5e-3

# Reinforcement Size
ACTION_SIZE   = 3
STATE_SIZE    = (61, 5, )
BATCH_SIZE    = 30
BUFFER_SIZE   = 240
EPISODE       = 1825        # 5년

# Epoch / Count
K_EPOCH = 20

# Start Date
START_DATE = datetime.date(2010, 1, 2)

# Dummy
DUMMY_ACTION   = np.zeros((1, ACTION_SIZE))
DUMMY_VALUE    = np.zeros((1, 1))
