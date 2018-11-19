#include<iostream>
#include<fstream>
#include<sstream>
#include<cstdio>
#include<string>
#include<set>
#include<map>
#include<stack>
#include<queue>
#include<vector>
using namespace std;
set<string> ns;
map<string,int> nm;
const int maxn=100000;
int n;
vector<int> m[maxn];
double CB[maxn];
string file;

void prepare()
{
	ifstream in("news.json.txt");
	ofstream ou("prepare.txt");
    string s,tmp;
    char c;
    while(!in.eof())
    {
    	in>>c;
    	if(!in.eof()&&c!=10&&c!=32&&c!=34)
    	{
    		if(c==',')c=32;
    		s+=c;
		}
		
	}
	
	string::size_type l=0,r=0;
	string::size_type ll,rr;
	int sum=0;
	while(true)
	{
		l=s.find("Entity_Person",r);
		if(l==string::npos)break;
		r=s.find(']',l);
		tmp=s.substr(l+15,r-l-15);	
		if(sum==0)
		{
			sum++;continue;
		}
		ou<<tmp<<endl;
		sum++;	
	}
	
	in.close();
	ou.close();
}

void insertName()
{
	ifstream in("prepare.txt");
	char line[10000];
	string s;	
	while(!in.eof())
    {
    	in.getline(line,10000);
    	string flag(line);
    	if(flag.size()==0)continue;
    	stringstream st(line);
    	while(st>>s)
    	{
    		if(s.size()==0)break;
    		ns.insert(s);
		}
	}
	in.close();
	
	set<string>::iterator pos;
    int num=0;
    for(pos=ns.begin();pos!=ns.end();++pos)
    {
    	nm.insert(make_pair(*pos,num));
    	++num;
	}
}

void createGraph()
{
	ifstream in("prepare.txt");
	char line[10000];
	string s;
	while(true)
    {
    	in.getline(line,10000);
    	string flag(line);
    	if(flag.size()==0)break;
    	stringstream st(line);
    	vector<int> tmp;
    	while(st>>s)
    	{
    		if(s.size()==0)break;
    		tmp.push_back(nm[s]);
		}
		for(int i=0;i<tmp.size();++i)
		for(int j=i+1;j<tmp.size();++j)
		{
			int x=tmp[i],y=tmp[j];
			if(m[x].size()==0)
			{
				m[x].push_back(y);m[y].push_back(x);
			}
			else{
				int k;
				for(k=0;k<m[x].size();++k)
				if(m[x][k]==y)break;
				if(k!=m[x].size())
				{
					m[x].push_back(y);m[y].push_back(x);
				}
			}	
		}
	}
	in.close();
	
	n=ns.size();
}
void excute()
{
    for(int i = 0 ;i < n; i++)
	{
		CB[i] = 0;
	}
	for(int s = 0; s < n; s++)
	{
	  vector< vector<int> > p(n);
	  stack<int> S;
	  queue<int> Q;
    
	  double a[maxn];
   	  for(int h = 0 ; h < n; h++)
	  {
		a[h] = 0.0;
	  }
	  a[s] = 1.0;
	  int b[maxn];
	  for(int e = 0 ; e < n; e++)
	  {
		b[e] = -1;
	  }
	  b[s] = 0;

	  Q.push(s);

	  while(!Q.empty())
	  {
		  int v = Q.front();
		  Q.pop();
		  S.push(v);
		  for(int jj = 0; jj < m[v].size() ;jj++)
		    {
		  	int w=m[v][jj];
			if(b[w] < 0)
				{
					Q.push(w);
					b[w] = b[v] +1;
				}
				   
				if(b[w] == b[v] +1)
				{
					a[w] = a[w] +a[v];
					p[w].push_back(v);
				}
		   }
	   }
	  double sum[maxn];
	  int v;
	  for(v = 0; v < n; v++)
	  {
		  sum[v]=0;
	  }
	  while(!S.empty())
	  {
		  int w = S.top();
		  S.pop();
		  
		  for(vector<int>::iterator ix = p[w].begin(); ix != p[w].end();++ix)
		 {
			 sum[*ix] = sum[*ix] + (a[*ix]/a[w])*(1.0+sum[w]);
		 }
		  if(w != s)
			  CB[w] = CB[w] + sum[w]/2;
	  }
	} 
}

void print()
{
	ofstream ou("result.txt");
	set<string>::iterator pos;
    int num=0;
    for(pos=ns.begin();pos!=ns.end();++pos)
    {
    	ou<<*pos<<" "<<CB[num]<<endl;
    	++num;
	}
	ou.close();
}
int main()
{
	prepare();
	insertName();
	createGraph();
    excute();
	print();	
	return 0;	
}
