
import strategy
from hand import Hand
from options import StrategyOptions
import support

class Player:
    def __init__(self,name,strategy,money=5000,standard_bet=5,play_as=True):
        self.name = name
        self.strategy = strategy
        self.hands = []
        self.starting_money = money
        self.money = money
        self.standard_bet = standard_bet
        self.play_as = play_as
        self.single_sim_results = []
        self.all_sim_results = []
        self.ave_sim_results = []
        self.std_sim_results = []

    def make_bet(self,shoe,table):
        if self.play_as:
            self.bet_size = support.prompt_make_bet(self,table)
        else:
            self.bet_size = strategy.decide_bet(self,shoe,table)
        if self.bet_size <= self.money:
            return False
        else:
            print("\n{} is trying to bet more money than they have. \n Money: {}\tBet: {}".format(
                self.name,self.money,self.bet_size))
            return True

    def hand_init(self,cards,bet=None):
        if self.strategy == StrategyOptions.DEALER:
            self.hands.append(Hand(self,cards, None))
        elif bet is not None: # This is an additional hand.
            self.hands.append(Hand(self,cards, bet))
        else:  # This is the first hand.
            self.hands.append(Hand(self,cards,self.bet_size))

    def decide_action(self,hand,dealer,table):
        return strategy.decide_action(self,hand,dealer,table,self.strategy)

    def discard_hands(self):
        self.hands = []
        self.completed_hands = []

    @property
    def has_split_hands(self):
        if len(self.hands)>1: return True
        else: return False

    def show_status(self):
        print("\nPlayer: {}\nMoney: ${}\nWinnings: ${}".format(
            self.name,self.money,self.money-self.__starting_money))




