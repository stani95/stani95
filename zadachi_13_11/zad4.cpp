#include <iostream>
#include <math.h>
using namespace std;
int main()
{
int a, ed=0,des=0,stot=0,hil=0,desetoh=0,bc;
cout<<"1 - One digit number"<<endl<<"2 - Two digits numbers"<<endl<<"3 - Three digits number"<<endl<<"4 - Four digits number"<<endl<<"5 - Five digits number"<<endl;
cin>>bc;
cin>>a;
switch(bc){
case 1:
cout<<a<<endl;
break;
case 2:
ed=a%10;
des=a/10;
cout<<des<<endl<<ed<<endl;
break;
case 3:
ed=a%10;
des=(a/10)%10;
stot=a/100;
cout<<stot<<endl<<des<<endl<<ed<<endl;
break;
case 4:
ed=a%10;
des=(a/10)%10;
stot=(a/100)%10;
hil=a/1000;
cout<<hil<<endl<<stot<<endl<<des<<endl<<ed<<endl;
break;
case 5:
ed=a%10;
des=(a/10)%10;
stot=(a/100)%10;
hil=(a/1000)%10;
desetoh=a/10000;
cout<<desetoh<<endl<<hil<<endl<<stot<<endl<<des<<endl<<ed<<endl;
break;
}
    return 0;
}
