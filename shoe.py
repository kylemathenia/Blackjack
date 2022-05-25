
from options import Cards
import random
import logging

logging.basicConfig(level=logging.DEBUG)

class Shoe:
    def __init__(self,num_decks,shoe_refill_depth):
        self.num_decks = num_decks
        self.shoe_refill_depth = shoe_refill_depth
        self.single_suit = [Cards.ACE,Cards.TWO,Cards.THREE,Cards.FOUR,Cards.FIVE,Cards.SIX,Cards.SEVEN,Cards.EIGHT,Cards.NINE,Cards.TEN,Cards.JACK,Cards.QUEEN,Cards.KING]
        self.shoe = []
        self.refill()
        self.played = []

    def draw_one(self):
        if self.cards_left <= self.shoe_refill_depth:
            self.refill()
        card = self.shoe.pop()
        self.played.append(card)
        return card

    def draw_two(self):
        card1 = self.draw_one()
        card2 = self.draw_one()
        self.played.append(card1)
        self.played.append(card2)
        return [card1,card2]

    def refill(self):
        logging.info("\nREFILLING SHOE\n")
        all_cards = []
        for deck_num in range(self.num_decks):
            for suit in range(4):
                all_cards += list(self.single_suit)
        self.shoe = []
        self.played = []
        for card_num in range(len(all_cards)):
            card = all_cards.pop(random.randrange(len(all_cards)))
            self.shoe.append(card)

    ## only works for one deck
    @property
    def true_count(self):
        count = 0
        for card in self.played:
            if card == 10:
                count += -1
            if card == 2 or 3 or 4 or 5 or 6:
                count += 1
        return count

    @property
    def cards_left(self):
        return len(self.shoe)