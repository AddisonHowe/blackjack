import numpy as np
from deck import Deck
from dealer import Dealer
from player import Player

class Table:

    def __init__(self, num_decks, players, **kwargs) -> None:
        self.num_decks = num_decks
        self.players = players
        self.num_players = len(players)
        # Process kwargs
        self.blackjack_payout_ratio = kwargs.get('blackjack_payout_ratio', 1.5)
        # Initialize dealer
        deck = Deck.standard_deck(num_decks)
        self.dealer = Dealer(deck)
        self.house_chips = 0
        # Initialize players
        

    def __repr__(self) -> str:
        return f"<Table: {self.num_decks} decks, {self.num_players} players>"
    
    def __str__(self) -> str:
        s = f"Table [{self.num_decks}-deck shoe, {self.num_players} players]"
        for player in self.players:
            s += f"\n\t{player}\t{player.get_current_bet()}\t{player.get_score()}"
        s += f"\n\t{str(self.dealer)}\t{self.dealer.get_score()}"
        return s

    def play_blackjack_round(self):
        # Shuffle cards
        self.dealer.shuffle()
        # Players place bets
        bets = []
        for player in self.players:
            bets.append(player.place_bet())
        # Dealer deals to self and players
        self.dealer.deal_blackjack(self.players)
        # Handle blackjacks
        dealer_blackjack, blackjacks, non_blackjacks = self.handle_blackjacks()
        # If dealer got blackjack, game ends
        if dealer_blackjack:
            print("Dealer got blackjack.")
            return
        # Dealer plays against each non-blackjack player
        player_results = []
        player_actions = []
        for player in non_blackjacks:
            result, actions = self.dealer.play_to(player)
            player_results.append(result)
            player_actions.append(actions)
            print(player, actions, result)
        # Dealer reveals hidden card
        self.dealer.reveal_hidden_card()
        # Dealer plays to self
        dealer_result, dealer_actions = self.dealer.play_to_self()
        print(self.dealer, dealer_actions, dealer_result)
        if dealer_result == "bust":
            # Dealer busts
            self.handle_bust(non_blackjacks, player_results)
        elif dealer_result == "stay":
            # Dealer pays or collects
            self.handle_stay(non_blackjacks, player_results)
        print(self)
        # Dealer retrieves cards
        self.dealer.collect_cards(self.players)

    def handle_blackjacks(self):
        # Check dealer and player hands for blackjack
        dealer_blackjack = 21 in self.dealer.get_score(include_hidden=True)
        blackjacks = []
        non_blackjacks = []
        for player in self.players:
            scores = player.get_score()
            if 21 in scores:
                blackjacks.append(player)
            else:
                non_blackjacks.append(player)
        if dealer_blackjack:
            # Dealer pushes with blackjack hands
            for player in blackjacks:
                player.retrieve_bet()
            # Dealer beats non-blackjack hands
            for player in non_blackjacks:
                self.house_chips += self.dealer.take_player_bet(player)
        else:
            # Dealer pays out to blackjack hands
            for player in blackjacks:
                bet = player.get_current_bet()
                payout = bet * self.blackjack_payout_ratio
                self.dealer.pay_player(player, payout)
                self.house_chips -= payout
        return dealer_blackjack, blackjacks, non_blackjacks
            
    def handle_stay(self, players, player_results):
        """Dealer did not bust."""
        for i, player in enumerate(players):
            if player_results[i] == 'bust':
                self.house_chips += self.dealer.take_player_bet(player)
            else:
                dealer_score = self.dealer.get_score()
                dealer_score = np.max(dealer_score[dealer_score <= 21])
                player_score = player.get_score()
                player_score = np.max(player_score[player_score <= 21])

                if player_score < dealer_score:
                    # Dealer collects
                    self.house_chips += self.dealer.take_player_bet(player)
                elif player_score > dealer_score:
                    # Player wins
                    bet = player.retrieve_bet()
                    self.house_chips -= bet
                    player.take_chips(bet)
                else:
                    # Push
                    player.retrieve_bet()

    def handle_bust(self, players, player_results):
        """Dealer busts. Pays to any player that did not bust. Takes the bet
        of any player that did bust."""
        for i, player in enumerate(players):
            if player_results[i] == 'bust':
                self.house_chips += self.dealer.take_player_bet(player)
            else:
                bet = player.retrieve_bet()
                self.house_chips -= bet
                player.take_chips(bet)
