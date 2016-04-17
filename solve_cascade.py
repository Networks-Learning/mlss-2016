#!/usr/bin/env python
from __future__ import print_function
import click
import os
import sys
import csv
import numpy as np
import cvxpy as CVX
from collections import defaultdict


# @click.command()
# @click.option('-i', '--input', 'input_file',
#               type=click.File('r'),
#               prompt='File with cascade info:',
#               default='cascades.csv',
#               help='File with cascade info.')
# @click.option('-T', '--time', 'time_period',
#               prompt='Time horizon.',
#               default=1.0,
#               help='Time horizon (after which, no data was collected).')
def run(input_file, time_period):
    nodes = set()
    cascades = defaultdict(lambda : [])

    # Reading data
    for row in csv.DictReader(input_file):
        # keys = 'cascade_id', 'dst', 'at'
        cascade_id = row['cascade_id']
        dst        = int(row['dst'])
        at         = float(row['at'])

        nodes.add(dst)
        cascades[cascade_id].append((at, dst))

    # Start definition of the problem
    num_nodes = len(nodes)

    # Sort according to time
    for cascade_id in cascades.keys():
        cascades[cascade_id] = sorted(cascades[cascade_id])

    # Possible edges
    possible_edges = set()
    for c in cascades.values():
        for i in range(len(c)):
           for j in range(i):
               possible_edges.add((c[j][1], c[i][1]))

    # Formulating the problem for each row of influence matrix A
    A = []
    probs = []
    results = []

    # These problems can be solved in parallel
    for target_node in range(num_nodes):
        Ai = CVX.Variable(num_nodes, name='A[:, {}]'.format(target_node))

        # Which edges are constrained to be zero
        constraints = []
        for j in range(num_nodes):
            if (j, target_node) not in possible_edges:
                constraints.append(Ai[j] == 0)
            else:
                constraints.append(Ai[j] >= 0)

        expr = 0
        for c_idx, c in cascades.items():
            infection_time_arr = [x[0] for x in c if x[1] == target_node]

            assert len(infection_time_arr) <= 1

            if len(infection_time_arr) == 0:
                # Node 'i' was not infected in this cascade
                # TODO: Can be precomputed and vectorized
                for j in range(len(c)):
                    expr += Ai[j] * (c[j][0] - time_period)
            else:
                # Node 'i' was infected in this cascade
                # TODO: Vectorize
                infection_time = infection_time_arr[0]
                num_infected_before = 0
                log_sum = 0
                for j in range(len(c)):
                    if c[j][0] < infection_time:
                        num_infected_before += 1
                        expr += Ai[j] * (c[j][0] - infection_time)
                        log_sum += Ai[j]
                    else:
                        break

                if num_infected_before > 0:
                    # This avoids np.log(0) term
                    expr += CVX.log(log_sum)

        prob = CVX.Problem(CVX.Maximize(expr), constraints)
        res = prob.solve(verbose=True)
        probs.append(prob)
        results.append(res)
        A.append(Ai)

    return A, probs, results

