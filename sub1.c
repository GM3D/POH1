#include <stdio.h>

/* #include <stdlib.h> */
/* #include <string.h> */
/* void setup() */
/* { */
/*   char *line; */
/*   size_t size = sizeof(int) * 1024; */
/*   int linenum = 0; */
/*   int N, D; */
/*   int *p_hist; */
/*   int *cprices; */
/*   int value = 0; */
/*   int i = 0; */
/*   line = malloc(size); */
/*   while(getline(&line, &size, stdin) != -1){ */
/*     if(linenum == 0){ */
/*       char *space = strchr(line, ' '); */
/*       N = strtol(line, NULL, 10); */
/*       D = strtol(space, NULL, 10); */
/*       p_hist = malloc(sizeof(int) * 1000001); */
/*       cprices = malloc(sizeof(int) * D); */
/*     }else if(linenum <= N){ */
/*       value = strtol(line, NULL, 10); */
/*       p_hist[value] += 1; */
/*     }else if(linenum <= N + D + 1){ */
/*       value = strtol(line, NULL, 10); */
/*       cprices[i++] = value; */
/*     } */
/*     linenum++; */
/*   } */
/*   free(p_hist); */
/*   free(cprices); */
/*   free(line); */
/* } */

/* int add(int a, int b) */
/* { */
/*   printf("%d\n", a + b); */
/*   return a + b; */
/* } */

int solve(int N, int D, int *p_hist, int *cprices)
{
  int candidate, cp, smaller, larger, day, i;
  for(day = 0; day < D; day++){
    candidate = 0;
    cp = cprices[day];
    larger = cp - 10;
    while(1){
      for(i = larger - 1; i >= 10; i--){
	if(p_hist[i]) break;
      }
      larger = i;
      if(larger < cp / 2 || larger < 10) break;
      p_hist[larger]--;
      for(i = cp - larger; i >= 10; i--){
	if(p_hist[i]) break;
      }
      smaller = i;
      p_hist[larger]++;
      if(smaller < 10) continue;
      if(smaller + larger > candidate){
	candidate = smaller + larger;
      }
    }
    printf("%d\n", candidate);
  }
  return 0;
}
