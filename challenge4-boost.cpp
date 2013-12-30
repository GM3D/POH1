// challenge4-boost.cpp by GM3D ver 0.1
// to call from Python via boost.python

#include <boost/python.hpp>
#include <iostream>
#include <sstream>
#include <cstdlib>
#include <cstring>
#include <unistd.h>

using namespace std;

#define likely(x)       __builtin_expect((x),1)
#define unlikely(x)     __builtin_expect((x),0)

const int lowest_price = 10;
const int million = 1000*1000;
const int bufsize = 8192 * 1000;
const int max_days = 75;

char buf[bufsize];
int count_and_offset[million + 1];
int cprices[max_days];
int best_prices[max_days];

int digit[64] = {
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0, 0, 0,
};

class Campaign {
private:
  int N, D;
  inline int find_best_price(int cp);
  inline int get_next_valid_lower(int x);
  void pre_compute();
public:
  void read_from_stdin();
  void find_best_prices();
  void print_best_prices();
};

inline int Campaign::get_next_valid_lower(int x)
{
  int l = count_and_offset[x];
  if(l < 0) x += l;
  return x;
}

void Campaign::pre_compute()
{
  int offset = 0;
  for(int i = 0; i <= million; i++){
    if(count_and_offset[i] > 0){
      offset = 0;
    }else{
      count_and_offset[i] = offset;
    }
    offset--;
  }
}

void Campaign::read_from_stdin()
{
  int n, i, value;
  int pos = 0;
  while((n = read(0, buf + pos, bufsize - pos)) > 0){
    pos += n;
  }
  buf[pos] = '\n';
  buf[pos + 1] = '\0';
  char *space = index(buf, ' ');
  N = atoi(buf);
  D = atoi(space + 1);
  /// read item prices.
  char *src = index(space + 1, '\n') + 1;
  value = 0;
  i = 0;
  while(i < N){
    if(*src != '\n'){
      value = 10 * value + digit[(int)*src];
    }else{
      count_and_offset[value]++;
      value = 0;
      i++;
    }
    src ++;
  }
  /// read campaign prices.
  int *dst = cprices;
  i = 0;
  value = 0;
  while(i < D){
    if(*src != '\n'){
      value = 10 * value + digit[(int)*src];
    }else{
      *(dst++) = value;
      value = 0;
      i++;
    }
    src ++;
  }
  pre_compute();
}

int Campaign::find_best_price(int cp)
{
  int candidate = 0;
  int lowlimit = max(cp / 2, (int)lowest_price);
  int larger = cp - lowest_price;
  larger = get_next_valid_lower(larger);
  while(larger >= lowlimit && candidate != cp){
    int smaller = cp - larger;
    if(unlikely(smaller == larger && count_and_offset[smaller] == 1)) smaller--;
    smaller = get_next_valid_lower(smaller);
    if(unlikely(smaller < lowest_price)){
      larger = get_next_valid_lower(--larger);
      continue;
    }
    candidate = max(smaller + larger, candidate);
    larger = get_next_valid_lower(--larger);
  }
  return candidate;
}

void Campaign::find_best_prices()
{
  int c;
  for(int day = 0; day < D; day++){
    c = cprices[day];
    best_prices[day] = find_best_price(c);
  }
}

void Campaign::print_best_prices()
{
  stringstream output;
  for(int day = 0; day < D; day++){
    output << best_prices[day] << "\n";
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

void solve()
{
  Campaign c1;
  c1.read_from_stdin();
  c1.find_best_prices();
  c1.print_best_prices();
}

BOOST_PYTHON_MODULE(challenge4_boost){
  boost::python::def("solve", solve);
}
