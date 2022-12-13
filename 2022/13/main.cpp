#include <cassert>
#include <algorithm>
#include <fstream>
#include <optional>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

class Packet
{
public:
    vector< Packet > children;
    optional< int > val;

    string str()
    {
        stringstream ss;
        if( val )
        {
            ss << val.value();
        }
        else if( children.empty() )
        {
            ss << "[]";
        }
        else
        {
            ss << "[";
            for(unsigned long int i = 0; i < children.size() - 1; i++)
            {
                ss << children[ i ].str() << ",";
            }
            ss << children.back().str() << "]";
        }
        return ss.str();
    }

    static pair< optional< Packet >, string > parse( string line )
    {
        if( line == "" )
        {
            return { {}, "" };
        }
        else if( line.at( 0 ) == '[' )
        {
            int c = 1;
            int i = 1;
            while( c > 0 )
            {
                assert( i < line.size() );
                if( line.at( i ) == '[' )
                    c++;
                else if( line.at( i ) == ']' )
                    c--;
                i++;
            }

            Packet packet;
            string objs = line.substr( 1, i - 2 );
            for(auto res = Packet::parse( objs ); res.first; res = Packet::parse( res.second ) )
            {
                packet.children.push_back( res.first.value() );
            }

            if( i >= line.size() )
            {
                return { packet, "" };
            }
            else
            {
                return { packet, line.substr( i + 1, line.size() ) };
            }
        }
        else
        {
            int i = 0;
            while( i < line.size() && '0' <= line.at( i ) && line.at( i ) <= '9'  )
                i++;
            Packet packet;
            packet.val = stoi( line.substr( 0, i ) );

            if( i == line.size() )
            {
                return { packet, "" };
            }
            else
            {
                assert( i + 1 < line.size() );
                return { packet, line.substr( i + 1, line.size() ) };
            }
        }
    }
};

class Data
{
public:
    vector< pair< Packet, Packet > > lines;
};

int part1( Data data )
{
    int result = 0;
    for(auto pp : data.lines)
    {
        cout << pp.first.str() << "\n";
        cout << pp.second.str() << "\n";
        cout << "\n";
    }
    return result;
}

int part2( Data data )
{
    int result = 0;
    return result;
}

Data parse( istream& is )
{
    vector< string > lines;
    for(string line; getline( is, line );)
    {
        if( line != "" )
        {
            lines.push_back( line );
        }
    }

    auto data = Data();
    for(auto it = lines.begin(); it != lines.end(); ++it)
    {
        auto [ left, rest1 ] = Packet::parse( *it );
        if( !rest1.empty() )
        {
            cout << "line: " << *it << "\n";
            cout << "rest: " << rest1 << "\n";
        }

        ++it;
        auto [ right, rest2 ] = Packet::parse( *it );
        if( !rest2.empty() )
        {
            cout << "line: " << *it << "\n";
            cout << "rest: " << rest2 << "\n";
        }

        data.lines.push_back( { left.value(), right.value() } );
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
