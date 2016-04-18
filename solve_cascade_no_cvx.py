#!/usr/bin/env python
from __future__ import print_function
import click
import os
import sys
import csv
import numpy as np
import networkx as nx
from scipy import optimize as O
from collections import defaultdict

def f_factory(Ai_coef, Ai_log_coefs, Ai_mask):
    def f(x):
        v = Ai_coef[Ai_mask].dot(x)
        # TODO: Can be vectorized better
        for log_coefs in Ai_log_coefs:
            if not np.all(log_coefs[Ai_mask] == 0):
                v += np.log(log_coefs[Ai_mask].dot(x))
        return -v

    def f_prime(x):
        v_prime = Ai_coef[Ai_mask].copy()
        for log_coefs in Ai_log_coefs:
            if not np.all(log_coefs[Ai_mask] == 0):
                v_prime += log_coefs[Ai_mask] / log_coefs[Ai_mask].dot(x)
        return -v_prime

    return f, f_prime


def run_no_cvx(input_file, time_period, num_nodes):
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

    eps = 1e-14

    for target_node in range(num_nodes):
        Ai_init = np.zeros(num_nodes, dtype=float) + 1.0
        Ai_coef = np.zeros_like(Ai_init)

        Ai_log_coefs = [np.zeros((num_nodes,), dtype=float)
                        for _ in cascades_keys]

        Ai_mask = np.array([ (j, target_node) in possible_edges
                              for j in range(num_nodes) ], dtype=bool)
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

    return A, statuses, results



