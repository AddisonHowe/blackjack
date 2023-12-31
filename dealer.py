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
    
    def get_discard_pile(self):
        return self.discard_pile
    
    def get_score(self, include_hidden=False):
        if include_hidden:
            return (self.hand + self.hidden_card).score()
        else:
            return self.hand.score()
    
    def shuffle(self):
        self.deck.shuffle()

    def deal_card_to_player(self, player):
        c = self.deck.pop()
        player.take_card(c)

    def deal_card_to_self(self):
        c = self.deck.pop()
        self.hand.append(c)

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
                raise RuntimeError(f"Unknown action {action}")
            
    def play_to_self(self):
        actions = []
        while True:
            # Get dealer action
            action = self.hit_or_stay()
            actions.append(action)
            if action == "hit":  # Process hit
                self.deal_card_to_self()
                score = self.get_score()
                if min(score) > 21:  # Check bust
                    return "bust", actions
            elif action == "stay":  # Process stay
                return "stay", actions
            else:
                raise RuntimeError(f"Unknown action {action}")

    def hit_or_stay(self):
        scores = self.get_score()
        scores_leq_21 = scores[scores <= 21]
        max_score = max(scores)
        if max(scores_leq_21) >= 17:
            return "stay"
        else:
            return "hit"

    def reveal_hidden_card(self):
        self.hand += self.hidden_card
        self.hidden_card = None

    def collect_cards(self, players):
        self.discard_pile += self.hand.discard()
        for player in players:
            self.discard_pile += player.discard_hand()
    
    def take_player_bet(self, player):
        bet = player.forfeit_bet()
        return bet
    
    def pay_player(self, player, amount):
        player.retrieve_bet()
        player.take_chips(amount)

    def combine_discards_with_deck(self, shuffle=True):
        self.deck = self.discard_pile + self.deck
        self.discard_pile = Deck()
        if shuffle:
            self.shuffle()
    