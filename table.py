
from shoe import Shoe
from player import Player
from player import StrategyOptions
import logging
from enum import Enum

logging.basicConfig(level=logging.DEBUG)


class ActionOptions(Enum):
    STAND = 1
    HIT = 2
    SPLIT = 3
    DOUBLE_DOWN = 4

class Table:
    def __init__(self,players,strategies,num_decks=1,shoe_shuffle_depth=0,min_bet=1,max_bet=10000,blackjack_multiple=1.5,hit_soft_17=True):
        self.players = players # List of player objects
        self.dealer = Player.Player(StrategyOptions.DEALER)
        self.shoe = Shoe(num_decks,shoe_shuffle_depth)
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.blackjack_prize_mult = blackjack_multiple
        self.hit_soft_17 = hit_soft_17
        self.check_if_players_legal()

    def play_round(self,autoplay=True):
        self.make_bets()
        self.deal()
        for player in self.players:
            if autoplay:
                self.autoplay_hands(player)
            else:
                self.play_hand(player)
        self.autoplay_hands(self.dealer)
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

    def autoplay_hands(self,player):
        action = player.strategy.decide_action(player,self.dealer,self.shoe)
        self.check_if_action_legal(player,action)
        if action == ActionOptions.STAND:
            pass
        if action == ActionOptions.HIT:
            pass
        if action == ActionOptions.SPLIT:
            self.create_split_hands(player)
            self.autoplay_hands(player)
        if action == ActionOptions.DOUBLE_DOWN:
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


    ####################################################################################################################
    # Testing functions
    ####################################################################################################################
    def check_if_players_legal(self):
        """Check to make sure the players given to this table have valid settings."""
        for player in self.players:
            if player.standard_bet < self.min_bet:
                logging.info(
                    "\n{} is too baller for this table max bet.\nStandard Bet: "
                    "{}, Min Bet: {}".format(player.name,player.standard_bet,self.min_bet))
            if player.standard_bet > self.max_bet:
                logging.info(
                    "\n{} is too baller for this table max bet.\nStandard Bet: "
                    "{}, Max Bet: {}".format(player.name,player.standard_bet,self.max_bet))
            if player.money < self.min_bet:
                logging.info("\n{} is too poor for the table min bet.\nMoney: {}, Min Bet: "
                    "{}".format(player.name, player.money,self.min_bet))

    def check_if_action_legal(self, player, action):
        # TODO
        pass

