#!/usr/bin/env python
from __future__ import print_function
import click
import os
import sys
import csv
import cxvpy as CVX


@click.command()
@click.option('-i', '--input', 'input_file',
              type=click.File('r'),
              prompt='File with cascade info:',
              default='cascade.csv',
              help='File with cascade info.')
@click.option('-T', '--time', 'time_period',
              prompt='Time horizon.',
              default=1.0,
              help='Time horizon (after which, no data was collected).')
def run(input_file, time_period):
    for row in csv.DictReader(input_file):
        # keys = 'cascade_id', 'src', 'dst', 'at'
        pass

