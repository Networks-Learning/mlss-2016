C = csvread('cascades.csv', 2); % Read the CSV, skipping the header line
num_nodes = 50;
time_period = 1.0;

% Assuming that the cascades are sorted by time.
% Assuming that the nodes are numbered sequentially.

cascade_ids = unique(C(:, 1));

possible_edges_arr = [];
for c_idx = 1:size(cascade_ids, 1)
    cascade = C(C(:, 1) == c_idx, :);
    for ii = 1:size(cascade, 1)
        for j = 1:(ii - 1)
            possible_edges_arr(end + 1, :) = [cascade(j, 2), cascade(ii, 2)];
        end
    end
end

possible_edges = unique(possible_edges_arr, 'rows');

A = zeros(num_nodes, num_nodes);

for target_node = 1:num_nodes
    cvx_begin
        variable Ai(num_nodes);
        expression expr;

        for c_idx = 1:size(cascade_ids, 1)
            cascade = C(C(:, 1) == c_idx, :);
            infection_time = cascade(cascade(:, 2) == target_node, 3);

            if size(infection_time, 1) == 0 % The node wasn't infected
                for j = 1:size(cascade, 1)
                    expr = expr + Ai(cascade(j, 2) + 1) * (cascade(j, 3) - time_period);
                end
            else % The node was infected
                num_infected_before = 0;
                expression log_sum;
                for j = 1:size(cascade, 1)
                    if cascade(j, 3) < infection_time
                        num_infected_before =  num_infected_before + 1;
                        expr = expr + Ai(cascade(j, 2) + 1) * (cascade(j, 3) - infection_time);
                        log_sum = log_sum + Ai(cascade(j, 2) + 1);
                    else
                        break;
                    end
                end

                if num_infected_before > 0
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
