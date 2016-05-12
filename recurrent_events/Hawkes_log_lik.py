import numpy as np
import cvxpy as CVX

def Hawkes_log_lik(T, alpha_opt, lambda_opt, lambda_ti, survival, for_cvx=False):
    L = 0
    for i in range(len(lambda_ti)):
        if for_cvx:
            L += CVX.sum_entries(CVX.log(lambda_opt + alpha_opt * lambda_ti[i]))
        else:
            L += np.sum(np.log(lambda_opt + alpha_opt * lambda_ti[i]))

        L -= lambda_opt * T[i] - alpha_opt * survival[i]

    return L

