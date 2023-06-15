from deck import Deck
from dealer import Dealer
from player import Player

class Table:

    def __init__(self, num_decks, num_players, **kwargs) -> None:
        self.num_decks = num_decks
        self.num_players = num_players
        # Process kwargs
        self.blackjack_payout = kwargs.get('blackjack_payout', 1.5)
        # Initialize dealer
        deck = Deck.standard_deck(num_decks)
        self.dealer = Dealer(deck)
        # Initialize players
        self.players = [Player() for _ in range(num_players)]

    def __repr__(self) -> str:
        return f"<Table: {self.num_decks} decks, {self.num_players} players>"
    
    def __str__(self) -> str:
        s = f"Table [{self.num_decks}-deck shoe, {self.num_players} players]"
        s += f"\n\t{str(self.dealer)}"
        for player in self.players:
            s += "\n\t" + str(player) + '\t' + str(player.get_score())
        return s

    def play_blackjack_round(self):
        # Shuffle cards
        self.dealer.shuffle()
        # Players place bets
        for player in self.players:
            player.place_bet()
        # Dealer deals to self and players
        self.dealer.deal_blackjack(self.players)
        # Checks dealer and players blackjack
        dealer_blackjack = self.get_dealer_blackjack()
        player_blackjacks = self.get_player_blackjacks()
        # Handle natural blackjacks
        self.handle_blackjacks(dealer_blackjack, player_blackjacks)
        # Dealer plays against each non-blackjack player
        for player in [p for p in self.players if p not in player_blackjacks]:
            result, actions = self.dealer.play_to(player)
            print(player, actions, result)
        # Dealer reveals hidden card
        self.dealer.reveal_hidden_card()
        # Dealer plays to self
        result, actions = self.dealer.play_to_self()
        print(self.dealer, actions, result)
        # Dealer pays out
        if result == "bust":
            self.dealer.handle_bust(self.players)
        elif result == "stay":
            self.dealer.handle_stay(self.players)

    def get_player_blackjacks(self):
        blackjacks = []
        for player in self.players:
            scores = player.get_score()
            if 21 in scores:
                blackjacks.append(player)
        return blackjacks
    
    def get_dealer_blackjack(self):
        return 21 in self.dealer.get_score()

    def handle_blackjacks(self, dealer_blackjack, players_blackjack):
        if dealer_blackjack:
            # Dealer pushes with blackjack players
            print("dealer got blackjack")
        else:
            # Dealer pays out to blackjack players per the ratio
            print("dealer did not get blackjack")