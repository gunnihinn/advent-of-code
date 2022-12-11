#include <algorithm>
#include <fstream>
#include <iostream>
#include <numeric>
#include <regex>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

class Monkey
{
public:
    vector< uint64_t > items;
    function< uint64_t ( uint64_t ) > operation;
    uint64_t test;
    map< bool, uint64_t > tf;

    Monkey() = default;
};

function< uint64_t ( uint64_t ) > mk_add( uint64_t x )
{
    return [ x ](uint64_t old) {
        return old + x;
    };
}

function< uint64_t ( uint64_t ) >mk_mult( uint64_t x )
{
    return [ x ](uint64_t old) {
        return old * x;
    };
}

function< uint64_t ( uint64_t ) >mk_square()
{
    return [](uint64_t old) {
        return old * old;
    };
}

class Data
{
public:
    vector< Monkey > monkeys;
};

uint64_t part1( Data data )
{
    map< uint64_t, uint64_t > inspected;
    for(uint64_t m = 0; m < data.monkeys.size(); m++)
    {
        inspected[ m ] = 0;
    }

    for(uint64_t i = 0; i < 20; i++)
    {
        for(uint64_t m = 0; m < data.monkeys.size(); m++)
        {
            inspected[ m ] += data.monkeys[ m ].items.size();
            for(uint64_t item: data.monkeys[ m ].items)
            {
                item = data.monkeys[ m ].operation( item );
                item = item / 3;
                bool cond = ( item % data.monkeys[ m ].test ) == 0;
                uint64_t next =  data.monkeys[ m ].tf[ cond ];
                data.monkeys[ next ].items.push_back( item );
            }
            data.monkeys[ m ].items = {};
        }
    }

    vector< uint64_t > vals;
    for(auto [ k, v ] : inspected)
    {
        vals.push_back( v );
    }
    sort( vals.begin(), vals.end() );

    uint64_t result = vals.at( vals.size() - 1 ) * vals.at( vals.size() - 2 );

    return result;
}

uint64_t part2( Data data )
{
    uint64_t result = 0;
    return result;
}

Data parse( istream& is )
{
    auto data = Data();

    regex re_monkey( "Monkey" );
    regex re_items( "Starting items: ([0-9]+)" );
    regex re_op( "Operation: new = old (.) (.+)" );
    regex re_test( "Test: divisible by (\\d+)" );
    regex re_t( "If true: throw to monkey (\\d+)" );
    regex re_f( "If false: throw to monkey (\\d+)" );

    for(string line; getline( is, line );)
    {
        smatch match;
        if( regex_search( line, match, re_monkey ) )
        {
            data.monkeys.push_back( Monkey() );
        }
        else if( regex_search( line, match, re_items ) )
        {
            stringstream ss( line.substr( 18, line.size() ) );
            for(string m; getline( ss, m, ',' );)
            {
                data.monkeys.back().items.push_back( stoi( m ) );
            }
        }
        else if( regex_search( line, match, re_op ) )
        {
            auto it = match.begin();
            ++it;
            if( *it == "+" )
            {
                ++it;
                data.monkeys.back().operation = mk_add( stoi( ( *it ).str() ) );
            }
            else if( *it == "*" )
            {
                ++it;
                if( *it == "old" )
                {
                    data.monkeys.back().operation = mk_square();
                }
                else
                {
                    data.monkeys.back().operation = mk_mult( stoi( ( *it ).str() ) );
                }
            }
            else
            {
                cout << "ERROR: Unknown op " << *it << "\n";
            }
        }
        else if( regex_search( line, match, re_test ) )
        {
            auto it = match.begin();
            ++it;
            data.monkeys.back().test = stoi( ( *it ).str() );
        }
        else if( regex_search( line, match, re_t ) )
        {
            auto it = match.begin();
            ++it;
            data.monkeys.back().tf[ true ] = stoi( ( *it ).str() );
        }
        else if( regex_search( line, match, re_f ) )
        {
            auto it = match.begin();
            ++it;
            data.monkeys.back().tf[ false ] = stoi( ( *it ).str() );
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
