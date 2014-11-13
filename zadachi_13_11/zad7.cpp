#include <iostream>
#include <math.h>
using namespace std;
int main()
{
int a,b,mini,maxi,brmax=1,brmin=1,br;
cout<<"Broj: ";
cin>>br;
cin>>a;
mini=a;
maxi=a;
for(int i=2;i<br+1;i++){
cin>>b;
if(b>maxi) {
maxi=b; brmax=i;
}
if(b<mini){
mini=b; brmin=i;
}
}
cout<<brmin<<" "<<mini<<endl;
cout<<brmax<<" "<<maxi<<endl;
    return 0;
}

