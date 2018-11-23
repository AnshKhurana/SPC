#include <bits/stdc++.h>
#include <string>
using namespace std;
int main()
{
    int t;
    cin>>t;
    int n;
    string s;
    int xmin, xmax;
    while(t--)
    {
        cin>>s;
        n = s.length();
        vector <pair <int, int> > ranges;
        for (int i = 0; i < n; ++i)
        {
            if (s[i]=='.')
            {
                ranges.push_back(make_pair(-1,-1));
            }
            else
            {
                xmin = max(0, i-(s[i] - 48));
                xmax = min(n, i + (s[i] - 48));
                ranges.push_back(make_pair(xmin, xmax));
            }
        }
        int prev_max = -1, cur_min;
        int done = 1;
        for (auto it = ranges.begin(); it != ranges.end(); it++)
        {
            if (it->first == -1)
            {
                continue;
            }
            else
            {
                cur_min = it->first;
                
                if (cur_min <= prev_max)
                {
                    cout<<"unsafe"<<endl;
                    done = 0;
                    break;
                }
                else
                {
                    prev_max = it->second;
                }
            }
        }
        if (done)
        {
            cout<<"safe"<<endl;
        }
    }
    return 0;
}