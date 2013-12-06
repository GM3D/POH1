#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

struct timeval t[10];

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
  gettimeofday(&t[0], NULL);
  char *line;
  size_t size = sizeof(int) * 1024;
  int linenum = 0;
  int N, D;
  int *p_hist, *p_hist2;
  int *cprices;
  int value = 0;
  int i = 0;
  int denom;
  int million = 1e6;
  line = malloc(size);

  gettimeofday(&t[1], NULL);
  while(getline(&line, &size, stdin) != -1){
    if(linenum == 0){
      char *space = strchr(line, ' ');
      N = strtol(line, NULL, 10);
      D = strtol(space, NULL, 10);
      p_hist = malloc(sizeof(int) * (million + 1));
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

  gettimeofday(&t[2], NULL);
  if(denom > 1){
    p_hist2 = malloc(sizeof(int) * (million / denom + 1));
    for(i = 0; i <= million / denom; i++){
      p_hist2[i] = p_hist[i * denom];
    }
    free(p_hist);
    p_hist = p_hist2;
    for(i = 0; i < D; i++){
      cprices[i] /= denom;
    }
    million /= denom;
  }

  gettimeofday(&t[3], NULL);
  int *offset_to_next_lower = malloc(sizeof(int) * (million + 1));
  //  int offset_to_next_lower[million + 1];

  gettimeofday(&t[4], NULL);
  int offset = 0;
  for(i = 0; i <= million; i++){
    offset_to_next_lower[i] = offset;
    if(p_hist[i]) offset = 0;
    offset++;
  }

  gettimeofday(&t[5], NULL);
  int candidate, cp, smaller, larger, day;
  int lowlimit, lowest_price = 10 / denom;
  for(day = 0; day < D; day++){
    candidate = 0;
    cp = cprices[day];
    lowlimit = (cp > 2 * lowest_price) ? cp / 2 : lowest_price;
    larger = cp - lowest_price;
    if(!p_hist[larger]){
      larger -= offset_to_next_lower[larger];
    }
    while(larger >= lowlimit){
      smaller = cp - larger;
      if(!p_hist[smaller] || (p_hist[smaller] == 1 && cp == 2 * larger)){
	smaller -= offset_to_next_lower[smaller];
      }
      if(smaller < lowest_price){
	larger -= offset_to_next_lower[larger];
	continue;
      }
      if(smaller + larger > candidate){
	candidate = smaller + larger;
      }
      larger -= offset_to_next_lower[larger];
    }
    printf("%d\n", candidate * denom);
  }
  free(p_hist);
  free(cprices);
  free(offset_to_next_lower);
  free(line);
  gettimeofday(&t[6], NULL);
  for(i = 0; i < 9; i++){
    printf("t[%d] - t[%d] = %ld usec.\n", i+1, i,
	   (t[i+1].tv_sec - t[i].tv_sec) * 1000000
	   + t[i+1].tv_usec - t[i].tv_usec);
	   
  }
  return 0;

}
