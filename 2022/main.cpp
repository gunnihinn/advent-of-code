#include <algorithm>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

class Data
{
};

int part1( Data data )
{
    int result = 0;
    return result;
}

int part2( Data data )
{
    int result = 0;
    return result;
}

Data parse( istream& is )
{
    auto data = Data();
    return data;
}

int main( int argc, char* argv[] )
{
    for(int i = 1; i < argc; ++i)
    {
        ifstream fh( *++argv  );
        auto data = parse( fh );
        cout << "part 1: " << part1( data ) << "\n";
        cout << "part 2: " << part2( data ) << "\n";
    }

    return 0;
}
