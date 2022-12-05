#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

struct Move {
    int amount;
    int from;
    int to;
};

class Data
{
public:
    map< int, vector< char > > stacks;
    vector< Move > moves;
};

int part1( Data data )
{
    for(auto [ amount, from, to ] : data.moves)
    {
        for(int i = 0; i < amount; i++)
        {
            data.stacks[ to ].push_back( data.stacks[ from ].back() );
            data.stacks[ from ].pop_back();
        }
    }

    for(long unsigned int i = 1; i < data.stacks.size() + 1; i++)
    {
        cout << data.stacks[ i ].back();
    }
    cout << " ";

    return 0;
}

int part2( Data data )
{
    for(auto [ amount, from, to ] : data.moves)
    {
        auto j = data.stacks[ from ].size() - amount;
        for(int i = 0; i < amount; i++)
        {
            data.stacks[ to ].push_back( data.stacks[ from ].at( j + i ) );
        }
        for(int i = 0; i < amount; i++)
        {
            data.stacks[ from ].pop_back();
        }
    }

    for(long unsigned int i = 1; i < data.stacks.size() + 1; i++)
    {
        cout << data.stacks[ i ].back();
    }
    cout << " ";

    return 0;
}

Data parse( istream& is )
{
    bool moves = false;
    auto data = Data();
    for(string line; getline( is, line );)
    {
        if( line == "" )
        {
            moves = true;
            continue;
        }

        if( !moves )
        {
            int nr = ( line.size() + 1 ) / 4;
            for(int i = 0; i < nr; i++ )
            {
                auto j = 1 + 4 * i;
                if( line[ j - 1 ] == '[' && line[ j ] != ' ' )
                {
                    auto stack = data.stacks[ i + 1 ];
                    stack.insert( stack.begin(), line[ j ] );
                    data.stacks[ i + 1 ] = stack;
                }
            }
        }
        else
        {
            string buf;
            stringstream ss( line );
            getline( ss, buf, ' ' ); // move
            getline( ss, buf, ' ' );  // X
            int amount = stoi( buf );
            getline( ss, buf, ' ' ); // from
            getline( ss, buf, ' ' ); // Y
            int from = stoi( buf );
            getline( ss, buf, ' ' ); // to
            getline( ss, buf, ' ' ); // Z
            int to = stoi( buf );

            data.moves.push_back( Move{ amount, from, to } );
        }
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
