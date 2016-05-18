#!/usr/bin/env python
from __future__ import print_function
import csv
import numpy as np
from scipy import optimize as O
from collections import defaultdict


def f_factory(Ai_coef, Ai_log_coefs, Ai_mask):
    """
    Returns a pair of functions which calculate the negative log-likelihood
    and the gradient respectively.

    Ai_mask is used to work only on the variables which are not constrained to
    be zero.

    L-BFGS-B does not handle variables which are bounded to be a constant well.
    """

    def f(x):
        # TODO: Implement the log-likelihood.
        raise NotImplementedError("Log-likelihood function not implemented.")
        return 0

    def f_prime(x):
        # TODO: Implement the gradient of the log-likelihood.
        # Copying the vector to avoid writing over the Coefficients.
        raise NotImplementedError("Gradient function not implemented.")
        return np.zeros_like(x)

    return f, f_prime


input_file = open('cascades.csv', 'r')
time_period = 1.0
num_nodes = 50

cascades = defaultdict(lambda : [])

# Reading data
for row in csv.DictReader(input_file):
    # keys = 'cascade_id', 'dst', 'at'
    cascade_id = int(row['cascade_id'])
    dst        = int(row['dst'])
    at         = float(row['at'])
    assert at < time_period, "Infection after observation period."
    cascades[cascade_id].append((at, dst))

# Start definition of the problem

# Sort according to time
cascades_keys = sorted(cascades.keys())
for cascade_id in cascades_keys:
    cascades[cascade_id] = sorted(cascades[cascade_id])

# Possible edges
possible_edges = set()
for c in cascades.values():
    for i in range(len(c)):
       for j in range(i):
           possible_edges.add((c[j][1], c[i][1]))

A = np.zeros((num_nodes, num_nodes), dtype=float)
statuses = []
results = []

# Placing a bound of 0 causes problems if the function evaluation results
# in calculating the logarithm of a 0 term.
eps = 1e-14

for target_node in range(num_nodes):
    Ai_init = np.zeros(num_nodes, dtype=float) + 1.0
    Ai_coef = np.zeros_like(Ai_init)

    Ai_log_coefs = [np.zeros((num_nodes,), dtype=float)
                    for _ in cascades_keys]

    # Find which nodes can potentially have a connection to the ith node.
    Ai_mask = np.array([(j, target_node) in possible_edges
                        for j in range(num_nodes)], dtype=bool)

    # Only create as many constraints as number of variables we have
    Ai_constraints = [(eps, None)] * Ai_mask.sum()

    for c_idx, key in enumerate(cascades_keys):
        c = cascades[key]
        infection_time_arr = [x[0] for x in c if x[1] == target_node]

        assert len(infection_time_arr) <= 1

        if len(infection_time_arr) == 0:
            # Node wasn't infected
            for j in range(len(c)):
                Ai_coef[c[j][1]] += (c[j][0] - time_period)
        else:
            infection_time = infection_time_arr[0]

            for j in range(len(c)):
                if c[j][0] < infection_time:
                    Ai_coef[c[j][1]] += (c[j][0] - infection_time)
                    Ai_log_coefs[c_idx][c[j][1]] += 1.0
                else:
                    break

    assert np.all(Ai_coef <= 0)

    f, f_prime = f_factory(Ai_coef, Ai_log_coefs, Ai_mask)

    # print('Initial f(x) = {}'.format(f(Ai_init[Ai_mask])))
    # print('Initial f_prime(x) = {}'.format(f_prime(Ai_init[Ai_mask])))
    # print('Initial Ai_coef = {}'.format(Ai_coef))

    if Ai_mask.sum() > 0:
        [Ai, res, status] = O.fmin_l_bfgs_b(f, Ai_init[Ai_mask], fprime=f_prime,
                                            disp=2, bounds=Ai_constraints, factr=1e07)
        A[Ai_mask, target_node] = Ai
    else:
        Ai = Ai_init
        res = - np.inf
        status = { 'error': 'No possible edges to this node.' }

    statuses.append(status)
    results.append(res)

