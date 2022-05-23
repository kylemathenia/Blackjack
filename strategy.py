

from player import StrategyOptions


#     Remember, can only take one card after splitting aces.

class Strategy:
    def __init__(self,strategy):
        self.strategy = Strategy(strategy)

    def decide_bet(self,shoe,standard_bet):
        """Place bets for a hand. Each hand (if their are multiple) has a bet associated with it."""
        if self.strategy == StrategyOptions.BASIC:
            return standard_bet

    def decide_action(self,player,dealer,shoe):
        # TODO
        pass