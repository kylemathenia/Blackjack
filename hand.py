
from options import StrategyOptions,Cards

class Hand:
    def __init__(self, player, cards, bet):
        self.player = player
        self.cards = cards
        self.bet = bet
        self.complete = False

    @property
    def is_double(self):
        if len(self.cards)==2:
            if self.cards[0] == self.cards[1]:
                return True
        else:
            return False

    @property
    def face_up_cards(self):
        if self.player.strategy is StrategyOptions.DEALER:
            return [self.cards[0]]
        else:
            return self.cards

    @property
    def best_value(self):
        """Returns the highest possible value of the hand that is not a bust, or the bust value."""
        if not self.hand_soft:
            return self.hard_sum
        # If the hand is soft, the best value of the two will be the higher.
        return self.soft_total_high

    @property
    def hard_sum(self):
        """Returns the combined value of the non-ace cards, plus aces counted as ones."""
        value = 0
        for card in self.hand:
            if card is not Cards.ACE:
                value += card.card_value
        return value + self.cards.count(Cards.ACE)

    @property
    def hand_soft(self):
        """A hand is soft if the player has more than one option for hand value."""
        if Cards.ACE in self.cards:
            if self.soft_total_high < 22:
                return True
        else:
            return False

    @property
    def soft_total_without_ace(self):
        """Returns the soft total of the hand excluding one ace. All additional aces after the first ace are counted
        as ones, because two aces would be 22, a bust."""
        num_aces = self.cards.count(Cards.ACE)
        return self.hard_sum + num_aces - 1

    @property
    def soft_total_low(self):
        """Returns the lower possible value of a soft hand."""
        if Cards.ACE not in self.cards:
            return None
        return self.soft_total_without_ace + 1

    @property
    def soft_total_high(self):
        """Returns the higher possible value of a soft hand."""
        if Cards.ACE not in self.cards:
            return None
        return self.soft_total_without_ace + 11
