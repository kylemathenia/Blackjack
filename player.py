
from hand import Hand
from strategy import Strategy
from enum import Enum

class StrategyOptions(Enum):
    DEALER = 1
    BASIC = 2


class Player:
    def __init__(self,strategy,money=5000):
        self.strategy = Strategy(strategy)
        self.hands = []
        self.money = money

    def make_bet(self,shoe):
        """Make the """

    def hand_init(self,cards):
        new_hand = Hand(cards)
        self.hands.append(new_hand)

    def discard_hands(self):
        self.hands = []

