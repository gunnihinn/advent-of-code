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
    vector< vector< int > > grid;
};

bool check( vector< vector< int > > grid, long unsigned row, long unsigned col, int dir )
{
    // dir : 0, 1 - left, right
    // dir : 2, 3 - up, down

    if( dir == 0 )
    {
        for(int i = row - 1; i >= 0; i--)
        {
            if( grid.at( i ).at( col ) >= grid.at( row ).at( col ) )
            {
                return false;
            }
        }
        return true;
    }
    else if( dir == 1 )
    {
        for(int i = row + 1; i < grid.size(); i++)
        {
            if( grid.at( i ).at( col ) >= grid.at( row ).at( col ) )
            {
                return false;
            }
        }
        return true;
    }
    else if( dir == 2 )
    {
        for(int j = col - 1; j >= 0; j--)
        {
            if( grid.at( row ).at( j ) >= grid.at( row ).at( col ) )
            {
                return false;
            }
        }
        return true;
    }
    else
    {
        for(int j = col + 1; j < grid.at( row ).size(); j++)
        {
            if( grid.at( row ).at( j ) >= grid.at( row ).at( col ) )
            {
                return false;
            }
        }
        return true;
    }
}

bool isVisible( vector< vector< int > > grid, long unsigned int row,  long unsigned int col )
{
    if( row == 0 ||
        row == grid.size() - 1 ||
        col == 0 ||
        col == grid.at( row ).size() - 1 )
    {
        return true;
    }

    bool left = check( grid, row, col, 0 );
    bool right = check( grid, row, col, 1 );
    bool up = check( grid, row, col, 2 );
    bool down = check( grid, row, col, 3 );

    return up || down || left || right;
}

int vdist( vector< vector< int > > grid, long unsigned row, long unsigned col, int dir )
{
    if( row == 0 ||
        row == grid.size() - 1 ||
        col == 0 ||
        col == grid.at( row ).size() - 1 )
    {
        return 0;
    }

    // dir : 0, 1 - left, right
    // dir : 2, 3 - up, down
    int val = 0;
    if( dir == 0 )
    {
        for(int i = row - 1; i >= 0; i--)
        {
            val++;
            if( grid.at( i ).at( col ) >= grid.at( row ).at( col ) )
            {
                break;
            }
        }
    }
    else if( dir == 1 )
    {
        for(int i = row + 1; i < grid.size(); i++)
        {
            val++;
            if( grid.at( i ).at( col ) >= grid.at( row ).at( col ) )
            {
                break;
            }
        }
    }
    else if( dir == 2 )
    {
        for(int j = col - 1; j >= 0; j--)
        {
            val++;
            if( grid.at( row ).at( j ) >= grid.at( row ).at( col ) )
            {
                break;
            }
        }
    }
    else
    {
        for(int j = col + 1; j < grid.at( row ).size(); j++)
        {
            val++;
            if( grid.at( row ).at( j ) >= grid.at( row ).at( col ) )
            {
                break;
            }
        }
    }

    return val;
}

int distance( vector< vector< int > > grid, long unsigned int row,  long unsigned int col )
{
    int left = vdist( grid, row, col, 0 );
    int right = vdist( grid, row, col, 1 );
    int up = vdist( grid, row, col, 2 );
    int down = vdist( grid, row, col, 3 );

    return up * down * left * right;
}

int part1( Data data )
{
    int result = 0;

    for(long unsigned int row = 0; row < data.grid.size(); row++)
    {
        for(long unsigned int col = 0; col < data.grid.at( row ).size(); col++)
        {
            bool ok = isVisible( data.grid, row, col );
            if( ok )
            {
                result++;
            }
        }
    }

    return result;
}

int part2( Data data )
{
    int result = 0;

    for(long unsigned int row = 0; row < data.grid.size(); row++)
    {
        for(long unsigned int col = 0; col < data.grid.at( row ).size(); col++)
        {
            int val = distance( data.grid, row, col );
            if( val > result )
            {
                result = val;
            }
        }
    }

    return result;
}

Data parse( istream& is )
{
    auto data = Data();
    for(string line; getline( is, line );)
    {
        vector< int > row;
        for(auto it = line.begin(); it != line.end(); ++it)
        {
            row.push_back(  *it - '0' );
        }
        data.grid.push_back( row );
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
