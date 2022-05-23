
from strategy import Strategy
from enum import Enum

class StrategyOptions(Enum):
    DEALER = 1
    BASIC = 2


class Player:
    def __init__(self,name,strategy,money=5000,standard_bet=5):
        self.name = name
        self.strategy = Strategy(strategy)
        self.hands = []
        self.money = money
        self.standard_bet = standard_bet

    def make_bet(self,shoe):
        self.bet_size = self.strategy.decide_bet(shoe,self.standard_bet)

    def hand_init(self,cards,bet=None):
        if self.strategy == StrategyOptions.DEALER:
            self.hands.append(Hand(cards, None))
        elif bet is not None: # This is an additional hand.
            self.hands.append(Hand(cards, bet))
        else:  # This is the first hand.
            self.hands.append(Hand(cards,self.bet_size))

    def discard_hands(self):
        self.hands = []
        self.completed_hands = []


class Hand:
    def __init__(self,cards,bet):
        self.cards = cards
        self.bet = bet
        self.complete = False

