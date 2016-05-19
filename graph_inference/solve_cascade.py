#!/usr/bin/env python
from __future__ import print_function
import csv
import numpy as np
import cvxpy as CVX
from collections import defaultdict

# This file has been changed from a script friendly format to an interactive
# session friendly version.

## You have to make sure to set these parameters to be the same as the
# parameters used to generate cascades.csv
input_file = open('cascades.csv', 'r')
time_period = 1.0
num_nodes = 50

# Cascades is a dictionary which will map cascade indexes (integers)
# to list of tuples of (time_of_infection, node_id_of_infected node)
cascades = defaultdict(lambda : [])

# Reading data
for row in csv.DictReader(input_file):
    # keys = 'cascade_id', 'dst', 'at'
    cascade_id = row['cascade_id']
    dst        = int(row['dst'])
    at         = float(row['at'])
    assert at < time_period, "Infection after observation period."
    cascades[cascade_id].append((at, dst))

# Start definition of the problem

# Sort according to time
for cascade_id in cascades.keys():
    cascades[cascade_id] = sorted(cascades[cascade_id])

# Possible edges: if we have never seen any infection travel down an edge, the
# best estimate for alpha for that edge is 0, i.e. it does not exist.
possible_edges = set()
for c in cascades.values():
    for i in range(len(c)):
       for j in range(i):
           possible_edges.add((c[j][1], c[i][1]))

# Formulating the problem for each row of influence matrix A
A = np.zeros((num_nodes, num_nodes), dtype=float)
probs = []
results = []


def logSurvival(t_i, t_j, alpha_ji):
    # TODO
    raise NotImplementedError('logSurvival not implemented.')

def hazard(t_i, t_j, alpha_ji):
    # TODO
    raise NotImplementedError('hazard not implemented.')

# These problems can be solved in parallel
for target_node in range(num_nodes):

    # This is one column of the alpha matrix
    Ai = CVX.Variable(num_nodes, name='A[:, {}]'.format(target_node))

    # Which edges are constrained to be zero
    constraints = []
    for j in range(num_nodes):
        if (j, target_node) not in possible_edges:
            constraints.append(Ai[j] == 0)
        else:
            constraints.append(Ai[j] >= 0)

    # Constructing the log-likelihood for the target_node
    expr = 0
    for c_idx, c in cascades.items():
        infection_time_arr = [x[0] for x in c if x[1] == target_node]

        assert len(infection_time_arr) <= 1

        if len(infection_time_arr) == 0:
            # Node 'i' was not infected in this cascade
            for j in range(len(c)):
                alpha_ji = Ai[c[j][1]]
                t_j = c[j][0]
                T = time_period
                expr += logSurvival(T, t_j, alpha_ji)
        else:
            # Node 'i' was infected in this cascade
            infection_time = infection_time_arr[0]
            t_i = infection_time

            if c[0][0] != infection_time:
                # Do this only if the target_node wasn't the first node
                # infected in the cascade.
                # If it was the first node (else branch), then we cannot deduce
                # anything about the incoming edges.
                log_sum = 0
                for j in range(len(c)):
                    # TODO => Complete the Log-Likelihood if
                    # the node was infected.
                    pass

                expr += CVX.log(log_sum)

    prob = CVX.Problem(CVX.Maximize(expr), constraints)
    res = prob.solve(verbose=True)
    probs.append(prob)
    results.append(res)
    if prob.status in [CVX.OPTIMAL, CVX.OPTIMAL_INACCURATE]:
        A[:, target_node] = np.asarray(Ai.value).squeeze()
    else:
        A[:, target_node] = -1

