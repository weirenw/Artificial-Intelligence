%Bayesian Network Modeling and Inference
%09212014

%sturcture of the graph
N=6; 
dag=zeros(N,N);
A=1; B=2; C=3; AB=4; AC=5; BC=6;
dag(A,[AB AC])=1;
dag(B,[AB BC])=1;
dag(C,[AC BC])=1;

%size and type of each node
discrete_nodes=1:N;
node_sizes=[4 4 4 3 3 3];

%definition of the BN
bnet = mk_bnet(dag, node_sizes);

%parameters
bnet.CPD{A}=tabular_CPD(bnet, A, [0.25 0.25 0.25 0.25]);
bnet.CPD{B}=tabular_CPD(bnet, B, [0.25 0.25 0.25 0.25]);
bnet.CPD{C}=tabular_CPD(bnet, C, [0.25 0.25 0.25 0.25]);
CPT=zeros(4,4,3);
for i=1:4
    for j=1:4
        CPT(i,j,1)=0.3+0.1*(i-j);
        CPT(i,j,2)=0.4-(i-j)*(i-j)/16.0;
        CPT(i,j,3)=0.3+(i-j)*(i-j)/16.0-0.1*(i-j);
    end
end
CPT=reshape(CPT, [1 48]);
bnet.CPD{AB}=tabular_CPD(bnet, AB, CPT);
bnet.CPD{AC}=tabular_CPD(bnet, AC, CPT);
bnet.CPD{BC}=tabular_CPD(bnet, BC, CPT);

%inference
engine=jtree_inf_engine(bnet);
evidence=cell(1,N);
evidence{AB}=1;
evidence{AC}=2;
[engine, loglik]=enter_evidence(engine, evidence);
marg=marginal_nodes(engine, BC);
marg.T




