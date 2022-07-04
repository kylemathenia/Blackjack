"""Enum classes for actions, strategies, and cards."""

from enum import Enum

class ActionOptions(Enum):
    STAND = 1
    HIT = 2
    SPLIT = 3
    # Double down if allowed. If not allowed, hit.
    DD_OR_HIT = 4
    # Double down if allowed. If not allowed, stand.
    DD_OR_STAND = 5
    DOUBLE_DOWN = 6
    # Take whatever action that basic strategy would make.
    BASIC_STRATEGY = 7
    # Take whatever action that simple card counting would make.
    HI_LOW_STRATEGY = 8

class StrategyOptions(Enum):
    DEALER = 1
    # A simple card counting strategy is implemented as well. Basically, if the odds are in the players favor based on the
    # cards that have already been played from the shoe, the player bets more in a linear fashion.
    HI_LOW_COUNT = 2
    # Basic strategy is implemented as found at Basic strategy according to 'https://www.blackjackapprenticeship.com/blackjack-strategy-charts/'.
    BASIC = 3
    # Basic strategy, but always hitting on a hard 16.
    BASIC_HIT_HARD_16 = 4
    # Basic strategy, but always standing on a hard 16.
    BASIC_STAND_HARD_16 = 5
    # Basic strategy, but never doubling down.
    BASIC_NEVER_DD = 6
    # Basic strategy, but never splitting.
    BASIC_NEVER_SPLIT = 7

class Cards(Enum):
    ACE,TWO,THREE,FOUR,FIVE,SIX,SEVEN,EIGHT,NINE,TEN,JACK,QUEEN,KING = 1,2,3,4,5,6,7,8,9,10,11,12,13

    @property
    def card_value(self):
        if self.name == 'JACK' or self.name == 'QUEEN' or self.name == 'KING':
            return [10]
        if self.name == 'ACE':
            return [1,11]
        else:
            return [self.value]