import numpy as np
from card import Card

class Hand:

    def __init__(self, card_list=[]):
        self.cards = []
        for c in card_list:
            if isinstance(c, Card):
                self.cards.append(c)
            elif isinstance(c, tuple):
                self.cards.append(Card(c[0], c[1]))

    def __repr__(self) -> str:
        return f"<Hand: {len(self)} cards>"
    
    def __str__(self) -> str:
        return ', '.join([str(c) for c in self.cards])

    def __len__(self):
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

    def __add__(self, other):
        if isinstance(other, Hand):
            self.cards += other.cards
        elif isinstance(other, (list, set)):
            assert all([isinstance(x, Card) for x in other])
            self.cards += other

    def append(self, card):
        assert isinstance(card, Card)
        self.cards.append(card)

    def score(self):
        scores = np.array([0])
        for card in self:
            s = card.get_score()
            if isinstance(s, (int, float)):
                scores += s
            else:
                new_scores = [scores.copy() for _ in range(len(s))]
                for i in range(len(s)):
                    new_scores[i] += s[i]
                scores = np.concatenate([*new_scores])
        return np.sort(np.unique(scores))