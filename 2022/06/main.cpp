#include <algorithm>
#include <fstream>
#include <iostream>
#include <numeric>
#include <set>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

class Data
{
public:
    vector< string > buffers;
};

int norepeats( string buffer, long unsigned int k )
{
    auto chars = buffer.data();
    for(long unsigned int i = 0; i < buffer.size() - k; i++)
    {
        set< char > cs;
        for(long unsigned int j = i; j < i + k; j++ )
        {
            cs.insert( chars[ j ] );
        }

        if( cs.size() == k )
        {
            return i + k;
        }
    }

    return 0;
}

int part1( Data data )
{
    for(auto buffer : data.buffers)
    {
        cout << norepeats( buffer, 4 ) << " ";
    }

    return 0;
}

int part2( Data data )
{
    for(auto buffer : data.buffers)
    {
        cout << norepeats( buffer, 14 ) << " ";
    }

    return 0;
}

Data parse( istream& is )
{
    auto data = Data();

    for(string line; getline( is, line );)
    {
        data.buffers.push_back( line );
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
