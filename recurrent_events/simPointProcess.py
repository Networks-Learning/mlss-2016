import cvxpy as CVX
import numpy as np

from sampleHawkes import sampleHawkes
from preprocessEv import preprocessEv

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


