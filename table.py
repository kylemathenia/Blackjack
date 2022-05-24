
from player import Player
from options import StrategyOptions,ActionOptions,Cards
from shoe import Shoe
import support

import logging

logging.basicConfig(level=logging.DEBUG)


class Table:
    def __init__(self,players,strategies,num_decks=1,shoe_shuffle_depth=0,min_bet=1,max_bet=10000,
                 blackjack_multiple=1.5,hit_soft_17=True,double_after_split=True,autoplay=False):
        self.players = players # Set of player objects
        self.dealer = Player(StrategyOptions.DEALER)
        self.shoe = Shoe(num_decks,shoe_shuffle_depth)
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.blackjack_prize_mult = blackjack_multiple
        self.hit_soft_17 = hit_soft_17
        self.double_after_split = double_after_split
        self.autoplay = autoplay

    ####################################################################################################################
    # Main
    ####################################################################################################################

    def play_round(self,autoplay=None):
        if autoplay is not None:
            self.autoplay = autoplay

        self.check_if_players_legal()
        self.make_bets()
        self.deal()
        for player in self.players:
            if autoplay or not player.play_as:
                self.autoplay_hands(player)
            else:
                self.play_hands(player)
        self.autoplay_hands(self.dealer)
        self.payout()
        self.cleanup_round()

    ####################################################################################################################
    # Support
    ####################################################################################################################

    def make_bets(self):
        for player in self.players:
            player.make_bet(self.shoe,self)

    def deal(self):
        self.dealer.hand_init(self.shoe.draw_two())
        for player in self.players:
            player.hand_init(self.shoe.draw_two())

    def play_hands(self,player):
        for hand in player.hands:
            if not hand.complete:
                self.play_hand(player,hand)

    def play_hand(self,player,hand):
        if player.play_as:
            support.prompt_start_hand(player,hand)
            action = support.prompt_play_hand(player,hand,self.dealer)
        else:
            action = player.decide_action(hand, self.dealer, self.shoe, self)
        self.check_if_action_legal(player, action)
        self.do_action(action,player,hand)

    def do_action(self,action,player,hand):
        if action == ActionOptions.STAND:
            hand.complete = True
        elif action == ActionOptions.HIT:
            hand.cards.append(self.shoe.draw_one())
            if hand.best_value > 21:
                hand.complete = True
            else:
                self.play_hand(self,player,hand)
        elif action == ActionOptions.DOUBLE_DOWN:
            hand.bet += hand.bet
            hand.cards.append(self.shoe.draw_one())
            hand.complete = True
        elif action == ActionOptions.SPLIT:
            self.create_split_hands(player, hand)
            self.play_hands(player)

    def create_split_hands(self,player,hand):
        split_card = hand.cards.pop()
        # Add a card to the original hand.
        hand.cards.append(self.shoe.draw_one())
        # Create a new hand with the split card.
        new_card = self.shoe.draw_one()
        player.hand_init([split_card,new_card], bet=hand.bet)
        if split_card == Cards.ACE: # If splitting aces, you only get one card.
            hand.complete = True
            new_hand = player.hands[-1]
            new_hand.complete = True


    def payout(self):
        """Settle up winnings and losings."""
        dealers_hand = self.dealer.hands[0]
        dealers_hand_value = dealers_hand.best_value
        for player in self.players:
            for hand in player.hands:
                if hand.best_value > 21:
                    player.money -= hand.bet
                elif hand.best_value == 21:
                    player.money += (hand.bet*self.blackjack_prize_mult)
                elif hand.best_value > dealers_hand_value:
                    player.money += hand.bet
                elif hand.best_value < dealers_hand_value:
                    player.money -= hand.bet
                elif hand.best_value == dealers_hand_value:
                    continue

    def cleanup_round(self):
        for player in self.players:
            player.discard_hands()
        self.dealer.discard_hands()
        if not self.autoplay:
            self.show_players()

    def show_players(self):
        print("\n\n#####     CURRENT TABLE STATUS     #####\n")
        for player in self.players:
            player.show_status()



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
        # Player cannot double down after already hitting.
        pass





