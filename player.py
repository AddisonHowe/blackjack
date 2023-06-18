import numpy as np
from deck import Deck
from hand import Hand

class Player:

    def __init__(self, **kwargs):
        self.hand = Hand()
        self.chips = kwargs.get('chips', 0)
        self.current_bet = None

    def __repr__(self) -> str:
        return f"<Player>"
    
    def __str__(self) -> str:
        return f"Player: [{str(self.hand)}]"
    
    def get_chips(self):
        return self.chips

    def get_score(self):
        return self.hand.score()
    
    def get_current_bet(self):
        return self.current_bet
    
    def take_card(self, card):
        self.hand.append(card)

    def place_bet(self, information=None):
        bet = self._decide_bet(information)
        self.current_bet = bet
        self.chips -= bet
        return bet

    def discard_hand(self):
        return self.hand.discard()

    def hit_or_stay(self, dealers_card, decision_method='random', **kwargs):        
        # Make decision
        if decision_method == 'random':
            return self._hit_or_stay_random(**kwargs)
        else:
            raise NotImplementedError()
            
    def _hit_or_stay_random(self, **kwargs):
        prob_hit = kwargs.get('prob_hit', 0.5)
        return "hit" if np.random.rand() < prob_hit else "stay"
        
    def _decide_bet(self, information=None):
        if self.chips >= 10:
            return 10
        return 0
    
    def forfeit_bet(self):
        bet = self.current_bet
        self.current_bet = None
        return bet
    
    def retrieve_bet(self):
        bet = self.current_bet
        self.chips += bet
        self.current_bet = None
        return bet
        
    def take_chips(self, amount):
        self.chips += amount
        return amount
