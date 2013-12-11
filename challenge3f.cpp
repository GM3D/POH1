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

inline char *get_line()
{
  static char* ptr = buf;
  char *p = ptr;
  char *end = index(p, '\n');
  *end = '\0';
  ptr = end + 1;
  return p;
}

int main(int argc, char **argv)
{
  char *line;
  int n, pos = 0;
  int N, D;
  
  while((n = read(0, buf + pos, bufsize - pos)) > 0){
    pos += n;
  }
  line = get_line();
  char *space = index(line, ' ');
  N = strtol(line, NULL, 10);
  D = strtol(space, NULL, 10);
  printf("N, D = %d, %d", N, D);
}
