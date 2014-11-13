#include <iostream>
#include <math.h>
using namespace std;
int main()
{
char a;
cin>>a;
if('a'<=a&&a<='z') cout<<"lower-case letter";
if('A'<=a&&a<='Z') cout<<"upper-case letter";
if('0'<=a&&a<='9') cout<<"Number!!!";
    return 0;
}
