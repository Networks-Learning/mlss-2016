function L= Hawkes_log_lik(T,alpha_opt,lambda_opt,lambda_ti, survival)
L=0;
for i=1:length(lambda_ti)
    L= L+ sum(log(lambda_opt+alpha_opt*lambda_ti{i}))- lambda_opt*T(i) - alpha_opt*survival(i);
end