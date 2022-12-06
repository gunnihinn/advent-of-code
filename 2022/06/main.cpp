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
    vector< string > buffers;
};

int part1( Data data )
{
    for(auto buffer : data.buffers)
    {
        auto chars = buffer.data();
        for(long unsigned int i = 4; i < buffer.size(); i++)
        {
            if(
                chars[ i - 4 ] != chars[ i - 3 ] &&
                chars[ i - 4 ] != chars[ i - 2 ] &&
                chars[ i - 4 ] != chars[ i - 1 ] &&
                chars[ i - 4 ] != chars[ i  ] &&
                chars[ i - 3 ] != chars[ i - 2 ] &&
                chars[ i - 3 ] != chars[ i - 1 ] &&
                chars[ i - 3 ] != chars[ i  ] &&
                chars[ i - 2 ] != chars[ i - 1 ] &&
                chars[ i - 2 ] != chars[ i  ] &&
                chars[ i - 1 ] != chars[ i ]
                )
            {
                cout << i << " ";
                break;
            }
        }
    }

    return 0;
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
