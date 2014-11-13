#include <iostream>
#include <math.h>
using namespace std;
int main()
{
int n;
char sym;
cin>>n;
cin>>sym;
for(int i=0;i<2*n-1;++i){
    if(i%2==0) cout<<sym;
    else cout<<" ";
}
cout<<endl;
    for(int i=1;i<n;++i){
        for(int j=0;j<2*n-1;++j){
            if(j==i) cout<<sym;
            else if(j==2*n-2-i) cout<<sym;
                else cout<<" ";
}
cout<<endl;
}
    return 0;
}

