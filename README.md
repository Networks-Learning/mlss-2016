# MLSS 2016

This is the material for practical about machine learning on networks held at MLSS-2016, at Cadiz.

This tutorial has two parts

## Graph inference

This is the code we used for the tutorial session about networks learning in
MLSS-2016. The tutorial is based on the NetRate algorithm described here:

> M. Gomez-Rodriguez, D. Balduzzi, B. Schölkopf. Uncovering the Temporal Dynamics of Diffusion Networks. The 28th International Conference on Machine Learning (ICML), 2011.

### Generation 

The generation code is written in Python 3.

#### Requirements

The requirements for data generation are in `requirements.txt`.

#### Graph

The script `generate-graph.py` can be used to generate a graph file as well as
the solution `A` matrix. Run `generate-graph.py -h` to see all supported options.

The script `csv2dot.sh` can be used on Unix-like systems to convert the graph
to a dot file which can be visualized using GraphViz.

#### Cascade

The script `run_cascade.py` uses the graph generated in the previous step to
generate the cascade. Run `run_cascade.py -h` to see all the supported options.

### Inference

The inference code, unless explicitly stated, reads the input from
`cascades.csv`, assume that the time period of the cascades was `1.0` and
that there are `50` nodes in the graph.

#### Python

`solve_cascade.py` uses CVX to solve the NetRate problem. 
`solve_cascade_no_cvx.py` solves the problem using the L-BFGS-B algorithm.

`utils.py` contains code which can be used to calculate the performance
of the solutions.

##### Requirements
  
  - cvxpy
  - scipy

#### MATLAB

`solve_cascade.m` uses CVX to solve the NetRate problem.
`calc_score.m` defines the function which can calculate the performance.

##### Requirements

  - CVX

## Recurrent events

Here, we model recurring user activities with the help of Hawkes Processes.

### MATLAB

All functions are provided in separate files and are self-explanatory. The main file which runs the simulation and inference is `simPointProcess.m`.

##### Requirements

  - CVX

### Python

There is only one python file with one unimplemented function (`sampleHawkes`)
in the file `simPointProcess.py`. The file may be run in an interactive console.

##### Requirements

  - cvxpy
