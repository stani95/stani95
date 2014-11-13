#include <iostream>
#include <math.h>
using namespace std;
int main()
{
int p;
int br=0;
cin>>p;
for(int i=2;i<p;++i){
if(p%i==0) br=1;
}
if(br==0) cout<<"prosto!";
else cout<<"systavno";
    return 0;
}
