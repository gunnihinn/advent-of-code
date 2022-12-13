#include <cassert>
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

struct Point {
    int first;
    int second;
};

struct Data
{
    vector< vector< char > > grid;
    Point start;
    Point end;
};

uint64_t timeSinceEpochMillisec()
{
    using namespace std::chrono;
    return duration_cast< milliseconds >( system_clock::now().time_since_epoch() ).count();
}

bool climbable( const vector< vector< char > > &grid, const Point &from, const Point &to )
{
    return grid.at( to.first ).at( to.second ) - grid.at( from.first ).at( from.second ) <= 1;
}

bool valid( int x, int y, const Point &p )
{
    return 0 <= p.second &&
           p.second < x &&
           0 <= p.first &&
           p.first < y;
}

int dijkstra( vector< vector< char > > grid, Point start, Point end )
{
    vector< vector< int > > dist;
    vector< vector< bool > > unvisited;

    for(int y = 0; y < grid.size(); y++)
    {
        vector< int > row_dist;
        vector< bool > row_unv;
        for(int x = 0; x < grid.at( y ).size(); x++)
        {
            row_unv.push_back( true );
            row_dist.push_back( grid.at( y ).size() * grid.size() + 1 );
        }
        unvisited.push_back( row_unv );
        dist.push_back( row_dist );
    }
    dist[ start.first ][ start.second ] = 0;

    auto current = start;
    while( unvisited[ end.first ][ end.second ] )
    {
        vector< Point > cand = {
            { current.first - 1, current.second },
            { current.first + 1, current.second },
            { current.first, current.second - 1 },
            { current.first, current.second + 1 },
        };

        for(auto& p: cand)
        {
            if( valid( grid.at( current.first ).size(), grid.size(), p ) && climbable( grid, current, p ) )
            {
                dist[ p.first ][ p.second ] = min( dist[ current.first ][ current.second ] + 1, dist[ p.first ][ p.second ] );
            }
        }

        unvisited[ current.first ][ current.second ] = false;

        bool found = false;
        int m = grid.size() * grid.at( current.first ).size() + 1;
        for(int y = 0; y < unvisited.size(); y++)
        {
            for(int x = 0; x < unvisited[ y ].size(); x++)
            {
                if( unvisited[ y ][ x ] && dist[ y ][ x ] < m )
                {
                    found = true;
                    current = { y, x };
                    m = dist[ y ][ x ];
                }
            }
        }

        if( !found )
        {
            break;
        }
    }

    return dist[ end.first ][ end.second ];
}

int part1( Data data )
{
    //vector< Point > visited = { data.start };
    //visited.push_back( data.start );
    //return dfs( data.grid, visited, data.end ) - 1;
    return dijkstra( data.grid, data.start, data.end );
}

int part2( Data data )
{
    vector< Point > as;
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
