import cvxpy as CVX
import numpy as np

from sampleHawkes import sampleHawkes
from preprocessEv import preprocessEv
from Hawkes_log_lik import Hawkes_log_lik
import plotHawkes as ph
import matplotlib.pyplot as plt

# Simulation time
T = 10

# Maximum number of events per realization
maxNev = 200

# Base intensity
lambda_0 = 1

# Self excitation parameter
alpha_0 = 0.5

# Rate of decay
w = 1

# Number of samples to take
Nsamples = 5

tev       = [ None ] * Nsamples
Tend      = [ None ] * Nsamples
lambda_ti = [ None ] * Nsamples
survival  = np.zeros(Nsamples)

for i in range(Nsamples):
    tev[i], Tend[i] = sampleHawkes(lambda_0, alpha_0, w, T, maxNev)
    lambda_ti[i], survival[i] = preprocessEv(tev[i], Tend[i], w)

ph.plotHawkes(tev, lambda_0, alpha_0, w, T, 10000)
plt.ion()
plt.show()

## Solution using CVX

alpha_opt = CVX.Variable() if alpha_0 > 0 else 0
constraints = [alpha_opt >= 0] if alpha_0 > 0 else []
lambda_opt = CVX.Variable()
constraints.append(lambda_opt >= 0)

prob = CVX.Problem(
    CVX.Maximize(Hawkes_log_lik(Tend,
                                alpha_opt,
                                lambda_opt,
                                lambda_ti,
                                survival,
                                for_cvx=True)),
    constraints=constraints)

res = prob.solve(verbose=True)


error_alpha = (alpha_opt.value - alpha_0) if alpha_0 > 0 else 0
error_lambda_0 = (lambda_opt.value - lambda_0)

print('error_alpha = {}, error_lambda_0 = {}'
      .format(error_alpha, error_lambda_0))
