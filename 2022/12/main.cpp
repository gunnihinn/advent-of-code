#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

struct Data
{
    vector< vector< char > > grid;
    pair< int, int > start;
    pair< int, int > end;
};

int part1( Data data )
{
    map< pair< int, int >, int > dist;
    dist[ data.start ] = 0;

    set< pair< int, int > > unvisited;
    for(int y = 0; y < data.grid.size(); y++)
        for(int x =0; x < data.grid.at( y ).size(); x++)
            unvisited.insert( { y, x } );

    auto climbable = [ data ](pair< int, int > from, pair< int, int > to) {
        auto [ y0, x0 ] = from;
        auto [ y1, x1 ] = to;
        return data.grid.at( y1 ).at( x1 ) - data.grid.at( y0 ).at( x0 ) <= 1;
    };

    auto current = data.start;
    while( unvisited.size() > 0 )
    {
        auto [ y, x ] = current;
        vector< pair< int, int > > neighbors;
        if( y > 0 && climbable( current, { y - 1, x } ) )
            neighbors.push_back( { y - 1, x } );
        if( y < data.grid.size() - 1 && climbable( current, { y + 1, x } ) )
            neighbors.push_back( { y + 1, x } );
        if( x > 0 && climbable( current, { y, x - 1 } ) )
            neighbors.push_back( { y, x - 1 } );
        if( x < data.grid.at( y ).size() - 1 && climbable( current, { y, x + 1 } ) )
            neighbors.push_back( { y, x + 1 } );

        for(auto p : neighbors)
        {
            auto it = dist.find( p );
            if( it == dist.end() )
            {
                dist[ p ] = dist[ current ] + 1;
            }
            else
            {
                dist[ p ] = min( dist[ current ] + 1, it->second );
            }
        }
        unvisited.erase( current );

        auto it = min_element(
            unvisited.begin(),
            unvisited.end(),
            [ dist ](const pair< int, int > a, const pair< int, int > b){
            auto it1 = dist.find( a );
            if( it1 == dist.end() )
                return false;

            auto it2 = dist.find( b );
            if( it2 == dist.end() )
                return true;

            return it1->second < it2->second;
        } );
        current = *it;
    }


    return dist[ data.end ];
}

int part2( Data data )
{
    int result = 0;
    return result;
}

Data parse( istream& is )
{
    auto data = Data();

    int y = 0;
    for(string line; getline( is, line );)
    {
        vector< char > row;
        for(long unsigned int x = 0; x < line.size(); x++)
        {
            char c = line.at( x );
            if( line.at( x ) == 'S' )
            {
                data.start = { y, x };
                c = 'a';
            }
            else if( line.at( x ) == 'E' )
            {
                data.end = { y, x };
                c = 'z';
            }
            row.push_back( c );
        }
        data.grid.push_back( row );
        y++;
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
