%GibbsSampling

postbc = zeros(1,3);
%initialization
AQ = unidrnd(4);
BQ = unidrnd(4);
CQ = unidrnd(4);

if BQ<CQ
    BC = 1;
elseif BQ==CQ
    BC = 2;
else
    BC = 3;
end
%iterations
for i = 1:100000
    %sample A
    PAQ = zeros(1,4);
    for j = 1:4
        if j>BQ
            ab = 1;
        else
            ab = 0;
        end
    
        if j==CQ
           ac = 1;
        else 
            ac = 0;
        end
        
        PAQ(j) = ab*ac;
    end
    PSA = sum(PAQ);
    r = rand;
    if(r<=PAQ(1)/PSA)
        AQ=1;
    elseif(r<=(PAQ(1)+PAQ(2))/PSA)
        AQ=2;
    elseif(r<=(PAQ(1)+PAQ(2)+PAQ(3))/PSA)
        AQ=3;
    else
        AQ=4;
    end
    
    %sample B
    PBQ = zeros(1,4);
    for j = 1:4
        if(AQ>j)
            ab = 1;
        else 
            ab = 0;
        end
        
        if BC==1
            if(j<CQ)
                bc =1;
            else 
                bc = 0;
            end
        elseif BC==2
            if(j==CQ)
                bc =1;
            else
                bc =0;
            end
        else
            if(j>CQ)
                bc=1;
            else
                bc=0;
            end
        end
        PBQ(j) = ab*bc;
    end
    PSB = sum(PBQ);
    r = rand;
    if(r<=PBQ(1)/PSB)
        BQ=1;
    elseif(r<=(PBQ(1)+PBQ(2))/PSB)
        BQ=2;
    elseif(r<=(PBQ(1)+PBQ(2)+PBQ(3))/PSB)
        BQ=3;
    else
        BQ=4;
    end
    
    %sample C
    
    PCQ = zeros(1,4);
    for j = 1:4
        if j==AQ
            ac = 1;
        else
            ac = 0;
        end
        
        if BC==1
            if(j>BQ)
                bc =1;
            else 
                bc = 0;
            end
        elseif BC==2
            if(j==BQ)
                bc =1;
            else
                bc =0;
            end
        else
            if(j<BQ)
                bc=1;
            else
                bc=0;
            end
        end
        PCQ(j) = ac*bc;
    end
    
    PSC=sum(PCQ);
    r = rand;
    if(r<=PCQ(1)/PSC)
        CQ=1;
    elseif(r<=(PCQ(1)+PCQ(2))/PSC)
        CQ=2;
    elseif(r<=(PCQ(1)+PCQ(2)+PCQ(3))/PSC)
        CQ=3;
    else
        CQ=4;
    end
    
    %sample BC
     if(BQ<CQ)
         BC = 1;
     elseif BQ==CQ
         BC = 2;
     else
         BC = 3;
     end
     
     postbc(BC) = postbc(BC)+1;
     if i==10
        display(postbc/10);
     elseif i==1000
        display(postbc/1000);
     elseif i==10000
        display(postbc/10000);
     elseif i==100000
        display(postbc/100000);
     end
end

    
        
 
            
        
    
        
        
        
        
    
       
    
