# This file is meant to be loaded into the interactive session

import numpy as np

def calc_score(A_pred, A_soln, eps=1e-6):
    """Calculates the F1 score for a given activation against the ground truth.."""
    # The A_pred may have some very small negative numbers as well.
    # So < eps == zero, and >= eps == non-zero

    num_edges = np.sum(A_soln > eps)
    TP = np.sum(A_soln[A_pred > eps] >= eps)
    FP = np.sum(A_soln[A_pred > eps] < eps)
    FN = np.sum(A_pred[A_soln > eps] < eps)

    precision = TP * 1.0 / (TP + FP)
    recall = TP * 1.0/ num_edges

    F1 = 2 * TP / (2 * TP + FN + FP)

    # TODO: Add metrics for comparing the actual numbers.

    return {'F1'        : F1,
            'precision' : precision,
            'recall'    : recall}



