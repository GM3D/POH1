#include <iostream>
#include <cstdlib>
#include <vector>
#include <map>
#include <algorithm>
#include <stdexcept>
#include <cstdio>
#include <sys/time.h>

timeval t[10];

using namespace std;

#define likely(x)       __builtin_expect((x),1)
#define unlikely(x)     __builtin_expect((x),0)

int compare(const void *a, const void *b)
{
  return (*(int *)a - *(int *)b);
}

class Campaign {
private:
  const int lowest_price;
  const int million;
  int N, D;
  int num_unique;
  vector<int> price_list;
  //  vector<int> multiplicity;
  map<int, int> multiplicity;
  vector<int> cprices; /// campaign prices list.
  vector<int> cp_sorted; /// same list, but sored.
  map<int, int> best_price;
  inline int find_best_price(int cp);
  inline bool not_registered(int value);
public:
  Campaign();
  ~Campaign();
  void read_from_stdin();
  void find_best_prices();
  void print_best_prices();
};

Campaign::Campaign()
  : lowest_price(10), million(1000000),
    N(0), D(0), num_unique(1),
    price_list(vector<int>()),
    //    multiplicity(vector<int>(million + 1, 0)),
    multiplicity(map<int, int>()),
    cprices(vector<int>()),
    cp_sorted(vector<int>()),
    best_price(map<int, int>())
{
}

Campaign::~Campaign()
{
}

void Campaign::read_from_stdin()
{
  string line;
  int i, value;
  /// read N, D and resize vectors accordingly.
  cin >> N >> D;
  price_list.resize(N + 1); /// add 0 as the first element.
  cprices.resize(D);
  cp_sorted.resize(D);
  price_list[0] = 0;
  /// read item prices.
  for(i = 0; i < N; i++){
    cin >> value;
    if(likely(not_registered(value))){
      multiplicity[value] = 1;
      price_list[num_unique] = value;
      num_unique++;
    }else{
      multiplicity[value]++;
    }
  }

  /// read campaign prices.
  for(i = 0; i < D; i++){
    cin >> value;
    cp_sorted[i] = value;
    cprices[i] = value;
  }

  /// sort price_list and cp_sorted
  qsort(cp_sorted.data(), D, sizeof(int), compare);
  qsort(price_list.data(), num_unique, sizeof(int), compare);
}



int Campaign::find_best_price(int cp)
{
  int candidate = 0;
  int lowlimit = max(cp / 2, (int)lowest_price);
  int larger = cp - lowest_price;
  const vector<int>::iterator i1 = price_list.begin() + 1;
  const vector<int>::iterator i2 = price_list.begin() + num_unique;
  vector<int>::iterator i = lower_bound(i1, i2, larger);
  if(unlikely(not_registered(larger))){
    --i;
  }
  while(larger >= lowlimit && candidate != cp && i != price_list.begin()){
    larger = *i;
    int smaller = cp - larger;
    if(unlikely(not_registered(smaller)) || 
       (multiplicity[smaller] == 1 && cp == 2 * larger)){
      smaller = *(lower_bound(price_list.begin() + 1, i, smaller) - 1);
    }
    if(unlikely(smaller < lowest_price)){
      --i;
      continue;
    }
    candidate = max(smaller + larger, candidate);
    --i;
  }
  return candidate;
}

void Campaign::find_best_prices()
{
  int last_best = 1;
  int c;
  for(int i = D - 1; i >= 0; i--){
    c = cp_sorted[i];
    if(unlikely(last_best == 0)){
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

bool Campaign::not_registered(int value)
{
  try{
    if(unlikely(multiplicity.at(value))) return false;
  }catch(const out_of_range e){
    return true;
  }
  return false;
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
