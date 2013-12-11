#include <iostream>
#include <sys/time.h>
#include <cstdlib>
#include <cstdio>
#include <cstring>
#include <unistd.h>

using namespace std;

const int intervals = 10;
timeval t[intervals];


void read_cin()
{
  int N, D;
  int i, value;
  cin >> N >> D;
  for(i = 0; i < N; i++){
    cin >> value;
    //    cout << value << "\n";
  }
  for(i = 0; i < D; i++){
    cin >> value;
    //    cout << value;
  }
}

void getline_cin()
{
  int N, D;
  int i, value;
  const int bufsize = 256;
  char *buf = new char[bufsize];
  cin.getline(buf, bufsize);
  char *space = index(buf, ' ');
  N = strtol(buf, NULL, 10);
  D = strtol(space, NULL, 10);
  for(i = 0; i < N; i++){
    cin.getline(buf, bufsize);
    value = strtol(buf, NULL, 10);
  }
  for(i = 0; i < D; i++){
    cin.getline(buf, bufsize);
    value = strtol(buf, NULL, 10);
  }
  delete[] buf;
}

void c_fgets()
{
  int N, D;
  int i, value;
  int linenum = 0;
  const int bufsize = 256;
  char *buf = new char[bufsize];
  fgets(buf, bufsize, stdin);
  char *space = index(buf, ' ');
  N = strtol(buf, NULL, 10);
  D = strtol(space, NULL, 10);
  for(i = 0; i < N; i++){
    fgets(buf, bufsize, stdin);
    value = strtol(buf, NULL, 10);
  }
  for(i = 0; i < D; i++){
    fgets(buf, bufsize, stdin);
    value = strtol(buf, NULL, 10);
  }
  delete[] buf;
}

void c_read()
{
  const int bufsize = 8192 * 1000;
  char buf[bufsize];
  int n;
  int count = 0;
  int loops = 0;
  while((n = read(0, buf, bufsize)) > 0){
    count += n;
    loops++;
  }
  std::cout << "read " << count << " bytes.\n";
  std::cout << "looped " << loops << " times.\n";
}

void report()
{
  for(int i = 0; i < intervals - 1; i++){
    long elapsed = (t[i+1].tv_sec - t[i].tv_sec) * 1000000 
      + t[i+1].tv_usec - t[i].tv_usec;

    if(elapsed > 0){
      cerr << "t[" << i + 1 << "] - t[" << i << "] = "
	   << elapsed << " usecs.\n";
    }
  }
}

int main(int argc, char **argv)
{
  gettimeofday(&t[0], NULL);
  c_read();
  gettimeofday(&t[1], NULL);

  report();
  return 0;
}
