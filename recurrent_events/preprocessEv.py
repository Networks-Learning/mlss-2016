import numpy as np

def preprocessEv(tev, T, w):
    lambda_ti = np.zeros_like(tev, dtype=float)
    survival = 0

    for i in range(len(tev)):
        lambda_ti[i] = np.sum(np.exp(-w * (tev[i] - tev[0:i])))
        survival += (1.0 / w) * (1.0 - np.exp(-w * (T - tev[i])))

    return lambda_ti, survival

