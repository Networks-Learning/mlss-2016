#!/usr/bin/env python
from __future__ import print_function
import click
import os
import sys
import csv
import numpy as np
import cvxpy as CVX
import networkx as nx
from collections import defaultdict


def get_soln_A(src_graph):
    '''Read the "correct" solution for a graph.'''
    g = nx.read_edgelist(src_graph, create_using=nx.DiGraph())
    nodes = [str(y) for y in sorted([int(x) for x in g.nodes()])]
    num_nodes = len(nodes)
    A = np.zeros((num_nodes, num_nodes), dtype=float)
    for i in range(num_nodes):
        for j in range(num_nodes):
            i_, j_ = str(i), str(j)
            if j_ in g[i_]:
                A[i, j] = g[i_][j_]['act_prob']

    return A

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
def run_with_cvx(input_file, time_period, num_nodes):
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

    # Possible edges
    possible_edges = set()
    for c in cascades.values():
        for i in range(len(c)):
           for j in range(i):
               possible_edges.add((c[j][1], c[i][1]))

    # Formulating the problem for each row of influence matrix A
    A = np.zeros((num_nodes, num_nodes), dtype=float)
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
                # NICE-TO-HAVE: Can be precomputed and vectorized
                for j in range(len(c)):
                    expr += Ai[c[j][1]] * (c[j][0] - time_period)
            else:
                # Node 'i' was infected in this cascade
                # NICE-TO-HAVE: Vectorize
                infection_time = infection_time_arr[0]
                num_infected_before = 0
                log_sum = 0
                for j in range(len(c)):
                    if c[j][0] < infection_time:
                        num_infected_before += 1
                        expr += Ai[c[j][1]] * (c[j][0] - infection_time)
                        log_sum += Ai[c[j][1]]
                    else:
                        break

                if num_infected_before > 0:
                    # This check avoids log(0) terms
                    expr += CVX.log(log_sum)

        prob = CVX.Problem(CVX.Maximize(expr), constraints)
        res = prob.solve(verbose=True)
        probs.append(prob)
        results.append(res)
        if prob.status in [CVX.OPTIMAL, CVX.OPTIMAL_INACCURATE]:
            A[:, target_node] = np.asarray(Ai.value).squeeze()
        else:
            A[:, target_node] = -1

    return A, probs, results

# TODO: Add code for comparing the performance.
