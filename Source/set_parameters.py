import numpy as np

f = []
# set starting parameters
starting_guess = np.array([0.001, 0.5, 0, 0.001])
alpha = len(f) * [starting_guess[0]]
beta = len(f) * [starting_guess[1]]
rho = len(f) * [starting_guess[2]]
nu = len(f) * [starting_guess[3]]