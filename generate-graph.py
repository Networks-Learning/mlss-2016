#!/usr/bin/env python
from __future__ import print_function
import click
import os.path as P
import sys
import numpy as np
import networkx as nx
import random as R

N = 50
SEED = 42


@click.command()
@click.option('-o', '--output', 'output_path',
              prompt='Which file to write the graph to',
              default='graph.csv',
              help='File in which to write the generated graph.')
@click.option('-g', '--graph', 'graph_type',
              default='erdos',
              help='What kind of graph to generate')
@click.option('-n', '--nodes', 'num_nodes',
              default=N,
              help='Number of nodes.')
@click.option('-p', '--prob', 'edge_prob',
              default=4.0 / N, # Total number of edges = N^2, so edges = 4 * N
              help='Fraction of edges which should exist')
@click.option('-f', '--force',
              is_flag=True,
              help='Overwrite files.')
@click.option('--seed',
              default=SEED,
              help='Seed for graph generation.')
@click.option('-S', '--solution', 'solution_path',
              prompt='Which file to save solution to',
              default='solution.csv',
              help='The path where to save the solution (as a CSV file).'
                   'If the filename ends in .gz, the file will be GZipped.')
def run(output_path, graph_type, force,
        seed, num_nodes, edge_prob, solution_path):

    any_op_file_exists = (P.exists(output_path) or P.exists(solution_path))

    if any_op_file_exists and not force:
        print('Cannot overwrite without --force', file=sys.stderr)
        sys.exit(-1)

    g = None
    if graph_type == 'erdos':
        g = nx.erdos_renyi_graph(num_nodes, edge_prob,
                                 seed=seed, directed=True)
    else:
        print('Unknown graph type: ', graph_type, file=sys.stderr)
        sys.exit(-1)

    A = np.zeros((num_nodes, num_nodes), dtype='float')
    # All edges are given uniformly random weights.
    for u, v, d in g.edges(data=True):
        d['act_prob'] = R.random()
        A[u, v] = d['act_prob']

    nx.write_edgelist(g, output_path)
    np.savetxt(solution_path, A, delimiter=',')


if __name__ == '__main__':
    run()

