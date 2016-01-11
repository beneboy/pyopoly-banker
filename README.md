#PyOpoly Banker

Take the tedium out of money management in Monopoly. This Django project allows transfer between players in a game as well as to and from the bank.

## Get Started

Standard Django setup applies

    git clone <this-repo>
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver*

\*the runserver command  should include the argument to listen on 0.0.0.0 or your IP address, otherwise external clients can't connect.

## Usage

Each player connects on their own device and signs in, and is given a $1,500 starting balance. As the game progresses players can transfer money to each other or to the bank, or add income. When the game is over, visit the URL /reset to clear all players.

## Issues
- Little to no validation (of values or users. Don't play with people you don't trust)
- Reset is heavy handded - deleting all players
- No support for multiple games
- Does not support the money-to-the-free-parking-pool incorrect style of game play
