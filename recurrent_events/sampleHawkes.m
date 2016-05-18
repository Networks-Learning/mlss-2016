function [tev, T]=sampleHawkes(lambda_0,alpha_0,w,T, Nev)
tev=zeros(1,Nev);
%first event
n=1;
lambda_star=lambda_0;
u=rand;
s=-1/lambda_star*log(u);
tev(1)=s;
%for n>1
n=2;
while (n<=Nev)
    lambda_star=lambda_star+alpha_0;
    u=rand;
    s=s-log(u)/lambda_star; % or  s=s+exprnd(lambda_star)
    if s<=T
        d=rand;
        lambda_s=lambda_0+alpha_0*sum(exp(-w*(s-tev(1:n-1))));
        if d<=lambda_s/lambda_star
           tev(n)=s;
           lambda_star=lambda_s;
           n=n+1;
        end
    else
        break;
    end
    
end
tev=tev(1:n-1);
if n==Nev+1
    T=tev(end);
end