N = 6;
dag = zeros(N,N);
AQ =1; BQ =2; CQ = 3;
AB =4; AC=5; BC=6;
dag([AQ BQ],AB) = 1;
dag([AQ,CQ], AC) = 1;
dag([BQ,CQ], BC) = 1;

discrete_nodes = 1:N;
node_sizes = [4 4 4 3 3 3];
onodes = 6;
bnet = mk_bnet(dag, node_sizes,'names', {'AQ', 'BQ', 'CQ', 'AB', 'AC', 'BC'}, 'discrete', discrete_nodes, 'observed', onodes);

bnet.CPD{AQ} = tabular_CPD(bnet, AQ, [0.25 0.25 0.25 0.25]);
bnet.CPD{BQ} = tabular_CPD(bnet, BQ, [0.25 0.25 0.25 0.25]);
bnet.CPD{CQ} = tabular_CPD(bnet, CQ, [0.25 0.25 0.25 0.25]);
CPT=zeros(4,4,3);
for i=1:4
    for j=1:4
        if i>j
            CPT(i,j,1)=1;
        else
            CPT(i,j,1)=0;
        end
        if i==j
            CPT(i,j,2)=1;
        else
            CPT(i,j,2)=0;
        end
        if i<j
            CPT(i,j,3)=1;
        else
            CPT(i,j,3)=0;
        end
    end
end
CPT=reshape(CPT, [1 48]);
bnet.CPD{AB} = tabular_CPD(bnet, AB, CPT);

bnet.CPD{AC} = tabular_CPD(bnet, AC, CPT);

                                  
bnet.CPD{BC} = tabular_CPD(bnet, BC, CPT);
                                  
engine = jtree_inf_engine(bnet);
evidence = cell(1,N);
evidence{AB} = 3;
evidence{AC} = 2;
[engine, loglik] = enter_evidence(engine, evidence);
marg = marginal_nodes(engine, BC);
marg.T


