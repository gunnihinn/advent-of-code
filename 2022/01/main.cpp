#include <algorithm>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

int part1( vector< vector< int > > data )
{
    vector< int > sums;
    for(auto bag : data)
    {
        sums.push_back( accumulate( bag.begin(), bag.end(), 0 ) );
    }

    return *max_element( sums.begin(), sums.end() );
}

int part2( vector< vector< int > > data )
{
    vector< int > sums;
    for(auto bag : data)
    {
        sums.push_back( accumulate( bag.begin(), bag.end(), 0 ) );
    }

    sort( sums.begin(), sums.end() );

    auto sum = 0;
    auto it = sums.end();
    for(int i = 0; i < 3; i++)
    {
        --it;
        sum += *it;
    }

    return sum;
}

vector< vector< int > > parse( istream& is )
{
    vector< vector< int > > bags;

    vector< int > bag;
    for(string line; getline( is, line );)
    {
        if( line == "" )
        {
            bags.push_back( bag );
            bag.clear();
        }
        else
        {
            bag.push_back( stoi( line ) );
        }
    }

    if( !bag.empty() )
    {
        bags.push_back( bag );
    }

    return bags;
}

int main( int argc, char** argv )
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
