#include <algorithm>
#include <fstream>
#include <chrono>
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

uint64_t timeSinceEpochMillisec()
{
    using namespace std::chrono;
    return duration_cast< milliseconds >( system_clock::now().time_since_epoch() ).count();
}

bool climbable( const vector< vector< char > > &grid, const pair< int, int > &from, const pair< int, int > &to )
{
    auto [ y0, x0 ] = from;
    auto [ y1, x1 ] = to;
    return grid.at( y1 ).at( x1 ) - grid.at( y0 ).at( x0 ) <= 1;
}

int calc( const map< pair< int, int >, int > &dist, const pair< int, int > &current, const pair< int, int > &p )
{
    auto it = dist.find( p );
    if( it == dist.end() )
    {
        return dist.at( current ) + 1;
    }
    else
    {
        return min( dist.at( current ) + 1, it->second );
    }
}

int dijkstra( vector< vector< char > > grid, pair< int, int > start, pair< int, int > end )
{
    map< pair< int, int >, int > dist;
    dist[ start ] = 0;

    set< pair< int, int > > unvisited;
    for(int y = 0; y < grid.size(); y++)
        for(int x =0; x < grid.at( y ).size(); x++)
            unvisited.insert( { y, x } );

    auto current = start;
    while( unvisited.find( end ) != unvisited.end() )
    {
        auto [ y, x ] = current;
        if( y > 0 && climbable( grid, current, { y - 1, x } ) )
            dist[ { y - 1, x } ] = calc( dist, current, { y - 1, x } );
        if( y < grid.size() - 1 && climbable( grid, current, { y + 1, x } ) )
            dist[ { y + 1, x } ] = calc( dist, current, { y + 1, x } );
        if( x > 0 && climbable( grid, current, { y, x - 1 } ) )
            dist[ { y, x - 1 } ] = calc( dist, current, { y, x - 1 } );
        if( x < grid.at( y ).size() - 1 && climbable( grid, current, { y, x + 1 } ) )
            dist[ { y, x + 1 } ] = calc( dist, current, { y, x + 1 } );

        unvisited.erase( current );

        auto it = min_element(
            unvisited.begin(),
            unvisited.end(),
            [ &dist ](const pair< int, int > &a, const pair< int, int > &b){
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


    return dist[ end ];
}

int part1( Data data )
{
    return dijkstra( data.grid, data.start, data.end );
}

int part2( Data data )
{
    vector< pair< int, int > > as;
    for(int y = 0; y < data.grid.size(); y++)
        for(int x = 0; x < data.grid.at( y ).size(); x++)
            if( data.grid.at( y ).at( x ) == 'a' )
                as.push_back( { y, x } );

    cout << "checking " << as.size() << " points\n";
    vector< int > dists;
    for(int i = 0; i < as.size(); i++)
    {
        auto t0 = timeSinceEpochMillisec();
        cout << "... point " << i;
        dists.push_back( dijkstra( data.grid, as.at( i ), data.end ) );
        auto t1 = timeSinceEpochMillisec();
        cout << " took " << t1 - t0 << " ms\n";
    }

    auto it = min_element( dists.begin(), dists.end() );
    return *it;
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
