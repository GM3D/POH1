#include <iostream>
#include <cstdlib>
#include <vector>
#include <map>
#include <sys/time.h>
#include <cstdio>

timeval t[10];

using namespace std;

class Campaign {
private:
  int N, D;
  const int lowest_price;
  const int million;
  int *price_list;
  int *multiplicity;
  int *cprices; /// campaign prices list.
  int *cp_sorted; /// same list, but sored.
  /// closest possible sum of two items, computed for each of
  /// campaign price.
  int *best_price;
  bool not_registered(int value);
  void insort(int *v, int value);
  int find_best_price(int cp);
public:
  Campaign();
  ~Campaign();
  void read_from_stdin();
  void find_best_prices();
  void print_best_prices();
};

Campaign::Campaign()
  :N(0), D(0), 
   lowest_price(10), million(100000);
  ,price_list(NULL), multiplicity(NULL),
   prices(NULL), cp_sorted(NULL),
   best_price(NULL)
{
}

Campaign::~Campaign()
{
  if(price_list) delete[] price_list;
  if(multiplicity) delete[] multiplicity;
  if(prices) delete[] prices;
  if(cp_sorted) delete[] cp_sorted;
  if(best_price) delete[] best_price;
}

void Campaign::insort(vector<int>&v, int value)
{
  vector<int>::iterator i = lower_bound(v.begin(), v.end(), value);
  v.insert(i, value);
}

bool Campaign::not_registered(int value)
{
  return multiplicity.find(value) == multiplicity.end();
}

void Campaign::read_from_stdin()
{
  string line;
  int i, value;

  /// read header and resize vectors accordingly.
  getline(cin, line);
  int space = line.find(' ');
  N = strtol(line.c_str(), NULL, 10);
  D = strtol(line.c_str() + space, NULL, 10);
  price_list = new int[N];
  multiplicity = new int[million];
  cprices = new int[D];
  cp_sorted = new int[D];
  /// read price data
  for(i = 0; i < N; i++){
    getline(cin, line);
    value = strtol(line.c_str(), NULL, 10);
    if(not_registered(value)){
      multiplicity[value] = 1;
      insort(price_list, value);
    }else{
      multiplicity[value]++;
    }
  }

  /// read campaign prices.
  for(i = 0; i < D; i++){
    getline(cin, line);
    value = strtol(line.c_str(), NULL, 10);
    insort(cp_sorted, value);
    cprices[i] = value;
  }
}

int Campaign::find_best_price(int cp)
{
  int candidate = 0;
  int lowlimit = max(cp / 2, (int)lowest_price);
  int larger = cp - lowest_price;
  vector<int>::iterator i 
    = lower_bound(price_list.begin(), price_list.end(), larger);
  if(not_registered(larger)){
    larger = *(--i);
  }
  while(larger >= lowlimit && candidate != cp){
    int smaller = cp - larger;
    if(not_registered(smaller) || 
       (multiplicity[smaller] == 1 && cp == 2 * larger)){
      smaller 
	= *(lower_bound(price_list.begin(), price_list.end(), smaller) - 1);
    }
    if(smaller < lowest_price){
      larger = *(--i);
      continue;
    }
    candidate = max(smaller + larger, candidate);
    larger = *(--i);
  }
  return candidate;
}

void Campaign::find_best_prices()
{
  int last_best = 1;
  int c;
  for(int i = D - 1; i >= 0; i--){
    c = cp_sorted[i];
    if(last_best == 0){
      best_price[c] = 0;
    }else{
      best_price[c] = last_best = find_best_price(c);
    }
  }
}

void Campaign::print_best_prices()
{
  for(int day = 0; day < D; day++){
    cout << best_price[cprices[day]] << "\n";
  }
}

int main(int argc, char **argv)
{
  gettimeofday(&t[0], NULL);
  Campaign c1;
  gettimeofday(&t[1], NULL);
  c1.read_from_stdin();
  gettimeofday(&t[2], NULL);
  c1.find_best_prices();
  gettimeofday(&t[3], NULL);
  c1.print_best_prices();
  gettimeofday(&t[4], NULL);
  for(int i = 0; i < 9; i++){
    fprintf(stderr, "t[%d] - t[%d] = %ld usec.\n", i+1, i,
	    (t[i+1].tv_sec - t[i].tv_sec) * 1000000
	    + t[i+1].tv_usec - t[i].tv_usec);
  }
  return 0;
}
