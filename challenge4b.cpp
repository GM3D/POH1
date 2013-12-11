// challenge4b.cpp by GM3D

#include <iostream>
#include <sstream>
#include <vector>
#include <map>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <unistd.h>
#include <sys/time.h>

const int num_marks = 100;
timeval t[num_marks];
long counter[10];
long counter1[10];

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

int digit[96] = {
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
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
  void report_branch();
};

inline int Campaign::get_next_valid_lower(int x)
{
  int l = count_and_offset[x];
  if(l < 0) x += l;
  return x;
}

void Campaign::read_from_stdin()
{
  int n, i, value;
  int pos = 0;
  while((n = read(0, buf + pos, bufsize - pos)) > 0){
    pos += n;
  }
  gettimeofday(&t[2], NULL);
  buf[pos] = '\n';
  buf[pos + 1] = '\0';
  char *space = index(buf, ' ');
  N = atoi(buf);
  D = atoi(space + 1);
  gettimeofday(&t[3], NULL);
  /// read item prices.
  char *src = index(space + 1, '\n') + 1;
  value = 0;
  i = 0;
  while(i < N){
    if(*src != '\n'){
      value = 10 * value + digit[*src];
    }else{
      count_and_offset[value]++;
      value = 0;
      i++;
    }
    src ++;
  }
  gettimeofday(&t[4], NULL);
  /// read campaign prices.
  int *dst = cprices;
  i = 0;
  value = 0;
  while(i < D){
    if(*src != '\n'){
      value = 10 * value + digit[*src];
    }else{
      *(dst++) = value;
      value = 0;
      i++;
    }
    src ++;
  }
  gettimeofday(&t[5], NULL);
  pre_compute();
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
    counter[3]++;
    if(unlikely(smaller < lowest_price)){
      counter1[3]++;
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
  for(int i = 0; i < D; i++){
    c = cprices[i];
    best_prices[i] = find_best_price(c);
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

void Campaign::report_branch()
{  
  for(int i = 0; i < 10; i++){
    if(counter[i] > 0){
      float ratio = 100.0 * ((float)(counter1[i])) / counter[i];
      cerr << "counter[" << i << "] true ratio = " << ratio << "% \n";
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
  gettimeofday(&t[6], NULL);
  c1.find_best_prices();
  gettimeofday(&t[7], NULL);
  c1.print_best_prices();
  gettimeofday(&t[8], NULL);
  c1.report_branch();
  report_time();
  return 0;
}
