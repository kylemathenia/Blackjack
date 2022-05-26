
from player import Player
from options import StrategyOptions,ActionOptions,Cards
from shoe import Shoe
import support
import logging

logging.basicConfig(level=logging.DEBUG)


class Table:
    def __init__(self,players,num_decks=1,shoe_shuffle_depth=0,min_bet=1,max_bet=10000,
                 blackjack_multiple=1.5,hit_soft_17=True,double_after_split=True,autoplay=False):
        self.players = players # Set of player objects
        self.dealer = Player('Dealer',StrategyOptions.DEALER,play_as=False)
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
    def play(self):
        while True:
            if not self.players:
                support.prompts_exit_game()
                break
            self.play_round()

    def play_round(self,autoplay=None):
        if autoplay is not None:
            self.autoplay = autoplay
        self.round_setup()
        self.make_bets()
        self.deal()
        for player in self.players:
            self.play_hands(player)
        self.play_hands(self.dealer)
        support.show_result(self.dealer,self.players,self)
        self.payout()
        self.cleanup_round()

    ####################################################################################################################
    # Support
    ####################################################################################################################

    def round_setup(self):
        self.check_if_players_legal()
        if not self.autoplay:
            self.show_table_status()

    def make_bets(self):
        for player in self.players:
            while player.make_bet(self.shoe,self):
                pass

    def deal(self):
        self.dealer.hand_init(self.shoe.draw_two())
        for player in self.players:
            player.hand_init(self.shoe.draw_two())

    def play_hands(self,player):
        for hand in player.hands:
            if not hand.complete:
                if player.play_as:
                    support.prompt_start_hand(player, hand)
                self.play_hand(player,hand)

    def play_hand(self,player,hand):
        if player.play_as:
            action = support.prompt_play_hand(player,hand,self.dealer,self)
        else:
            action = player.decide_action(hand, self.dealer, self.shoe, self)
        self.do_action(action,player,hand)

    def do_action(self,action,player,hand):
        if action == ActionOptions.STAND:
            hand.complete = True
        elif action == ActionOptions.HIT:
            new_card = self.shoe.draw_one()
            hand.cards.append(new_card)
            if player.play_as:
                support.show_new_card(new_card,hand)
            if hand.best_value > 21:
                hand.complete = True
            else:
                self.play_hand(player,hand)
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
        for player in self.players:
            for hand in player.hands:
                player.money += self.hand_winnings(hand,dealers_hand)

    def hand_winnings(self,hand,dealers_hand):
        dealers_hand_value = dealers_hand.best_value
        if hand.best_value > 21:
            return -hand.bet
        elif hand.best_value == 21 and dealers_hand_value != 21:
            return hand.bet*self.blackjack_prize_mult
        elif dealers_hand_value > 21:
            return hand.bet
        elif hand.best_value > dealers_hand_value:
            return hand.bet
        elif hand.best_value < dealers_hand_value:
            return -hand.bet
        elif hand.best_value == dealers_hand_value:
            return 0

    def cleanup_round(self):
        for player in self.players:
            player.discard_hands()
        self.dealer.discard_hands()

    def show_table_status(self):
        print("\n\n##########   CURRENT TABLE STATUS   ##########")
        for player in self.players:
            player.show_status()

    def legal_actions(self, hand, player):
        legal_actions = [ActionOptions.STAND,ActionOptions.HIT]
        #DOUBLE DOWN
        if len(hand.cards) > 2:
            pass
        elif player.has_split_hands and not self.double_after_split:
            pass
        elif hand.bet*2 > player.money:
            pass
        else:
            legal_actions.append(ActionOptions.DOUBLE_DOWN)
        # SPLIT
        if hand.is_double and len(player.hands) < 3:
            legal_actions.append(ActionOptions.SPLIT)
        return legal_actions

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
                    "${}, Min Bet: ${}".format(player.name,player.standard_bet,self.min_bet))
            if player.standard_bet > self.max_bet:
                logging.info(
                    "\n{} is too baller for this table max bet.\nStandard Bet: "
                    "${}, Max Bet: ${}".format(player.name,player.standard_bet,self.max_bet))
            if player.money < self.min_bet:
                logging.info("\n{} is too poor for the table min bet.\nMoney: ${}, Min Bet: "
                    "${}".format(player.name, player.money,self.min_bet))
                illegal_players.append(player)
        for player in illegal_players:
            logging.info("\n{} has been removed from the table.".format(player.name))
            self.players.remove(player)

    def is_legal_action(self,player,action):
        #TODO
        pass

    def check_if_action_legal(self,player,action):
        #TODO
        pass




