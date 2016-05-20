C = csvread('cascades.csv', 1); % Read the CSV, skipping the header line
                                % C(:, 1) = cascade_id; C(:, 2) = dest_id; C(:, 3) = infection time
num_nodes = 50;
time_period = 1.0;

% Assuming that the cascades are sorted by time.
% Assuming that the nodes are numbered sequentially.

cascade_ids = unique(C(:, 1));

% Not all the edges are possible (if two nodes do not appear toguether in
% any cascade, the MLE solution for this alpha is zero)
possible_edges_arr = [];
for c_idx = 1:size(cascade_ids, 1)
    cascade = C(C(:, 1) == c_idx, :);
    for ii = 1:size(cascade, 1)
        for j = 1:(ii - 1)
            possible_edges_arr(end + 1, :) = [cascade(j, 2)+1, cascade(ii, 2)+1];
        end
    end
end

possible_edges = unique(possible_edges_arr, 'rows');

A = zeros(num_nodes, num_nodes); %influence parameters

for target_node = 1:num_nodes % Distributed
    cvx_begin % Optimization solver
        variable Ai(num_nodes);
        expression expr;

        for c_idx = 0:size(cascade_ids, 1)-1
            cascade = C(C(:, 1) == c_idx, :);
            infection_time = cascade(cascade(:, 2)+1 == target_node, 3);

            if size(infection_time, 1) == 0 % The node wasn't infected
                for j = 1:size(cascade, 1)
                    expr = expr + % TODO: Survival (log(S(T | t_j, alpha_ji)))
                end
            else % The node was infected
                if cascade(1, 3) ~= infection_time
                    % Do this only if this node wasn't the first node infected.
                    % If this was the first node infected, then we cannot
                    % deduce anything about the incoming edges.
                    expression log_sum;

                    for j = 1:size(cascade, 1)
                        % TODO ==> Complete the  Log-Likelihood
                    end

                    expr = expr + log(log_sum);
                end
            end
        end

        maximize expr
        subject to
            for j = 1:num_nodes
                if ismember([j, target_node], possible_edges)
                    Ai(j) >= 0
                else
                    Ai(j) == 0
                end
            end
    cvx_end

    A(:, target_node) = Ai;
end

A_soln = dlmread('solution.csv'); % This is the true A matrix.

[F1, precision, recall] = calc_score(A, A_soln, 1e-6)
