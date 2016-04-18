#!/usr/bin/env python
from __future__ import print_function
import click
import os
import sys
import csv
import numpy as np
import cvxpy as CVX
import networkx as nx
from scipy import optimize as O
from collections import defaultdict

def run(input_file, time_period, num_nodes):
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

    A = np.zeros((num_nodes, num_nodes), dtype=float)

    for target_node in range(num_nodes):
        Ai_init = np.zeros(num_nodes, dtype=float)



