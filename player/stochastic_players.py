from abc import abstractmethod
import numpy as np
from .abstract_player import AbstractPlayer

"""
"""

class GaussianPlayer(AbstractPlayer):

    def __init__(self, mu, var, **kwargs):
        super().__init__(**kwargs)
        self.mu = mu
        self.var = var
        self.std = np.sqrt(var)

    def decide_bet(self, information=None):
        amount = self.chips * (self.mu + np.abs(np.random.randn()) * self.std)
        return amount if amount <= self.chips else self.chips

    def hit_or_stay(self, dealers_card, decision_method='random', **kwargs):
        return super().hit_or_stay(dealers_card, decision_method, **kwargs)
    

class BetaPlayer(AbstractPlayer):

    def __init__(self, max_proportion, mu=0.5, precision=3, **kwargs):
        super().__init__(**kwargs)
        self.max_proportion = max_proportion
        self.mu = mu
        self.precision = precision
        self.alpha = self.precision * self.mu
        self.beta = self.precision * (1 - self.mu)

    def decide_bet(self, information=None):
        p = np.random.beta(self.alpha, self.beta)
        assert 0 <= p and p <= 1, f"p={p} out of bounds. Should be in [0, 1]."
        max_bet = self.max_proportion * self.chips
        return p * max_bet
    
    def hit_or_stay(self, dealers_card, decision_method='random', **kwargs):
        return super().hit_or_stay(dealers_card, decision_method, **kwargs)
    