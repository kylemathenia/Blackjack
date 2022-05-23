
from shoe import Shoe
from player import Player
from player import StrategyOptions
import logging
logging.basicConfig(level=logging.DEBUG)

class Table:
    def __init__(self,players,strategies,num_decks=1,shoe_shuffle_depth=0,bet_min=1,bet_max=10000,blackjack_multiple=1.5,hit_soft_17=True):
        self.players = players # List of player objects
        self.dealer = Player.Player(StrategyOptions.DEALER)
        self.shoe = Shoe(num_decks,shoe_shuffle_depth)
        self.bet_min = bet_min
        self.bet_max = bet_max
        self.blackjack_prize_mult = blackjack_multiple
        self.hit_soft_17 = hit_soft_17
    #     Remember, can only take one card after splitting aces.

    def play_round(self,autoplay=True):
        self.make_bets()
        self.deal()
        for player in self.players:
            if autoplay:
                self.autoplay_hand(player)
            else:
                self.play_hand(player)
        self.autoplay_hand(self.dealer)
        self.payout()
        self.cleanup_round()

    def make_bets(self):
        for player in self.players:
            player.make_bet(self.shoe)

    def deal(self):
        cards = self.shoe.draw_two()
        self.dealer.hand_init(cards)
        for player in self.players:
            cards = self.shoe.draw_two()
            player.hand_init(cards)

    def autoplay_hand(self,player):
        pass

    def play_hand(self, player):
        logging.debug("\nplay_hand() has not been implemented yet.\n")

    def payout(self):
        """Settle up winnings and losings. If a player is out of money, they are kicked out."""
        pass

    def cleanup_round(self):
        for player in self.players:
            player.discard_hands()
        self.dealer.discard_hands()

