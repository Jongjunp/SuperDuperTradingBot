import datetime
import numpy as np

# Hyperparameter
EPS           = .05
LEARNING_RATE = .0001
LMBDA         = .95
T_HORIZON     = 20
DISCOUNT      = .95
ENTROPY_LOSS  = 5e-3

# Reinforcement Size
ACTION_SIZE   = 3
STATE_SIZE    = (31, 5, )
BATCH_SIZE    = 250
BUFFER_SIZE   = 1000
EPISODE       = 20        # 5년

# Epoch / Count
K_EPOCH = 5

# Start Date
START_DATE = datetime.date(2010, 1, 2)

# Dummy
DUMMY_ACTION   = np.zeros((1, ACTION_SIZE))
DUMMY_VALUE    = np.zeros((1, 1))
