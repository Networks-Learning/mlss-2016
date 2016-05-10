import numpy as np

def preprocessEv(tev, T, w):
    lambda_ti = np.zeros_like(tev)
    survival = 0

    for i in range(len(tev)):
        if i > 0:
            lambda_ti[i] = sum(np.exp(-w * (tev[i] - tev[0:i - 1])))

        survival += (1.0 / w) * (1 - np.exp(-w * (T - tev[i])))

    return lambda_ti, survival

