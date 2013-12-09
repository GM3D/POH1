#include <iostream>
#include <sys/time.h>

using namespace std;

timeval t[2];


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

void read_whole_syscall()
{
    std::string contents;
    std::fseek(stdin, 0, SEEK_END);
    contents.resize(std::ftell(stdin));
    std::rewind(stdin);
    std::fread(&contents[0], 1, contents.size(), stdin);
    std::fclose(stdin);
    return(contents);
}

int main(int argc, char **argv)
{
  gettimeofday(&t[0], NULL);
  read_cin();
  gettimeofday(&t[1], NULL);
  for(int i = 0; i < 1; i++){
    cerr << "t[" << i + 1 << "] - t[" << i << "] = "
	 << (t[i+1].tv_sec - t[i].tv_sec) * 1000000 
      + t[i+1].tv_usec - t[i].tv_usec
	 << " usecs.\n";
  }
  return 0;
}
