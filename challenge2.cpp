#include <iostream>
#include <cstdlib>

using namespace std;

int main(int argc, char **argv){
  string line;
  int linenum = 0;
  int N, D;
  list<int> p_list;
  int *cprices;
  int value = 0;
  int i = 0;
  while(getline(cin, line)){
    if(linenum == 0){
      int space = line.find(' ');
      N = strtol(line.c_str(), NULL, 10);
      D = strtol(line.c_str() + space, NULL, 10);
      p_list = new int[1000001];
      cprices = new int[D];
    }else if(linenum <= N){
      value = strtol(line.c_str(), NULL, 10);
      p_list[value] += 1;
    }else if(linenum <= N + D + 1){
      value = strtol(line.c_str(), NULL, 10);
      cprices[i++] = value;
    }
    linenum++;
  }

  int candidate;
  int cp, smaller, larger;
  for(int day = 0; day < D; day++){
    candidate = 0;
    cp = cprices[day];
    larger = cp - 10;
    while(1){
      larger = search_nonzero_downward(larger - 1, p_list);
      if(larger < cp / 2 || larger < 10) break;
      p_list[larger]--;
      smaller = search_nonzero_downward(cp - larger, p_list);
      p_list[larger]++;
      if(smaller < 10) continue;
      if(smaller + larger > candidate){
	candidate = smaller + larger;
      }
    }
    cout << candidate << "\n";
  }
  delete[] cprices;
  return 0;
}
