#include <algorithm>
#include <fstream>
#include <iostream>
#include <numeric>
#include <set>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

enum Dir {
    Up, Down, Left, Right
};

struct Move {
    Dir dir;
    int steps;
};

int truncate( int x )
{
    if( x > 0 )
        return 1;
    if( x < 0 )
        return -1;
    return 0;
}

struct Rope {
    int x; int y;
};

Rope move_head( Rope head, Dir dir )
{
    if( dir == Dir::Up )
    {
        return { head.x, head.y + 1 };
    }
    if( dir == Dir::Down )
    {
        return { head.x, head.y - 1 };
    }
    if( dir == Dir::Left )
    {
        return { head.x - 1, head.y };
    }
    if( dir == Dir::Right )
    {
        return { head.x + 1, head.y };
    }
}

Rope move_tail( Rope head, Rope tail )
{
    if( abs( head.x - tail.x ) <= 1 && abs( head.y - tail.y ) <= 1 )
        return tail;
    return { tail.x + truncate( head.x - tail.x ), tail.y + truncate( head.y - tail.y ) };
}


class Data
{
public:
    vector< Move > moves;
};

int part1( Data data )
{
    Rope head = { 0, 0 };
    Rope tail = { 0, 0 };
    set< pair< int, int > > seen = { { 0, 0 } };

    for(auto [ dir, steps ] : data.moves)
    {
        for(int i = 0; i < steps; i++)
        {
            head = move_head( head, dir );
            tail = move_tail( head, tail );
            seen.insert( { tail.x, tail.y } );
        }
    }

    return seen.size();
}

int part2( Data data )
{
    int n = 10;
    vector< Rope > ropes;
    for(int i = 0; i < n; i++)
    {
        ropes.push_back( { 0, 0 } );
    }
    set< pair< int, int > > seen = { { 0, 0 } };

    for(auto [ dir, steps ] : data.moves)
    {
        for(int i = 0; i < steps; i++)
        {
            vector< Rope > newRopes = { move_head( ropes.at( 0 ), dir ) };
            for(int j = 1; j < n; j++)
            {
                newRopes.push_back( move_tail( newRopes.at( j - 1 ), ropes.at( j ) ) );
            }

            seen.insert( { newRopes.back().x, newRopes.back().y } );
            ropes = newRopes;
        }
    }

    return seen.size();
}

Data parse( istream& is )
{
    auto data = Data();

    for(string line; getline( is, line );)
    {
        int steps = stoi( line.substr( 2, line.size() ) );
        Dir dir = [](char c){
            if( c == 'U' )
                return Dir::Up;
            if( c == 'D' )
                return Dir::Down;
            if( c == 'L' )
                return Dir::Left;
            if( c == 'R' )
                return Dir::Right;
        }( line.at( 0 ) );

        data.moves.push_back( { dir, steps } );
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
