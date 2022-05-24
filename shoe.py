
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

    def draw_one(self):
        if self.cards_left <= self.shoe_refill_depth:
            self.refill()
        return self.shoe.pop()

    def draw_two(self):
        card1 = self.draw_one()
        card2 = self.draw_one()
        return [card1,card2]

    def refill(self):
        logging.info("\nREFILLING SHOE\n")
        all_cards = []
        for deck_num in range(self.num_decks):
            for suit in range(4):
                all_cards += list(self.single_suit)
        self.shoe = []
        for card_num in range(len(all_cards)):
            card = all_cards.pop(random.randrange(len(all_cards)))
            self.shoe.append(card)

    @property
    def cards_left(self):
        return len(self.shoe)