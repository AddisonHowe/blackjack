import numpy as np
from deck import Deck
from hand import Hand

class Dealer:

    def __init__(self, deck):
        self.deck = deck
        self.discard_pile = Deck()
        self.hand = Hand()
        self.hidden_card = None

    def __repr__(self) -> str:
        return f"<Dealer>"
    
    def __str__(self) -> str:
        string = "Dealer: ["
        if self.hidden_card is not None:
            string += "??, "
        string += str(self.hand) + "]"
        return string
    
    def get_deck(self):
        return self.deck
    
    def get_score(self, include_hidden=False):
        if include_hidden:
            return self.hand.score()
    
    def shuffle(self):
        self.deck.shuffle()

    def deal_card_to_player(self, player):
        c = self.deck.pop()
        player.take_card(c)

    def deal_players(self, players):
        for player in players:
            self.deal_card_to_player(player)

    def deal_self(self, hidden=False):
        c = self.deck.pop()
        if hidden:
            self.hidden_card = c
        else:
            self.hand.append(c)
    
    def deal_blackjack(self, players):
        self.deal_players(players)
        self.deal_self(hidden=True)
        self.deal_players(players)
        self.deal_self(hidden=False)

    def pay_blackjacks(self, players):
        blackjacks = []
        for player in players:
            scores = player.get_score()
            if 21 in scores:
                blackjacks.append(player)
        return blackjacks

    def play_to(self, player):
        actions = []
        while True:
            # Get player action
            action = player.hit_or_stay(self.hidden_card)
            actions.append(action)
            if action == "hit":  # Process hit
                self.deal_card_to_player(player)
                score = player.get_score()
                if 21 in score:  # Check for blackjack
                    return "21", actions
                if min(score) > 21:  # Check bust
                    return "bust", actions
            elif action == "stay":  # Process stay
                return "stay", actions
            else:
                raise RuntimeError()
