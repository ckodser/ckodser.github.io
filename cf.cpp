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

const ll maxn=3e5+500;
const ll inf=1e9+800;
const ll mod=1e9+7;

bool ok[maxn];
ll be_koj[maxn];
ll amel[maxn];
ll dp[maxn];
vector<ll> gg[maxn];


void is_some_number_exzits_that_gcd_of_that_with(ll j,/* is*/ll i){
	
}
int main(){
	ios_base::sync_with_stdio(0);
	cin.tie(0);
	cout.tie(0);

	for(ll i=2;i<maxn;i++){
		if(amel[i]==0){
			amel[i]=i;
			for(ll j=2*i;j<maxn;j+=i){
				amel[j]=i;
			}
		}
	}
	be_koj[1]=1;
	for(ll i=2;i<maxn;i++){
		if(i%(amel[i]*amel[i])==0){
			be_koj[i]=be_koj[i/amel[i]];
		}else{
			be_koj[i]=be_koj[i/amel[i]]*amel[i];
		}
	}
	for(ll i=2;i<maxn;i++){
		ll a=i;
		while(a!=1){
			gg[i].pb(a/be_koj[a]);
			a=be_koj[a];
		}
	}
	ll n;
	cin>>n;
	for(ll i=0;i<n;i++){
		ll v;
		cin>>v;
		v=be_koj[v];
		ok[v]=1;
	}
	for(ll i=1;i<maxn;i++){
		if(ok[i]){
			for(ll j=i*2;j<maxn;j+=i){
				ok[j]=0;
			}
		}
	}
	for(ll i=maxn-2;i>=1;i--){
		dp[i]=inf;
		if(ok[i]){
			dp[i]=1;
		}
		for(ll j=2*i;j<maxn;j+=i){
			ll k=j/i;
			if(is_some_number_exzits_that_gcd_of_that_with(j,i)){
				dp[i]=min(dp[i],dp[j]+1);
			}
		}
	}
	cout<<dp[1];
}























