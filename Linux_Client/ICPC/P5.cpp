#include <bits/stdc++.h>

using namespace std;

bool is_full(string ans[4])
{
    bool full = true;
    for (int i = 0; i < 4; ++i)
    {
        if (ans[i].find('a') == string::npos)
        {
            continue;
        }
        else
        {
            full = false;
        }
    }

    return full;
}

string* insert_column(int i, string word, string ans[4])
{
    string res[4];
    res = ans;
    if (ans[0][i] == 'a' || ans[0][i] == word[0] && ans[1][i] = 'a' || ans[1][i] == word[1] && ans[2][i] == 'a' || ans[2][i] == word[2] && ans[3][i] == 'a' || ans[3][i] == word[3])
    {
        res[0][i] = word[0];
        res[1][i] = word[1];
        res[2][i] = word[2];
        res[3][i] = word[3];
        return res;
    }
    else
        return ans;
}
string* insert_row(int i, string word, string ans[4])
{
    string res[4];
    if (ans[i][0] == 'a' || ans[i][0] == word[0] && ans[i][1] = 'a' || ans[i][1] == word[1] && ans[i][2] == 'a' || ans[i][2] == word[2] && ans[i][3] == 'a' || ans[i][3] == word[3])
    {
        res[i] = word;
        return res;
    }
    else
        return ans;   
}

string 

bool check_equal(string a[4], string b[4])
{
    bool x = true;
    for (int i = 0; i < 4; ++i)
    {
        if (a[i]  == b[i])
        {
            continue;
        }
        else
            x = false;
    }
    return x;

}

string* solution(string ans[4], set<string> words)
{
    string cur_word = *(words.begin());
    words.erase(words.begin());
    for (int i = 0; i < 4; ++i)
    {
        string cur[4] = insert_row(i, word, ans);
    if (cur == ans)
    {
        continue;
    }
    else
    {
        if(is_full(cur))
        {
            if(check_soln(cur, words))
            {
                return cur;
            }
            else
                return ans;
        }
        else
        {
            return solution(cur, words);
        }   
    }
    }

    for (int i = 0; i < 4; ++i)
    {
        string cur[4] = insert_column(i, word, ans);
    if (check_equal(cur, ans))
    {
        continue;
    }
    else
    {
        if(is_full(cur))
        {
            if(check_soln(cur, words))
            {
                return cur;
            }
            else
                return ans;
        }
        else
        {
            return solution(cur, words);
        }   
    }
    }
    
}

int main()
{
    int n, t;
    cin>>t;
    bool found = false;
    set <string> words;
    string ans[4] = {"aaaa"}; 
    string def[4] = {"grid", "snot", "poss", "ible"};
    string word;
    string rev_word;
    while(t--)
    {
        cin>>n;
        for (int i = 0; i < n; ++i)
        {
            cin>>word;
            words.insert(word);
        }
        for (auto it = words.begin(); it != words.end(); ++it)
        {   
            word = *it;
            rev_word = reverse(word.begin(), word.end());
            bool is_in = set.find(rev_word) != set.end();
            if (is_in)
            {
               words.erase(rev_word);
            }
        }
        if (words.size() > 16)
        {
            cout<<def<<"\n";
            continue;
        }
    
        ans = solution(ans, words, found);
        if (found)
        {
            cout<<ans<<"\n";
        }
        else
        {
            cout<<def<<"\n";
        }
        
    }

    return 0;
}