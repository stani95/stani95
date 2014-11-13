#include <iostream>
#include <math.h>
using namespace std;
int main()
{
int a, ed=0,des=0,stot=0,hil=0,desetoh=0,stoh=0;
cin>>a;
ed=a%10;
des=(a/10)%10;
stot=(a/100)%10;
hil=(a/1000)%10;
desetoh=(a/10000)%10;
stoh=a/100000;
if(ed==stoh&&des==desetoh&&stot==hil) cout<<a<<" is a palindrom!!!"<<endl;
else cout<<a<<" is not a palindrom!!!"<<endl;
    return 0;
}
