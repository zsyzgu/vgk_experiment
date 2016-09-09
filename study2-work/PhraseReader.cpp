#include <set>
#include <string>
#include <cstdio>
#include <iostream>

using namespace std;

string s;
set<string> distinct;

int main()
{
    freopen("phrases.txt", "r", stdin);
    freopen("words.csv", "w", stdout);
    while (cin >> s)
        distinct.insert(s);
    cout << "word,length" << endl;
    for(set<string>::iterator it = distinct.begin(); it != distinct.end(); ++it)
        cout << *it << "," << (*it).length() << endl;
    return 0;
}
