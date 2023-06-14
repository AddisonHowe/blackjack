import numpy as np
from deck import Deck
from hand import Hand

class Player:

    def __init__(self):
        self.hand = Hand()

    def __repr__(self) -> str:
        return f"<Player>"
    
    def __str__(self) -> str:
        return f"Player: [{str(self.hand)}]"
    
    def get_score(self):
        return self.hand.score()
    
    def take_card(self, card):
        self.hand.append(card)

    def place_bet(self):
        pass

    def hit_or_stay(self, dealers_card, decision_method='random', **kwargs):        
        # Make decision
        if decision_method == 'random':
            return self._hit_or_stay_random(**kwargs)
        else:
            raise NotImplementedError()
            
    def _hit_or_stay_random(self, **kwargs):
        prob_hit = kwargs.get('prob_hit', 0.5)
        return "hit" if np.random.rand() < prob_hit else "stay"
        