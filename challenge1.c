#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int search_nonzero_downward(int start, int *histgram)
{
  int i;
  for (i = start; i >= 10; i--){
    if(histgram[i]) return i;
  }
  return -1;
}

int main(int argc, char **argv){
  char *line;
  size_t size = sizeof(int) * 1024;
  int linenum = 0;
  int N, D;
  int *p_hist;
  int *cprices;
  int value = 0;
  int i = 0;
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
    }else if(linenum <= N + D + 1){
      value = strtol(line, NULL, 10);
      cprices[i++] = value;
    }
    linenum++;
  }

  int candidate;
  int cp, smaller, larger;
  int day;
  for(day = 0; day < D; day++){
    candidate = 0;
    cp = cprices[day];
    larger = cp - 10;
    while(1){
      larger = search_nonzero_downward(larger - 1, p_hist);
      if(larger < cp / 2 || larger < 10) break;
      p_hist[larger]--;
      smaller = search_nonzero_downward(cp - larger, p_hist);
      p_hist[larger]++;
      if(smaller < 10) continue;
      if(smaller + larger > candidate){
	candidate = smaller + larger;
      }
    }
    printf("%d\n", candidate);
  }
  free(p_hist);
  free(cprices);
  free(line);
  return 0;
}
