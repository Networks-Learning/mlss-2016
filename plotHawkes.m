function plotHawkes(tev,lambda_0,alpha_0,w,T, res)

tvec=0:max(T)/res:max(T);
mu_t= (exp((alpha_0-w).*tvec)+w*(alpha_0-w)^-1*(exp((alpha_0-w).*tvec)-1))*lambda_0;
plot(tvec, mu_t, 'b-','linewidth',1.5);


colorLambda={'r--','k--','g--','m--','c--'};
colorEv={'r+','k+','g+','m+','c+'};
for i=1:length(tev)
    n=0;
    lambda_t=zeros(1,length(tvec));
    for t=tvec
        n=n+1;
        lambda_t(n)= lambda_0+alpha_0*sum(exp(-w*(t-tev{i}(tev{i}<t))));
    end
    hold on, plot(tvec, lambda_t, colorLambda{mod(i,length(colorEv))+1}, tev{i},zeros(1,length(tev{i})), colorEv{mod(i,length(colorEv))+1});
end
legend('E_H[\lambda(t)]','\lambda(t)', 'events')