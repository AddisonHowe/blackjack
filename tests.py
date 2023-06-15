import pytest
import numpy as np
from card import Card
from deck import Deck
from hand import Hand

class TestCard:
    
    def test_init(self):
        card = Card(8, 'S')
        assert card.get_rank() == 8
        assert card.get_suit() == 'S'
    
    def test_score(self):
        card = Card(8, 'S')
        assert card.get_score() == 8

class TestDeck:
    
    @pytest.mark.parametrize("n", [1,2,3])
    def test_init(self, n):
        deck = Deck.standard_deck(n=n)
        assert len(deck) == 52 * n

    @pytest.mark.parametrize("n", [1,2,3])
    def test_iter(self, n):
        deck = Deck.standard_deck(n=n)
        count = 0
        print(deck)
        for card in deck:
            print(card)
            assert isinstance(card, Card)
            count += 1
        assert count == n * 52

    def test_shuffle(self):
        deck = Deck.standard_deck(n=3)
        prev_order = [c.get_rank() for c in deck]
        deck.shuffle()
        new_order = [c.get_rank() for c in deck]
        assert not np.all([x1 == x2 for x1, x2 in zip(prev_order, new_order)])

    def test_pop(self):
        deck = Deck.standard_deck(n=1)
        for i in range(len(deck) - 1):
            c = deck.pop()
        assert len(deck) == 1

class TestHand:
    
    def test_init(self):
        pass

    @pytest.mark.parametrize("card_list, expected_scores", [
        [[(3,'S'), (3,'H'), (3,'C')], 9],
        [[(3,'S'), (2,'H'), ('A','C')], [6, 16]],
        [[(2,'S'), ('A','H'), ('A','C')], [4, 14, 24]],
    ])
    def test_score(self, card_list, expected_scores):
        hand = Hand(card_list)
        assert np.all(hand.score() == expected_scores)

    def test_add(self):
        hand1 = Hand(['1S', '1H', '1D'])
        hand2 = Hand(['2S', '2H', '2D'])
        hand3 = hand1 + hand2
        assert hand1 == Hand(['1S', '1H', '1D'])
        assert hand2 == Hand(['2S', '2H', '2D'])
        assert hand3 == Hand(['1S', '1H', '1D']+['1S', '1H', '1D'])

    def test_iadd(self):
        hand1 = Hand(['1S', '1H', '1D'])
        hand2 = Hand(['2S', '2H', '2D'])
        hand3 = Hand(['1S', '1H', '1D'] + ['1S', '1H', '1D'])
        hand1 += hand2
        assert hand1 == hand3
        assert hand1 == Hand(['1S', '1H', '1D']+['1S', '1H', '1D'])
        assert hand2 == Hand(['2S', '2H', '2D'])
        