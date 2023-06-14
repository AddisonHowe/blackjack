import argparse
import numpy as np
from card import Card
from deck import Deck
from hand import Hand
from player import Player
from dealer import Dealer

parser = argparse.ArgumentParser()

parser.add_argument('-n', '--num_decks', type=int, default=1)
parser.add_argument('-p', '--num_players', type=int, default=4)

args = parser.parse_args()


def play_blackjack_round(dealer, players):
    dealer.shuffle()
    for player in players:
        player.place_bet()
    dealer.deal_blackjack(players)
    blackjacks = dealer.pay_blackjacks(players)
    for player in blackjacks:
        print(player)
    for player in [p for p in players if p not in blackjacks]:
        result, actions = dealer.play_to(player)
        print(actions, result)
        

def main(args):
    n_decks = args.num_decks
    n_players = args.num_players
    print(f"num decks: {n_decks}")
    print(f"num players: {n_players}")

    deck = Deck.standard_deck(n_decks)
    dealer =  Dealer(deck)
    players = [Player() for _ in range(n_players)]
    
    def print_table():
        for player in players:
            print(str(player) + '\t' + str(player.get_score()))
        print(dealer)

    print_table()

    play_blackjack_round(dealer, players)

    print_table()
    

if __name__ == "__main__":
    main(args)
    