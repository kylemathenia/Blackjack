
from table import Table
from player import Player
from options import StrategyOptions

# Create players
jake = Player('Jake', StrategyOptions.HI_LOW_COUNT, money=10000, standard_bet=5, play_as=False)
kyle = Player('Kyle',StrategyOptions.BASIC,money=10000,standard_bet=5,play_as=True)

# Create table
t = Table([jake, kyle],num_decks=1,shoe_shuffle_depth=0,min_bet=5,max_bet=10000,
                 blackjack_multiple=1.5,hit_soft_17=True,double_after_split=True,autoplay=True)

t.play()