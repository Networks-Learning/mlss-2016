import cvxpy as CVX
import numpy as np
import matplotlib.pyplot as plt

# MATLAB: see sampleHawkes.m

def sampleHawkes(lambda_0, alpha_0, w, T, Nev, seed=None):
    """Generates a sample of a Hawkes process until one of the following happens:
      - The next generated event is after T
      - Nev events have been generated.

    Returns: a tuple with the event times and the last generated time.
    """

    # TODO: Implement.

    np.random.seed(seed)
    tev = np.zeros(Nev)
    Tend = T

    return tev, Tend

## MATLAB: preprocessEv.m

def preprocessEv(tev, T, w):
    lambda_ti = np.zeros_like(tev, dtype=float)
    survival = 0

    for i in range(len(tev)):
        lambda_ti[i] = np.sum(np.exp(-w * (tev[i] - tev[0:i])))
        survival += (1.0 / w) * (1.0 - np.exp(-w * (T - tev[i])))

    return lambda_ti, survival

## MATLAB: Hawkes_log_lik.m

def Hawkes_log_lik(T, alpha_opt, lambda_opt, lambda_ti, survival, for_cvx=False):
    # The implementation has to be different for CVX and numpy versions because
    # CVX variables cannot handle the vectorized operations of Numpy  like
    # np.sum and np.log.

    L = 0
    for i in range(len(lambda_ti)):
        if for_cvx and len(lambda_ti) > 0:
            L += CVX.sum_entries(CVX.log(lambda_opt + alpha_opt * lambda_ti[i]))
        else:
            L += np.sum(np.log(lambda_opt + alpha_opt * lambda_ti[i]))

        L -= lambda_opt * T[i] + alpha_opt * survival[i]

    return L

## MATLAB: plotHawkes.m

def plotHawkes(tev, l_0, alpha_0, w, T, resolution):
    tvec = np.arange(0, T, step=T / float(resolution))

    mu_t = (np.exp((alpha_0 - w) * tvec) + w * (1.0 / (alpha_0 - w)) *
            (np.exp((alpha_0 - w) * tvec) - 1)) * l_0

    plt.plot(tvec, mu_t, 'b-', linewidth=1.5)

    colorLambda = ['r--', 'k--', 'g--', 'm--', 'c--']
    colorEv = ['r+', 'k+', 'g+', 'm+', 'c+']

    for i in range(len(tev)):
        n = -1
        l_t = np.zeros(len(tvec))

        for t in tvec:
            n += 1
            l_t[n] = l_0 + alpha_0 * np.sum(np.exp(-w * (t - tev[i][tev[i] < t])))

        plt.plot(tvec, l_t, colorLambda[i % len(colorLambda)])
        plt.plot(tev[i], np.zeros(len(tev[i])), colorEv[i % len(colorEv)])

##################################################

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

plotHawkes(tev, lambda_0, alpha_0, w, T, 10000.0)
plt.ion()  # Make the plot interactive
plt.show() # Show the plot. May not be needed in IPython


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

result = prob.solve(verbose=True)


error_alpha = (alpha_opt.value - alpha_0) if alpha_0 > 0 else 0
error_lambda_0 = (lambda_opt.value - lambda_0)

print('error_alpha = {}, error_lambda_0 = {}'
      .format(error_alpha, error_lambda_0))
