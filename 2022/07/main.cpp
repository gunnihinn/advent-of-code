#include <algorithm>
#include <fstream>
#include <iostream>
#include <numeric>
#include <regex>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

class Data
{
public:
    string name;
    int size; // if file
    vector< shared_ptr< Data > > children; // if dir

    Data( string name ) : name( name )
    {
        size = 0;
    }

    Data( string name, int size ) : name( name ), size( size )
    {
    }

    string str() const
    {
        return _str( 0 );
    }

    int sum() const
    {
        if( size > 0 )
        {
            return size;
        }

        int s = 0;
        for(auto c : children)
        {
            s += c->sum();
        }

        return s;
    }

private:
    string _str( int level ) const
    {
        stringstream ss;
        string pad = "";
        pad.append( level, ' ' );
        ss << pad << "- " << name << " ";
        if( size > 0 )
        {
            ss << "(file, size=" << size << ")\n";
        }
        else
        {
            ss << "(dir)\n";
            for(auto c : children)
            {
                ss << c->_str( level + 2 );
            }
        }

        return ss.str();
    }
};

int p1sum( shared_ptr< Data > data )
{
    int s = 0;

    for(auto c : data->children)
    {
        s += p1sum( c );
    }

    if( !data->children.empty() && data->sum() < 100000 )
    {
        s += data->sum();
    }

    return s;
}

vector< int > p2( shared_ptr< Data > data )
{
    vector< int > sizes;
    if( data->size > 0 )
    {
        return sizes;
    }

    sizes.push_back( data->sum() );
    for(auto c : data->children)
    {
        auto s = p2( c );
        sizes.insert( sizes.end(), s.begin(), s.end() );
    }

    return sizes;
}

int part1( shared_ptr< Data > data )
{
    int result = p1sum( data );
    return result;
}

int part2( shared_ptr< Data > data )
{
    int total = 70000000;
    int need = 30000000;

    vector< int > sizes = p2( data );
    sort( sizes.begin(), sizes.end() );
    int used = total - sizes.back();

    for(auto i : sizes)
    {
        if( used + i > need )
        {
            return i;
        }
    }
    return 0;
}

shared_ptr< Data > parse( istream& is )
{
    regex re_cd( "\\$ cd (.+)" );
    regex re_ls( "\\$ ls" );
    regex re_file( "(\\d+) (.+)" );
    regex re_dir( "dir (.+)" );

    vector< shared_ptr< Data > > stack = { make_shared< Data >( "/" ) };

    for(string line; getline( is, line );)
    {
        smatch match;
        if( regex_match( line, match, re_cd ) )
        {
            auto it = match.begin();
            ++it;
            string m = ( *it ).str();
            if( m == ".." )
            {
                stack.pop_back();
            }
            else if( m == "/" )
            {
                auto root = stack.front();
                stack.clear();
                stack.push_back( root );
            }
            else
            {
                for(auto child : stack.back()->children)
                {
                    if( child->name == m )
                    {
                        stack.push_back( child );
                        break;
                    }
                }
            }
        }
        else if( regex_match( line, match, re_ls ) )
        {
            // do nothing
            //auto it = sregex_token_iterator( line.begin(), line.end(), re_ls );
        }
        else if( regex_match( line, match, re_file ) )
        {
            auto it = match.begin();
            ++it;
            int size = stoi( ( *it ).str() );
            ++it;
            string name = ( *it ).str();
            stack.back()->children.push_back( make_shared< Data >( name, size ) );
        }
        else if( regex_match( line, match, re_dir ) )
        {
            auto it = match.begin();
            ++it;
            string name = ( *it ).str();
            stack.back()->children.push_back( make_shared< Data >( name ) );
        }
        else
        {
            cout << "ERROR: Unmatched line " << line << "\n";
        }
    }

    return stack.at( 0 );
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
