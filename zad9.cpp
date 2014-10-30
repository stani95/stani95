#include <iostream>
#include <math.h>
using namespace std;
int main()
{
int myAge,currentYear,compareYear;
cout<<"What is the current year?"<<endl;
cin>>currentYear;
cout<<"What is your age?"<<endl;
cin>>myAge;
cout<<"Enter a year in the future?"<<endl;
cin>>compareYear;
if(compareYear-currentYear+myAge>=150){
cout<<"You will be dead by then!!!"<<endl;
}
else cout<<"Your age will be "<<compareYear-currentYear+myAge<<endl;
    return 0;
}
