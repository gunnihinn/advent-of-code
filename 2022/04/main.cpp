#include <algorithm>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

struct Range {
    int left;
    int right;
};

class Data
{
public:
    vector< pair< Range, Range > > ranges;
};

int part1( Data data )
{
    int sum = 0;
    for(auto [ a, b ] : data.ranges)
    {
        sum += (
            ( a.left <= b.left && b.right <= a.right ) ||
            ( b.left <= a.left && a.right <= b.right )
            );
    }

    return sum;
}

int part2( Data data )
{
    return 0;
}

Data parse( istream& is )
{
    auto data = Data();

    for(string line; getline( is, line );)
    {
        auto i = line.find( "," );

        auto left = line.substr( 0, i );
        auto j = left.find( "-" );
        Range a = {
            stoi( left.substr( 0, j ) ),
            stoi( left.substr( j + 1, left.size() ) )
        };

        auto right = line.substr( i + 1, line.size() );
        auto k = right.find( "-" );
        Range b = {
            stoi( right.substr( 0, k ) ),
            stoi( right.substr( k + 1, right.size() ) )
        };

        data.ranges.push_back( pair( a, b ) );
    }

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
