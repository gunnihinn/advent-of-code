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
    int sum = 0;
    for(auto it = data.sacks.begin(); it != data.sacks.end();)
    {
        // Maybe do less work while parsing and have each part munge the data?
        auto a = ( *it ).first;
        a.insert( a.end(), ( *it ).second.begin(), ( *it ).second.end() );
        ++it;

        auto b = ( *it ).first;
        b.insert( b.end(), ( *it ).second.begin(), ( *it ).second.end() );
        ++it;

        auto c = ( *it ).first;
        c.insert( c.end(), ( *it ).second.begin(), ( *it ).second.end() );
        ++it;

        sort( a.begin(), a.end() );
        sort( b.begin(), b.end() );
        sort( c.begin(), c.end() );

        vector< char > common1;
        set_intersection( a.begin(), a.end(), b.begin(), b.end(), back_inserter( common1 ) );
        sort( common1.begin(), common1.end() );

        vector< char > common;
        set_intersection( common1.begin(), common1.end(), c.begin(), c.end(), back_inserter( common ) );

        char last = 0;
        for(auto ch : common )
        {
            if( last != ch )
            {
                sum += priority( ch );
                last = ch;
            }
        }
    }

    return sum;
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
