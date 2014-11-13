%Metropolis-Hastings Sampling in a Bayesian Network %parameter
iter=0; postbc=zeros(1,3);
%initialization
A=2;
B=1;
C=2;
BC=3;
%iterations
for i=1:100000
    %proposal distribution
    A2=unidrnd(4);
    B2=unidrnd(4);
    C2=unidrnd(4);
    BC2=unidrnd(3);
    %acceptance probability
    if BC==1 
         pi=(0.3+0.1*(A-B))*(0.4-(A-C)*(A-C)/16.0)*(0.3+0.1*(B-C));
    elseif BC==2
        pi=(0.3+0.1*(A-B))*(0.4-(A-C)*(A-C)/16.0)*(0.4-(B-C)*(B-C)/16.0);
    else
        pi=(0.3+0.1*(A-B))*(0.4-(A-C)*(A-C)/16.0)*(0.3+(B-C)*(B-C)/16.0-0.1*(B-C));
    end
    
    if BC2==1
        pi2=(0.3+0.1*(A2-B2))*(0.4-(A2-C2)*(A2-C2)/16.0)*(0.3+0.1*(B2-C2)); 
    elseif BC2==2
        pi2=(0.3+0.1*(A2-B2))*(0.4-(A2-C2)*(A2-C2)/16.0)*(0.4-(B2-C2)*(B2-C2)/16.0);
    else
        pi2=(0.3+0.1*(A2-B2))*(0.4-(A2-C2)*(A2-C2)/16.0)*(0.3+(B2-C2)*(B2-C2)/16.0-0.1*(B2-C2));
    end
    r=rand;
    if r<=min(1,pi2/pi);
        A=A2; B=B2; C=C2; BC=BC2;
        postbc(BC2)=postbc(BC2)+1;
    else
        postbc(BC)=postbc(BC)+1;
    end
end