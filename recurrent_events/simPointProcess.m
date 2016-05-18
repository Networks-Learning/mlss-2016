close
clear 
%% Parameters
T=10; % simulation time
maxNev= 50; %maximum number of events per realization
lambda_0= 1; %base intensity
alpha_0 = 0.5; % self-excitation parameter. Set alpha_0 = 0 to generate samples from a Poisson process 
w = 1; % decay of the exponential kernel
Nsamples= 20; %number of realizations of the Hawkes process
tev=cell(1,Nsamples);
Tend=zeros(1,Nsamples);
lambda_ti=cell(1,Nsamples);
survival=zeros(1,Nsamples);
%% Sample from a Univariate Hawkes
for i = 1:Nsamples
[tev{i}, Tend(i)]=sampleHawkes(lambda_0,alpha_0,w,T, maxNev);
[lambda_ti{i}, survival(i)]= preprocessEv(tev{i},Tend(i),w);
end

%% plot first realization of the Hawkes and mean of the Hawkes (if alpha_0<w)
plotHawkes(tev,lambda_0,alpha_0,w,T, 10000);


%% Find the ML estimates of the Hawkes parameters
%addpath cvx
% Builds and solves a simple linear program
echo off
cvx_begin
   if alpha_0~=0
    variable alpha_opt;
   else
     alpha_opt=0;
   end
   variable lambda_opt;
   maximize(Hawkes_log_lik(Tend,alpha_opt,lambda_opt,lambda_ti, survival))
   
   subject to
       if alpha_0~=0
         alpha_opt>=0
       end
       lambda_opt>=0
cvx_end

echo off

%% Estimation error
error_alpha  = abs(alpha_0-alpha_opt)
error_lambda = abs(lambda_0-lambda_opt)
