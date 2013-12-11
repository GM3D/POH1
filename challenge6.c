// challenge6.c by GM3D

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define likely(x)       __builtin_expect((x),1)
#define unlikely(x)     __builtin_expect((x),0)

#define max(a, b) (((a)>(b))?(a):(b))

#define MILLION  1000*1000
#define BUFSIZE 8192 * 1000
#define MAX_DAYS 75

const int lowest_price = 10;

char buf[BUFSIZE];
int count_and_offset[MILLION + 1];
int cprices[MAX_DAYS];
int best_prices[MAX_DAYS];

int digit[96] = {
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
};

int N, D;

inline int get_next_valid_lower(int x)
{
  int l = count_and_offset[x];
  if(l < 0) x += l;
  return x;
}

void pre_compute()
{
  int offset = 0;
  int i;
  for(i = 0; i <= MILLION; i++){
    if(count_and_offset[i] > 0){
      offset = 0;
    }else{
      count_and_offset[i] = offset;
    }
    offset--;
  }
}

void read_from_stdin()
{
  int n, i, value;
  int pos = 0;
  while((n = read(0, buf + pos, BUFSIZE - pos)) > 0){
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
      value = 10 * value + digit[(int)(*src)];
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
      value = 10 * value + digit[(int)(*src)];
    }else{
      *(dst++) = value;
      value = 0;
      i++;
    }
    src ++;
  }
  pre_compute();
}

int find_best_price(int cp)
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

void find_best_prices()
{
  int day, c;
  for(day = 0; day < D; day++){
    c = cprices[day];
    best_prices[day] = find_best_price(c);
  }
}

void print_best_prices()
{
  int day;
  for(day = 0; day < D; day++){
    printf("%d\n", best_prices[day]);
  }
}

int main(int argc, char **argv)
{
  read_from_stdin();
  find_best_prices();
  print_best_prices();
  return 0;
}
