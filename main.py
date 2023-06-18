import argparse
import numpy as np
import matplotlib.pyplot as plt
from table import Table
from player import FixedPlayer, GaussianPlayer, BetaPlayer

parser = argparse.ArgumentParser()

parser.add_argument('-n', '--num_decks', type=int, default=1)
parser.add_argument('-p', '--num_players', type=int, default=4)
parser.add_argument('-c', '--num_chips', type=int, default=1000)
parser.add_argument('-r', '--num_rounds', type=int, default=1000)

parser.add_argument('-t', '--type', type=str, default="fixed", 
                    choices=['fixed', 'gaussian', 'beta'])

player_args = parser.add_argument_group()
player_args.add_argument('--bet_amount', type=float, default=10)
player_args.add_argument('--max_bet_proportion', type=float, default=0.05)
player_args.add_argument('--mu', type=float, default=0.5)
player_args.add_argument('--precision', type=float, default=3)
player_args.add_argument('--var', type=float, default=0.005)

args = parser.parse_args()

player_args = {
    'bet_amount': args.bet_amount,
    'max_bet_proportion': args.max_bet_proportion,
    'mu': args.mu,
    'var': args.var,
    'precision': args.precision,
}

def get_players(player_type, num_players, num_chips, player_args):
    players = []
    for i in range(num_players):
        if player_type == 'fixed':
            player = FixedPlayer(
                player_args['bet_amount'], 
                chips=num_chips
            )
        elif player_type == 'gaussian':
            player = GaussianPlayer(
                player_args['mu'], player_args['var'],
                chips=num_chips
            )
        elif player_type == 'beta':
            player = BetaPlayer(
                player_args['max_bet_proportion'],
                player_args['mu'], player_args['precision'],
                chips=num_chips
            )
        else:
            raise RuntimeError(f"Unknown player type `{player_type}`")
        players.append(player)
    return players

def main(args, player_args):

    num_decks = args.num_decks
    num_players = args.num_players
    player_type = args.type
    num_chips = args.num_chips
    num_rounds = args.num_rounds

    players = get_players(player_type, num_players, num_chips, player_args)

    table = Table(num_decks, players)
    
    chip_history = np.zeros([num_rounds, num_players])
    for i in range(num_rounds):
        table.play_blackjack_round()
        chip_history[i] = [p.get_chips() for p in players]

    plt.plot(chip_history)
    plt.show()

if __name__ == "__main__":
    main(args, player_args)
    