function [F1, precision, recall] = calc_score(A_pred, A_soln, eps)

num_edges = sum(sum(A_soln > eps));
TP = sum(sum(A_soln(A_pred > eps) >= eps));
FP = sum(sum(A_soln(A_pred > eps) < eps));
FN = sum(sum(A_pred(A_soln > eps) < eps));

precision = TP / (TP + FP);
recall = TP / num_edges;

F1 = 2 * TP / (2 * TP + FN + FP);

end