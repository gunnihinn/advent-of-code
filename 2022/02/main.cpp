#include <algorithm>
#include <exception>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

using namespace std;

enum Move {
    Rock, Paper, Scissors
};

Move from_str( char s )
{
    switch( s )
    {
        case 'A':
        case 'X':
            return Move::Rock;
        case 'B':
        case 'Y':
            return Move::Paper;
        case 'C':
        case 'Z':
            return Move::Scissors;
        default:
            throw exception();
    }
}

// Checks if player 1 won
int play( pair< Move, Move > round )
{
    auto a = round.first;
    auto b = round.second;

    if( a == b )
    {
        return 1;
    }

    switch( a )
    {
        case Move::Rock:
            if( b == Move::Scissors )
                return 2;
            return 0;
        case Move::Paper:
            if( b == Move::Rock )
                return 2;
            return 0;
        case Move::Scissors:
            if( b == Move::Paper )
                return 2;
            return 0;
        default:
            throw exception();
    }
}

Move cheat( pair< Move, Move > round )
{
    if( round.second == Move::Rock )
    {
        // Lose
        switch( round.first )
        {
            case Move::Rock:
                return Move::Scissors;
            case Move::Paper:
                return Move::Rock;
            default:
                return Move::Paper;
        }
    }
    else if( round.second == Move::Paper )
    {
        // Tie
        return round.first;
    }
    else
    {
        // Win
        switch( round.first )
        {
            case Move::Rock:
                return Move::Paper;
            case Move::Paper:
                return Move::Scissors;
            default:
                return Move::Rock;
        }
    }
}

int move_score( Move move )
{
    if( move == Move::Rock )
        return 1;
    else if( move == Move::Paper )
        return 2;
    else if( move == Move::Scissors )
        return 3;

}

class Data
{
public:
    vector< pair< Move, Move > > moves;
};

int part1( Data data )
{
    int score = 0;

    for(auto round : data.moves )
    {
        score += move_score( round.second );
        auto outcome = play( round );
        score += 3 * ( 2 - outcome );
    }

    return score;
}

int part2( Data data )
{
    int score = 0;

    for(auto round : data.moves )
    {
        Move mine = cheat( round );
        score += move_score( mine );
        auto outcome = play( pair( round.first, mine ) );
        score += 3 * ( 2 - outcome );
    }

    return score;
}

Data parse( istream& is )
{
    auto data = Data();

    for(string line; getline( is, line );)
    {
        auto it = line.begin();
        Move a = from_str( *it );
        ++it;
        ++it;
        Move b = from_str( *it );
        data.moves.push_back( pair( a, b ) );
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
