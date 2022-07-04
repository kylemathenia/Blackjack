"""A blackjack player class."""

import strategy
from hand import Hand
from options import StrategyOptions
import support

class Player:
    def __init__(self,name,strategy,money=5000,standard_bet=5,play_as=True):
        """A blackjack player. Used inside of a blackjack table instance. Each player has a list of hand instances,
        self.hands, for the potentially multiple hands during one round (split)."""
        self.name = name
        self.strategy = strategy
        self.hands = []
        self.starting_money = money
        self.money = money
        self.standard_bet = standard_bet
        # Edge case. Can bet more than available during split hands if the total bet for the round is untracked.
        self.total_bet_for_round = 0
        self.play_as = play_as
        self.sim_results = None
        self.gameplay_results = []

    def make_bet(self,shoe,table):
        if self.play_as:
            self.bet_size = support.prompt_make_bet(self,table)
        else:
            self.bet_size = strategy.decide_bet(self,shoe,table)
        if self.money < self.bet_size:
            print("\n{} is trying to bet more money than they have. \n Money: {}\tBet: {}".format(
                self.name,self.money,self.bet_size))

    def hand_init(self,cards):
        if self.strategy == StrategyOptions.DEALER:
            self.hands.append(Hand(self,cards, None))
        else:
            self.hands.append(Hand(self,cards,self.bet_size))
            self.total_bet_for_round += self.bet_size

    def decide_action(self,hand,dealer,table):
        return strategy.decide_action(self,hand,dealer,table,self.strategy)

    def discard_hands(self):
        self.hands = []

    @property
    def has_split_hands(self):
        if len(self.hands)>1: return True
        else: return False

    def show_status(self):
        print("\nPlayer: {}\nMoney: ${}\nTotal Winnings: ${}".format(
            self.name,self.money,self.money-self.starting_money))

    @property
    def info(self):
        return 'Name: {:<20} Strategy: {:<20} Standard bet: ${:<20} Starting Money: ${:<20}'.format(self.name,self.strategy.name,self.standard_bet,self.starting_money)




