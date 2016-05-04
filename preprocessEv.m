function [lambda_ti, survival]= preprocessEv(tev, T,w)
lambda_ti=zeros(1,length(tev));
survival=0;
for ii=1:length(tev)
    if ii>1
        lambda_ti(ii)= sum(exp(-w*(tev(ii)-tev(1:ii-1))));
    end
    survival=survival+ (1/w)*(1-exp(-w*(T-tev(ii))));
end