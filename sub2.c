#include <stdio.h>
#include <boost/python.hpp>

BOOST_PYTHON_MODULE(solve_ext)
{
  using namespace boost::python;
  def("solve", solve);
}

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
