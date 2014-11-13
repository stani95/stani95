#include <iostream>
#include <math.h>
using namespace std;
int main()
{
int a;
cin>>a;
do{
cout<<a%2;
a=a/2;
}
while(a>0);
    return 0;
}
