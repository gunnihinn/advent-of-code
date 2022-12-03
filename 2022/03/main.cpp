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
public:
    vector< pair< vector< char >, vector< char > > > sacks;
};

int priority( char c )
{
    if( c >= 'a' )
        return c - 96;
    else
        return c - 38;
}

int part1( Data data )
{
    int sum = 0;

    for(auto sack : data.sacks)
    {
        auto l = sack.first;
        auto r = sack.second;
        sort( l.begin(), l.end() );
        sort( r.begin(), r.end() );

        vector< char > common;
        set_intersection( l.begin(), l.end(), r.begin(), r.end(), back_inserter( common ) );

        char last = 0;
        for(auto c : common )
        {
            if( last != c )
            {
                sum += priority( c );
                last = c;
            }
        }
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
        vector< char > left;
        vector< char > right;
        auto it = line.begin();

        for(long unsigned int i = 0; i < line.size(); i++)
        {
            if( i < line.size() / 2 )
            {
                left.push_back( *it );
            }
            else
            {
                right.push_back( *it );
            }
            ++it;
        }

        data.sacks.push_back( pair( left, right ) );
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
