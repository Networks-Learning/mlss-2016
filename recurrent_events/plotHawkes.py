import matplotlib.pyplot as plt
import numpy as np

def plotHawkes(tev, l_0, alpha_0, w, T, res):
    tvec = np.arange(0, T, step=T / res)

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


    plt.ylim([-0.1, None]) # To make sure that the event markers show.
    # plt.legend

