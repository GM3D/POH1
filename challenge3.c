#include <stdio.h>
#include <stdlib.h>
#include <string.h>

inline int gcd(int a, int b)
{
  int d, r, tmp;
  if(b > a){
    tmp = a;
    a = b;
    b = tmp;
  }
  do{
    r = a % b;
    a = b;
    b = r;
  }while(r > 0);
  return a;
}

int main(int argc, char **argv){
  char *line;
  size_t size = sizeof(int) * 1024;
  int linenum = 0;
  int N, D;
  int *p_hist, *p_hist2;
  int *cprices;
  int value = 0;
  int i = 0;
  int denom;
  line = malloc(size);
  while(getline(&line, &size, stdin) != -1){
    if(linenum == 0){
      char *space = strchr(line, ' ');
      N = strtol(line, NULL, 10);
      D = strtol(space, NULL, 10);
      p_hist = malloc(sizeof(int) * 1000001);
      cprices = malloc(sizeof(int) * D);
    }else if(linenum <= N){
      value = strtol(line, NULL, 10);
      p_hist[value] += 1;
      if(linenum == 1){
	denom = value;
      }else{
	if(denom > 1){
	  denom = gcd(denom, value);
	}
      }
    }else if(linenum <= N + D + 1){
      value = strtol(line, NULL, 10);
      cprices[i++] = value;
      if(denom > 1){
	denom = gcd(denom, value);
      }
    }
    linenum++;
  }
  
  if(denom > 1){
    p_hist2 = malloc(sizeof(int) * (1000000 / denom + 1));
    for(i = 0; i <= 1000000 / denom; i++){
      p_hist2[i] = p_hist[i * denom];
    }
    free(p_hist);
    p_hist = p_hist2;
    for(i = 0; i < D; i++){
      cprices[i] /= denom;
    }
  }

  int candidate, cp, smaller, larger, day;
  int minimum = 10 / denom;
  for(day = 0; day < D; day++){
    candidate = 0;
    cp = cprices[day];
    larger = cp - minimum;
    while(1){
      for(i = larger - 1; i >= minimum; i--){
	if(p_hist[i]) break;
      }
      larger = i;
      if(larger < cp / 2 || larger < minimum) break;
      p_hist[larger]--;
      for(i = cp - larger; i >= minimum; i--){
	if(p_hist[i]) break;
      }
      smaller = i;
      p_hist[larger]++;
      if(smaller < minimum) continue;
      if(smaller + larger > candidate){
	candidate = smaller + larger;
      }
    }
    printf("%d\n", candidate * denom);
  }
  free(p_hist);
  free(cprices);
  free(line);
  return 0;
}
