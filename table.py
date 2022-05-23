
from shoe import Shoe
from player import Player
from player import StrategyOptions
import logging
from enum import Enum

logging.basicConfig(level=logging.DEBUG)


class Cards(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

class ActionOptions(Enum):
    STAND = 1
    HIT = 2
    SPLIT = 3
    DOUBLE_DOWN = 4

class Table:
    def __init__(self,players,strategies,num_decks=1,shoe_shuffle_depth=0,min_bet=1,max_bet=10000,blackjack_multiple=1.5,hit_soft_17=True):
        self.players = players # Set of player objects
        self.dealer = Player.Player(StrategyOptions.DEALER)
        self.shoe = Shoe(num_decks,shoe_shuffle_depth)
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.blackjack_prize_mult = blackjack_multiple
        self.hit_soft_17 = hit_soft_17

    def play_round(self,autoplay=True):
        self.check_if_players_legal()
        self.make_bets()
        self.deal()
        for player in self.players:
            if autoplay:
                self.autoplay_hands(player)
            else:
                self.play_hand(player)
        self.autoplay_hands(self.dealer)
        self.payout()
        self.cleanup_round()



    def make_bets(self):
        for player in self.players:
            player.make_bet(self.shoe)

    def deal(self):
        cards = self.shoe.draw_two()
        self.dealer.hand_init(cards)
        for player in self.players:
            cards = self.shoe.draw_two()
            player.hand_init(cards)

    def autoplay_hands(self,player):
        for hand in player.hands:
            if not hand.complete:
                self.autoplay_hand(player,hand)

    def autoplay_hand(self,player,hand):
        action = self.get_action(player, hand)
        if action == ActionOptions.STAND:
            hand.complete = True
        elif action == ActionOptions.HIT:
            hand.cards.append(self.shoe.draw_one())
            if sum(hand.cards) > 21:  # Bust
                hand.complete = True
            else:
                self.autoplay_hand(self,player,hand)
        elif action == ActionOptions.DOUBLE_DOWN:
            hand.bet += hand.bet
            hand.cards.append(self.shoe.draw_one())
            hand.complete = True
        elif action == ActionOptions.SPLIT:
            cards=hand.cards
            self.create_split_hands(player, hand)
            self.autoplay_hands(player)

    def get_action(self,player,hand):
        action = player.strategy.decide_action(player, hand, self.dealer, self.shoe)
        self.check_if_action_legal(player, action)
        return action

    def create_split_hands(self,player,hand):
        split_card = hand.cards.pop()
        # Add a card to the original hand.
        hand.cards.append(self.shoe.draw_one())
        # Create a new hand with the split card.
        new_card = self.shoe.draw_one()
        #TODO need to confirm the bet size is the same as the original hand for the new hand.
        player.hand_init([split_card,new_card], bet=hand.bet)
        if split_card == Cards.ACE: # If splitting aces, you only get one card.
            hand.complete = True
            new_hand = player.hands[-1]
            new_hand.complete = True

    def play_hand(self, player):
        # TODO
        logging.debug("\nplay_hand() has not been implemented yet.\n")

    def payout(self):
        """Settle up winnings and losings."""
        dealers_hand = sum(self.dealer.hands[0])
        for player in self.players:
            for hand in player.hands:
                hand_total = sum(hand)
                if hand_total > 21:
                    player.money -= hand.bet
                elif hand_total == 21:
                    player.money += (hand.bet*self.blackjack_prize_mult)
                elif hand_total > dealers_hand:
                    player.money += hand.bet
                elif hand_total < dealers_hand:
                    player.money -= hand.bet
                elif hand_total == dealers_hand:
                    continue

    def cleanup_round(self):
        for player in self.players:
            player.discard_hands()
        self.dealer.discard_hands()


    ####################################################################################################################
    # Testing functions
    ####################################################################################################################
    def check_if_players_legal(self):
        """Check to make sure the players given to this table have valid settings."""
        illegal_players = []
        for player in self.players:
            if player.standard_bet < self.min_bet:
                logging.info(
                    "\n{} is too baller for this table max bet.\nStandard Bet: "
                    "{}, Min Bet: {}".format(player.name,player.standard_bet,self.min_bet))
            if player.standard_bet > self.max_bet:
                logging.info(
                    "\n{} is too baller for this table max bet.\nStandard Bet: "
                    "{}, Max Bet: {}".format(player.name,player.standard_bet,self.max_bet))
            if player.money < self.min_bet:
                logging.info("\n{} is too poor for the table min bet.\nMoney: {}, Min Bet: "
                    "{}".format(player.name, player.money,self.min_bet))
            illegal_players.append(player)
        for player in illegal_players:
            logging.info("\n{} has been removed from the table.".format(player.name))
            self.players.remove(player)

    def check_if_action_legal(self, player, action):
        # TODO
        pass

