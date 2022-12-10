#include <algorithm>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

enum Op {
    addx, noop
};

struct Instruction {
    Op op;
    int val;
};

class Data
{
public:
    vector< Instruction > instructions;
};

int part1( Data data )
{
    int result = 0;

    int x = 1;
    int cycle = 0;
    for(auto [ op, val ] : data.instructions)
    {
        if( op == addx )
        {
            for(int j = 0; j < 2; j++)
            {
                cycle++;
                if( cycle % 40 == 20 )
                {
                    result += cycle * x;
                }
            }
            x += val;
        }
        else
        {
            cycle++;
            if( cycle % 40 == 20 )
            {
                result += cycle * x;
            }
        }
    }

    return result;
}

int part2( Data data )
{
    vector< vector< char > > crt;
    for(int i = 0; i < 6; i++)
    {
        vector< char > line;
        for(int j =0; j < 40; j++)
        {
            line.push_back( '.' );
        }
        crt.push_back( line );
    }

    int x = 1;
    int cycle = 0;
    for(auto [ op, val ] : data.instructions)
    {
        if( op == addx )
        {
            for(int j = 0; j < 2; j++)
            {

                if( abs( x - ( cycle % 40 ) ) < 2 )
                {
                    crt.at( cycle / 40 ).at( cycle % 40 ) = '#';
                }
                cycle++;
            }
            x += val;
        }
        else
        {

            if( abs( x - ( cycle % 40 ) ) < 2 )
            {
                crt.at( cycle / 40 ).at( cycle % 40 ) = '#';
            }
            cycle++;
        }
    }

    cout << "\n";
    for(auto line: crt)
    {
        for(auto c  :line)
        {
            cout << c;
        }
        cout << "\n";
    }

    int result = 0;
    return result;
}

Data parse( istream& is )
{
    auto data = Data();
    for(string line; getline( is, line );)
    {
        if( line.at( 0 ) == 'a' )
        {
            int val = stoi( line.substr( 4, line.size() ) );
            data.instructions.push_back( { addx, val } );
        }
        else
        {
            data.instructions.push_back( { noop, 0 } );
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
