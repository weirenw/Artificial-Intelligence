%Gibbs Sampling in a Bayesian Network

%parameter
postbc=zeros(1,3);

%initialization
A=unidrnd(4);
B=unidrnd(4);
C=unidrnd(4);
r=rand;
if r<=0.4+0.1*(B-C)
    BC=1;
elseif r<=0.4+0.1*(B-C)+0.2
    BC=2;
else
    BC=3;
end

%iterations
for i=1:100000
    %sample A
    PA=zeros(1,4);
    for j=1:4
        PA(j)=0.4+0.1*(j-B);    %proportional to Pr(A=j)
    end
    PAT=sum(PA);
    r=rand;
    if r<=PA(1)/PAT
        A=1;
    elseif r<=(PA(1)+PA(2))/PAT
        A=2;
    elseif r<=(PA(1)+PA(2)+PA(3))/PAT
        A=3;
    else
        A=4;
    end
    
    %sample B
    PB=zeros(1,4);
    if BC==1
        for j=1:4
            PB(j)=(0.4+0.1*(A-j))*(0.4+0.1*(j-C));    %proportional to Pr(B=j)
        end
    elseif BC==2
        for j=1:4
            PB(j)=0.4+0.1*(A-j);    %proportional to Pr(B=j)
        end
    else
        for j=1:4
            PB(j)=(0.4+0.1*(A-j))*(0.4+0.1*(C-j));    %proportional to Pr(B=j)
        end
    end 
    PBT=sum(PB);
    r=rand;
    if r<=PB(1)/PBT
        B=1;
    elseif r<=(PB(1)+PB(2))/PBT
        B=2;
    elseif r<=(PB(1)+PB(2)+PB(3))/PBT
        B=3;
    else
        B=4;
    end
    
    %sample C
    PC=zeros(1,4);
    if BC==1
        for j=1:4
            PC(j)=0.4+0.1*(B-j);    %proportional to Pr(C=j)
        end
    elseif BC==2
        PC=ones(1,4);
    else
        for j=1:4
            PC(j)=0.4+0.1*(j-B);    %proportional to Pr(B=j)
        end
    end 
    PCT=sum(PC);
    r=rand;
    if r<=PC(1)/PCT
        C=1;
    elseif r<=(PC(1)+PC(2))/PCT
        C=2;
    elseif r<=(PC(1)+PC(2)+PC(3))/PCT
        C=3;
    else
        C=4;
    end
    
    %sample BC
    r=rand;
    if r<=0.4+0.1*(B-C)
        BC=1;
    elseif r<=0.4+0.1*(B-C)+0.2
        BC=2;
    else
        BC=3;
    end
    
    %count
    postbc(BC)=postbc(BC)+1;
    
    %display results
    if i==1
        display(postbc/1);
    elseif i==1000
        display(postbc/1000);
    elseif i==10000
        display(postbc/10000);
    elseif i==100000
        display(postbc/100000);
    end
end



