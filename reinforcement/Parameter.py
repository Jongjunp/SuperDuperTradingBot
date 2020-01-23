import datetime
import numpy as np

# Hyperparameter
EPS           = .2
LEARNING_RATE = .00001
LMBDA         = .95
T_HORIZON     = 20
DISCOUNT      = .95
ENTROPY_LOSS  = 5e-3

# Reinforcement Size
ACTION_SIZE   = 3
STATE         = 30
STATE_SIZE    = (31, 5, )
BATCH_SIZE    = 100
BUFFER_SIZE   = 2000
EPISODE       = 40        # 5년

# Epoch / Count
K_EPOCH = 10

# Start Date
START_DATE = datetime.date(2010, 1, 2)

# Dummy
DUMMY_ACTION   = np.zeros((1, ACTION_SIZE))
DUMMY_VALUE    = np.zeros((1, 1))
