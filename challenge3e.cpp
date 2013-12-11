#include <iostream>
#include <sstream>
#include <vector>
#include <map>
#include <algorithm>
#include <cstdlib>
#include <cstdio>
#include <cstring>
#include <unistd.h>
#include <stdexcept>



#define likely(x)       __builtin_expect((x),1)
#define unlikely(x)     __builtin_expect((x),0)

using namespace std;

const int lowest_price = 10;
const int million = 1000*1000;
const int bufsize = 8192 * 1000;
char buf[bufsize];
int count_and_offset[million + 1];

/// used for sorting.
int compare(const void *a, const void *b)
{
  return (*(int *)a - *(int *)b);
}

class Campaign {
private:
  int N, D;
  int num_unique;
  vector<int> price_list; /// list of item prices
  //  vector<int> count_and_offset; /// how many items for a given count
  vector<int> cprices; /// campaign prices list.
  vector<int> cp_sorted; /// same list as cprices, but sorted.
  map<int, int> best_price; /// record best solution for each campaign price.
  inline  int find_best_price(int cp); /// main algorithm
  inline char *get_line();
  void precompute();
public:
  Campaign();
  ~Campaign();
  /// read data from stdin and prepare internal structures.
  void read_from_stdin();
  /// loops over all campaign prices calling find_best_price(cp)
  void find_best_prices();
  /// dispays result.
  void print_best_prices();
};

Campaign::Campaign()
  :N(0), D(0), num_unique(1),
   price_list(vector<int>()),
   //   count_and_offset(vector<int>(million + 1, 0)),
   cprices(vector<int>()),
   cp_sorted(vector<int>()),
   best_price(map<int, int>())
{
}

Campaign::~Campaign()
{
}

inline char *Campaign::get_line()
{
  static char* ptr = buf;
  char *p = ptr;
  char *end = index(p, '\n');
  *end = '\0';
  ptr = end + 1;
  return p;
}

void Campaign::read_from_stdin()
{
  int n, i, value;
  char *line;
  int pos = 0;
  while((n = read(0, buf + pos, bufsize - pos)) > 0){
    pos += n;
  }
  buf[pos] = '\n';
  buf[pos + 1] = '\0';
  line = get_line();
  char *space = index(line, ' ');
  N = strtol(line, NULL, 10);
  D = strtol(space, NULL, 10);
  price_list.resize(N + 1); /// add 0 as the first element.
  cprices.resize(D);
  cp_sorted.resize(D);
  price_list[0] = 0;

  /// read item prices.
  for(i = 0; i < N; i++){
    line = get_line();
    value = strtol(line, NULL, 10);
    if(likely(!count_and_offset[value])){
      count_and_offset[value] = 1;
      price_list[num_unique] = value;
      num_unique++;
    }else{
      count_and_offset[value]++;
    }
  }

  /// read campaign prices.
  for(i = 0; i < D; i++){
    line = get_line();
    value = strtol(line, NULL, 10);
    cp_sorted[i] = value;
    cprices[i] = value;
  }

  /// sort price_list and cp_sorted
  precompute();
}

void Campaign::precompute()
{
  qsort(cp_sorted.data(), D, sizeof(int), compare);
  qsort(price_list.data(), num_unique, sizeof(int), compare);
}



int Campaign::find_best_price(int cp)
{
  int candidate = 0;
  int lowlimit = max(cp / 2, (int)lowest_price);
  /// possible largest value for the larger price.
  int larger = cp - lowest_price;
  /// price_list[1] ... price_list[num_unique - 1] are valid prices.
  const vector<int>::iterator i1 = price_list.begin() + 1;
  const vector<int>::iterator i2 = price_list.begin() + num_unique;
  
  /// possible location for larger
  vector<int>::iterator i = lower_bound(i1, i2, larger);
  /// buf if it is not in price_list, use the next lower value.
  if(!count_and_offset[larger]){
    --i;
  }
  /// looping over larger.
  /// larger must be less than equal lowlimit(=10),
  /// must be in the price_list range,
  /// and once we find the best candidate solution which is equal to cp,
  /// we don't have to calculate further.
  while(larger >= lowlimit && candidate != cp && i != price_list.begin()){
    /// larger price.
    larger = *i;
    /// trial value for smaller price.
    int smaller = cp - larger;
    /// if smaller is not on the price_list, or, it is on the list but
    /// smaller happens to be same with larger and count_and_offset is 1
    /// (means smaller and larger are same item), we need to look for the
    /// next lower value for smaller.
    if(likely(!count_and_offset[smaller]) || 
       (count_and_offset[smaller] == 1 && cp == 2 * larger)){
      smaller = *(lower_bound(i1, i, smaller) - 1);
    }
    /// if smaller ends up in being unacceptably small, that means
    /// there is no possible pair for this (larger, small) pair.
    /// so we check next larger.
    if(unlikely(smaller < lowest_price)){
      --i;
      continue;
    }
    /// valid (larger, smaller) pair found. compare with the maximum so far.
    candidate = max(smaller + larger, candidate);
    /// and check for next larger.
    --i;
  }
  /// all possible larger value checked. return what we've got.
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
  stringstream output;
  for(int day = 0; day < D; day++){
    output << best_price[cprices[day]] << "\n";
  }
  cout << output.str();
}

int main(int argc, char **argv)
{
  Campaign c1;
  c1.read_from_stdin();
  c1.find_best_prices();
  c1.print_best_prices();
  return 0;
}
