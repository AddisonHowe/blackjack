import numpy as np
from abc import ABC, abstractmethod
from hand import Hand

class AbstractPlayer(ABC):

    def __init__(self, **kwargs):
        self.hand = Hand()
        self.current_bet = None
        # Process keyword arguments
        self.chips = kwargs.get('chips', 0)

    def __repr__(self) -> str:
        return f"<Player>"
    
    def __str__(self) -> str:
        return f"Player: [{str(self.hand)}]"
    
    ######################
    ##  Getter Methods  ##
    ######################

    def get_chips(self):
        return self.chips

    def get_score(self):
        return self.hand.score()
    
    def get_current_bet(self):
        return self.current_bet
    
    ##############################
    ##  Hand Interface Methods  ##
    ##############################

    def take_card(self, card):
        self.hand.append(card)

    def discard_hand(self):
        return self.hand.discard()

    #######################
    ##  Betting Methods  ##
    #######################

    def place_bet(self, information=None):
        bet = self.decide_bet(information)
        self.current_bet = bet
        self.chips -= bet
        return bet
    
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

    ########################
    ##  Abstract Methods  ##
    ########################

    @abstractmethod
    def hit_or_stay(self, dealers_card, decision_method='random', **kwargs):        
        """Decide to hit or stay.
        Args:
            dealers_card (Card): Card the dealer is showing.

        Returns:
            decision (str): Either "hit" or "stay"
        """
        if decision_method == 'random':
            return self._hit_or_stay_random(**kwargs)
        else:
            raise NotImplementedError()
            
    def _hit_or_stay_random(self, **kwargs):
        prob_hit = kwargs.get('prob_hit', 0.5)
        return "hit" if np.random.rand() < prob_hit else "stay"
        
    @abstractmethod
    def decide_bet(self, information=None):
        """Return an amount to bet.
        Args:
            information (dict): information about the state of the game.
        Returns:
            bet (float): bet amount.
        """
        if self.chips >= 10:
            return 10
        return 0
