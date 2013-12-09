#include <iostream>
#include <vector>
#include <map>
#include <algorithm>
#include <cstdlib>
#include <stdexcept>

#define likely(x)       __builtin_expect((x),1)
#define unlikely(x)     __builtin_expect((x),0)

using namespace std;

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
  map<int, int> multiplicity;
  vector<int> cprices; /// campaign prices list.
  vector<int> cp_sorted; /// same list, but sored.
  map<int, int> best_price;
  inline  int find_best_price(int cp);
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
  /// read item prices.
  price_list[0] = 0;
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
  cout << "i = " << i - price_list.begin() << "\n";
  if(unlikely(not_registered(larger))){
    --i;
    cout << "i adjusted: " << i - price_list.begin() << "\n";
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
  Campaign c1;
  c1.read_from_stdin();
  c1.find_best_prices();
  c1.print_best_prices();
  return 0;
}
