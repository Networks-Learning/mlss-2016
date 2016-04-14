#!/usr/bin/env python
from __future__ import print_function
import click
import os
import sys
import networkx as nx
import random as R

N = 50
SEED = 42

@click.command()
@click.option('-o', '--output', 'output_path',
              prompt='Which file to write the output to',
              default='graph.csv',
              help='File in which to write the generated graph.')
@click.option('-g', '--graph', 'graph_type',
              default='erdos',
              help='What kind of graph to generate')
@click.option('-n', '--nodes', 'num_nodes',
              default=N,
              help='Number of nodes.')
@click.option('-p', '--prob', 'edge_prob',
              default=4.0 / N, # Total number of edges = N², so edges = 4 * N
              help='Fraction of edges which should exist')
@click.option('-f', '--force',
              is_flag=True,
              help='Overwrite files.')
@click.option('--seed',
              default=SEED,
              help='Seed for graph generation.')
def run(output_path, graph_type, force, seed, num_nodes, edge_prob):
    if os.path.exists(output_path) and not force:
        print('Cannot overwrite without --force', file=sys.stderr)
    else:
        if graph_type == 'erdos':
            g = nx.erdos_renyi_graph(num_nodes, edge_prob,
                                     seed=seed, directed=True)

            # All edges are given uniformly random weights.

            for u, v, d in g.edges(data=True):
                d['threshold'] = R.random()

            nx.write_edgelist(g, output_path, delimiter=',')

        else:
            print('Unknown graph type: ', graph_type, file=sys.stderr)


if __name__ == '__main__':
    run()

