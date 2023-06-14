from itertools import product as iterprod
import numpy as np
from card import Card

RANKS = [i for i in range(2, 11)] + ['J', 'Q', 'K', 'A']
SUITS = ['C', 'D', 'H', 'S']

class Deck:

    def __init__(self, card_list=[]):
        self.cards = []
        for c in card_list:
            if isinstance(c, Card):
                self.cards.append(c)
            elif isinstance(c, tuple):
                self.cards.append(Card(c[0], c[1]))

    @staticmethod
    def standard_deck(n=1):
        card_list = []
        for i in range(n):
            card_list += [Card(r, s) for s, r in iterprod(SUITS, RANKS)]
        return Deck(card_list)

    def __repr__(self) -> str:
        return f"<Deck: len={len(self)}>"
    
    def __str__(self) -> str:
        return f"Deck ({len(self)} cards)"

    def __len__(self) -> int:
        return len(self.cards)

    def __iter__(self):
        self.current = 0
        return self
    
    def __next__(self):
        if self.current >= len(self.cards):
            raise StopIteration
        card = self.cards[self.current]
        self.current += 1
        return card
    
    def pop(self):
        return self.cards.pop()
    
    def top(self, n=5) -> str:
        return "..."+", ".join([str(c) for c in self.cards[-n:]])

    def shuffle(self):
        np.random.shuffle(self.cards)
    