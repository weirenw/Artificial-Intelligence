A = imread('party_spock.png');
[row,col] = size(A);
K = 3;%compoments number
ms = zeros(1,K);
e = exp(1);
%random means
for i=1:K
   x = randi([1,row]);
   y = randi([1,col]);
   ms(i) = A(x,y);
end

%EM Algortihm
sigma = ones(1,K);
fai = ones(1,K)./K;%weight for each gaussian 
lnp = zeros(1,1);
gamma=zeros(row,col,K);
lnp(2) = intmax;
t=2;
while(abs(lnp(t)-lnp(t-1)>500))
    %E Step
    Insum = zeros(row,col,K);
    for i=1:row
        for j=1:col
            msCur = ms;
            sigmaCur = sigma;
            faiCur = fai;
            rankCur = zeros(1,K);
            for cmp = 1:K
                rankCur(cmp) = find(log(faiCur)-A(i,j)-msCur.^2./(2*(sigmaCur).^2)==max(log(faiCur)-A(i,j)-msCur.^2./(2*(sigmaCur).^2)));
                if(cmp==1)
                    Insum(i,j,k) = log(faiCur(rankij(cmp)))-0.5*log(2*p*sigma(rankCur(cmp))^2)-(A(i,j)-ms(rankCur(cmp))).^2./(2*(sigma(rankCur(cmp)))^2);
                else
                    Insum(i,j,k) = Insum(i,j,k-1)+log(1+e.^(log(faiCur(rankij(cmp)))-0.5*log(2*p*sigma(rankCur(cmp))^2)-(A(i,j)-ms(rankCur(cmp))).^2./(2*(sigma(rankCur(cmp)))^2)-Insum(i,j,k-1)));
                end
                msCur(rankCur(cmp))=[];
                sigmaCur(rankCur(cmp))=[];
                faiCur(rankCur(cmp))=[];
            end
        end
    end
    N=zeros(1,K);
    for cmp = 1:K
        gamma(:,:,cmp) = e.^(log(fai(cmp))-0.5*log(2*pi*sigma(cmp)^2)-(A(:,:)-ms(cmp)).^2./(2*(sigma(cmp))^2)-Insum(:,:,cmp))
        N(cmp) = sum(sum(gamma(:,:,cmp)));
    end
    
    %M step
    for cmp = 1:K
        ms(cmp)=sum(sum(gamma(:,:,cmp).*A(:,:)))/N(cmp);
        sigma(cmp)= sqrt(sum(sum(gamma(:,:,cmp).*(A(:,:)-ms(cmp)).*(A(:,:)-ms(cmp))))/N(cmp));
        fai(cmp) = N(cmp)/(row*col);
    end
    t=t+1;
    lnp(t)=sum(sum(Insum(:,:,K)));
end
            
                