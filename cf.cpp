#include <algorithm>
#include <bitset>
#include <complex>
#include <deque>
#include <exception>
#include <fstream>
#include <functional>
#include <iomanip>
#include <ios>
#include <iosfwd>
#include <iostream>
#include <istream>
#include <iterator>
#include <limits>
#include <list>
#include <locale>
#include <map>
#include <memory>
#include <new>
#include <numeric>
#include <ostream>
#include <queue>
#include <set>
#include <sstream>
#include <stack>
#include <stdexcept>
#include <streambuf>
#include <string>
#include <typeinfo>
#include <utility>
#include <valarray>
#include <vector>
#if __cplusplus >= 201103L
#include <array>
#include <atomic>
#include <chrono>
#include <condition_variable>
#include <forward_list>
#include <future>
#include <initializer_list>
#include <mutex>
#include <random>
#include <ratio>
#include <regex>
#include <scoped_allocator>
#include <system_error>
#include <thread>
#include <tuple>
#include <typeindex>
#include <type_traits>
#include <unordered_map>
#include <unordered_set>
#endif
 
#define ll int
#define pb push_back
#define FOR(i,a) for(ll i=0;i<(ll)a.size();i++)
#define ld long double
#define mp make_pair
#define F first
#define S second
#define pii pair<ll,ll> 

using namespace :: std;

const ll maxn=5e6;
const ll inf=1e9+800;
const ll mod=1e9+7;

ll fen[maxn];
pii ki[maxn];
ll ans[maxn];

void update_fen(ll x,ll v){
	for(x++;x<maxn;x+=(x&(-x))){
		fen[x]+=v;
	}
}
void update(ll x,pii a){
	ki[x]=a;
	update_fen(x,+1);
}
ll lower_fen(ll x){
	ll ans=0;
	for(ll i=21;i>=0;i--){
		if(fen[ans+(1<<i)]<x){
			x-=fen[ans+(1<<i)];
			ans+=(1<<i);
		}
	}
	return ans;//?? ans+1 ans-1;
}
pair<ll,pii> lower_b(ll x){
	ll a=lower_fen(x);
	return mp(a,ki[a]);
}
void clea(ll x){
	ki[x]=mp(0,0);
	update_fen(x,-1);
}
int main(){
	ll n,m;
	cin>>n>>m;
	for(ll i=1;i<=n;i++){
		update(m+i,mp(-1,i));
	}
	for(ll qw=0;qw<m;qw++){
		ll x,y;
		cin>>x>>y;
		pair<ll,pii>  b=lower_b(y);
		pii a=b.S;
		if(a.F!=-1 && a.F!=x){
			cout<<-1;
			return 0;
		}	
		a.F=x;
		clea(b.F);
		update(m-qw,a);
	}
	set<ll> st;
	for(ll i=1;i<=n;i++){
		st.insert(i);
		pii a=lower_b(i).S;
		ans[a.S]=a.F;
	}
	for(ll i=1;i<=n;i++){
		if(ans[i]!=-1){
			if(st.find(ans[i])==st.end()){
				cout<<-1;
				return 0;
			}
			st.erase(ans[i]);
		}
	}
	for(ll i=1;i<=n;i++){
		if(ans[i]==-1){
			ans[i]=(*st.begin());
			st.erase(st.begin());
		}
	}
	for(ll i=1;i<=n;i++){
		cout<<ans[i]<<' ';
	}
}























