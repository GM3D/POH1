#include <iostream>
#include <cstdlib>
#include <vector>
#include <map>
#include <algorithm>
#include <stdexcept>
#include <cstdio>
#include <cstring>
#include <sys/time.h>

const int num_marks = 10;
timeval t[num_marks];

using namespace std;

#define likely(x)       __builtin_expect((x),1)
#define unlikely(x)     __builtin_expect((x),0)

inline int compare(const void *a, const void *b)
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
  vector<int> multiplicity;
  //  map<int, int> multiplicity;
  vector<int> cprices; /// campaign prices list.
  vector<int> cp_sorted; /// same list, but sored.
  map<int, int> best_price;
  inline int find_best_price(int cp);
  long counter[10];
  long counter1[10];
public:
  Campaign();
  ~Campaign();
  void read_from_stdin();
  void find_best_prices();
  void print_best_prices();
  void report_branch();
  void sort_data();
};

Campaign::Campaign()
  : lowest_price(10), million(1000000),
    N(0), D(0), num_unique(1),
    price_list(vector<int>()),
    multiplicity(vector<int>(million + 1, 0)),
    // multiplicity(map<int, int>()),
    cprices(vector<int>()),
    cp_sorted(vector<int>()),
    best_price(map<int, int>())
{
  for(int i = 0; i < 10; i++){
    counter[i] = counter1[i] = 0;
  }
}

Campaign::~Campaign()
{
}

void Campaign::read_from_stdin()
{
  int i, value;
  const int bufsize = 256;
  char *buf = new char[bufsize];
  /// read N, D and resize vectors accordingly.
  fgets(buf, bufsize, stdin);
  char *space = index(buf, ' ');
  N = strtol(buf, NULL, 10);
  D = strtol(space, NULL, 10);
  gettimeofday(&t[2], NULL);
  price_list.resize(N + 1); /// add 0 as the first element.
  cprices.resize(D);
  cp_sorted.resize(D);
  price_list[0] = 0;
  gettimeofday(&t[3], NULL);
  /// read item prices.
  for(i = 0; i < N; i++){
    fgets(buf, bufsize, stdin);
    value = strtol(buf, NULL, 10);
    if(likely(!multiplicity[value])){
      multiplicity[value] = 1;
      price_list[num_unique] = value;
      num_unique++;
      // counter[0]++;
      // counter1[0]++;
    }else{
      multiplicity[value]++;
      // counter[0]++;
    }
  }
  gettimeofday(&t[4], NULL);
  /// read campaign prices.
  for(i = 0; i < D; i++){
    fgets(buf, bufsize, stdin);
    value = strtol(buf, NULL, 10);
    cp_sorted[i] = value;
    cprices[i] = value;
  }
  delete[] buf;
}

void Campaign::sort_data()
{
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
  if(!multiplicity[larger]){
    --i;
    // counter1[1]++;
  }
  // counter[1]++;
  while(larger >= lowlimit && candidate != cp && i != price_list.begin()){
    larger = *i;
    int smaller = cp - larger;
    // counter[2]++;
    if(unlikely(!multiplicity[smaller]) || 
       (multiplicity[smaller] == 1 && cp == 2 * larger)){
      // counter1[2]++;
      smaller = *(lower_bound(price_list.begin() + 1, i, smaller) - 1);
    }
    if(unlikely(smaller < lowest_price)){
      --i;
      // counter[3]++;
      // counter1[3]++;
      continue;
    }else{
      // counter[3]++;
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
    // counter[4]++;
    if(unlikely(last_best == 0)){
      // counter1[4]++;
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

void Campaign::report_branch()
{  
  for(int i = 0; i < 10; i++){
    if(counter[i] > 0){
      float ratio = 100.0 * ((float)(counter1[i])) / counter[i];
      cout << "counter[" << i << "] true ratio = " << ratio << "% \n";
    }
  }
}

void report_time()
{
  for(int i = 0; i < num_marks - 1; i++){
    long elapsed 
      = (t[i+1].tv_sec - t[i].tv_sec) * 1000000
      + t[i+1].tv_usec - t[i].tv_usec;
    if(elapsed > 0){
      fprintf(stderr, "t[%d] - t[%d] = %ld usec.\n", i+1, i, elapsed);
    }
  }
}


int main(int argc, char **argv)
{
  gettimeofday(&t[0], NULL);
  Campaign c1;
  gettimeofday(&t[1], NULL);
  c1.read_from_stdin();
  gettimeofday(&t[5], NULL);
  c1.sort_data();
  gettimeofday(&t[6], NULL);
  c1.find_best_prices();
  gettimeofday(&t[7], NULL);
  c1.print_best_prices();
  gettimeofday(&t[8], NULL);
  //  c1.report_branch();
  report_time();
  return 0;
}
