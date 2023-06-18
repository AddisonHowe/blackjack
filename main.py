import argparse
import numpy as np
from table import Table
from deck import Deck
from player import Player
from dealer import Dealer

parser = argparse.ArgumentParser()

parser.add_argument('-n', '--num_decks', type=int, default=1)
parser.add_argument('-p', '--num_players', type=int, default=4)
parser.add_argument('-c', '--num_chips', type=int, default=1000)

args = parser.parse_args()

def main(args):
    num_decks = args.num_decks
    num_players = args.num_players
    num_chips = args.num_chips

    players = [Player(chips=num_chips) for _ in range(num_players)]
    table = Table(num_decks, players)
    table.play_blackjack_round()
    
    for player in players:
        print(player.get_chips())

if __name__ == "__main__":
    main(args)
    