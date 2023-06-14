import numpy as np

RANK_SCORES = {'A': (1, 11)}
RANK_SCORES.update({i: i for i in range(2, 11)})
RANK_SCORES.update({r: 10 for r in ['J', 'Q', 'K']})

SUIT_SYMBOLS = {
    'C': u'\u2663',
    'D': u'\u2666',
    'H': u'\u2665',
    'S': u'\u2660',
}

class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def get_rank(self):
        return self.rank
    
    def get_suit(self):
        return self.suit
    
    def __repr__(self) -> str:
        return f"<Card: {self.rank}{self.suit}>"
    
    def __str__(self) -> str:
        return f"{self.rank}{SUIT_SYMBOLS[self.suit]}"
    
    def get_score(self):
        return RANK_SCORES[self.rank]
    