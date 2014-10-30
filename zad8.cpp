#include <iostream>
#include <math.h>
using namespace std;
int main()
{
int a,b,c,d;
cout<<"Enter the coordinates of point A"<<endl;
cin>>a;
cin>>b;
cout<<"Enter the coordinates of point B"<<endl;
cin>>c;
cin>>d;
cout<<"Distance is "<<sqrt(pow(a-c,2)+pow(b-d,2))<<endl;
    return 0;
}
