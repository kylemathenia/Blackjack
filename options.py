
from enum import Enum

class ActionOptions(Enum):
    STAND = 1
    HIT = 2
    SPLIT = 3
    DD_OR_HIT = 4
    DD_OR_STAND = 5
    DOUBLE_DOWN = 6

class StrategyOptions(Enum):
    DEALER = 1
    BASIC = 2
    Hi_low_count = 3

class Cards(Enum):
    """Must be initialized with different values. (so not the card values) """
    ACE,TWO,THREE,FOUR,FIVE,SIX,SEVEN,EIGHT,NINE,TEN,JACK,QUEEN,KING = 1,2,3,4,5,6,7,8,9,10,11,12,13

    @property
    def card_value(self):
        if self.name == 'JACK' or self.name == 'QUEEN' or self.name == 'KING':
            return [10]
        if self.name == 'ACE':
            return [1,11]
        else:
            return [self.value]