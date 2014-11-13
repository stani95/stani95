#include <iostream>
#include <math.h>
using namespace std;
int main()
{
int a, ed,des,stot,hil;
cin>>a;
ed=a%10;
des=(a/10)%10;
stot=(a/100)%10;
hil=a/1000;
cout<<hil<<endl<<stot<<endl<<des<<endl<<ed<<endl;
    return 0;
}
