from abc import abstractmethod
from .abstract_player import AbstractPlayer

"""
"""

class FixedPlayer(AbstractPlayer):

    def __init__(self, bet_amount, **kwargs):
        super().__init__(**kwargs)
        self.bet_amount = bet_amount

    def decide_bet(self, information=None):
        return self.bet_amount if self.chips >= self.bet_amount else 0

    def hit_or_stay(self, dealers_card, decision_method='random', **kwargs):
        return super().hit_or_stay(dealers_card, decision_method, **kwargs)
    