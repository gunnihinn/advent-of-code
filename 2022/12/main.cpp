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

bool seen( const vector< pair< int, int > > &visited, const pair< int, int > &p )
{
    for(auto &q: visited)
    {
        if( p == q )
            return true;
    }

    return false;
}

bool valid( int x, int y, pair< int, int > p )
{
    return 0 <= p.second &&
           p.second < x &&
           0 <= p.first &&
           p.first < y;
}

int dfs( const vector< vector< char > > &grid, vector< pair< int, int > > &visited, const pair< int, int > &end )
{
    auto current = visited.back();

    if( current == end )
    {
        return visited.size();
    }

    auto [ y, x ] = current;
    vector< pair< int, int > > cand = {
        { y - 1, x },
        { y + 1, x },
        { y, x - 1 },
        { y, x + 1 },
    };

    vector< int > distances = { grid.size() * grid.at( y ).size() + 1 };

    for(auto &p : cand)
    {
        if( valid( grid.at( y ).size(), grid.size(), p ) &&
            climbable( grid, current, p ) &&
            !seen( visited, p ) )
        {
            visited.push_back( p );
            distances.push_back( dfs( grid, visited, end ) );
            visited.pop_back();
        }
    }

    auto it = min_element( distances.begin(), distances.end() );
    return *it;
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
        vector< pair< int, int > > cand = {
            { y - 1, x },
            { y + 1, x },
            { y, x - 1 },
            { y, x + 1 },
        };

        for(auto& p: cand)
            if( valid( grid.at( y ).size(), grid.size(), p ) && climbable( grid, current, p ) )
                dist[ p ] = calc( dist, current, p );

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
    //vector< pair< int, int > > visited = { data.start };
    //visited.push_back( data.start );
    //return dfs( data.grid, visited, data.end ) - 1;
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
