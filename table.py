from player import Player
from options import StrategyOptions,ActionOptions,Cards
from shoe import Shoe
import support
import logging
import copy
import concurrent.futures
import time

logging.basicConfig(level=logging.INFO)


class Table:
    def __init__(self,players,num_decks=1,shoe_shuffle_depth=0,min_bet=1,max_bet=10000,
                 blackjack_multiple=1.5,hit_soft_17=True,double_after_split=True,autoplay=False,boot_when_poor=False,
                 round_lim=100_000):
        self.players = players # Set of player objects
        self.dealer = Player('Dealer',StrategyOptions.DEALER,play_as=False)
        self.shoe = Shoe(num_decks,shoe_shuffle_depth)
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.blackjack_prize_mult = blackjack_multiple
        self.hit_soft_17 = hit_soft_17
        self.double_after_split = double_after_split
        # FIXME
        self.autoplay = autoplay
        self.boot_when_poor = boot_when_poor
        self.round_lim = round_lim
        self.num_rounds = 0
        # FIXME
        self.autoplay_update_freq = 10_000
        self.simulating = False
        self.num_sim_rounds = 0

    ####################################################################################################################
    # Main functions.
    ####################################################################################################################
    def play(self):
        """Main game loop for non-simulation play."""
        self.num_rounds = 0
        while True:
            if not self.players or self.num_rounds > self.round_lim:
                support.prompts_exit_game()
                break
            self.play_round()
            # FIXME
            if self.autoplay:
                support.show_autoplay_results(self)

    def play_round(self):
        """Single round of play, used in both simulation and non-simulation."""
        self.round_setup()
        self.make_bets()
        self.deal()
        for player in self.players:
            self.play_hands(player)
        self.play_hands(self.dealer)
        if not self.simulating:
            support.show_result(self.dealer,self.players,self)
        self.payout()
        self.cleanup_round()
        self.num_rounds += 1

    ####################################################################################################################
    # Simulation functions
    ####################################################################################################################

    def simulate(self,x_series,sample_size=100,multiprocessing=True):
        """Simulates a single table configuration sample_size number of times and processes data."""
        self.check_settings_for_sim()
        self.num_sim_rounds = sample_size
        # Create copies of this table configuration.
        table_copies = []
        for i in range(sample_size):
            table = copy.deepcopy(self)
            table.table_num = i
            # Refill the shoe so that all tables do not have the same starting shoe.
            table.shoe.refill()
            table.simulating = True
            table_copies.append(table)
        # Simulate and process data
        start_time = time.perf_counter()
        table_results = self.simulate_all_table_copies(x_series,multiprocessing,table_copies)
        logging.info('\nSimulation time: {:.2f} min\n'.format((time.perf_counter()-start_time)/60))
        start_time = time.perf_counter()
        support.process_sim_data(self,table_results,x_series)
        logging.info('\nData processing time: {:.2f} min\n'.format((time.perf_counter()-start_time)/60))


    def simulate_all_table_copies(self,x_series,multiprocessing,table_copies):
        """Performs the simulations for sample_size number of table copies."""
        if multiprocessing:
            with concurrent.futures.ProcessPoolExecutor() as executor:
                results = [executor.map(table.simulate_one_gameplay_series, [x_series]) for table in table_copies]
            table_results = []
            for result in results:
                for sub_result in result:
                    table_results.append(sub_result)
        if not multiprocessing:
            for table in table_copies:
                table.simulate_one_gameplay_series(x_series)
            table_results = table_copies
        return table_results

    def simulate_one_gameplay_series(self,x_series):
        """Simulates one full x_series of play for a single sample table.
        Saves players scores at every x_series entry number of rounds."""
        num_rounds = x_series[-1] + 1
        for round_number in range(num_rounds):
            self.play_round()
            if round_number in x_series:
                for player in self.players:
                    player.gameplay_results.append(player.money)
        logging.info('\t{:.2f}% Complete\t\tTable {}/{} finished.'.format(self.completion_percent,self.table_num,self.num_sim_rounds))
        return self

    ####################################################################################################################
    # Support
    ####################################################################################################################

    def round_setup(self):
        """Check some things before a round, like if people have enough money, etc."""
        if self.boot_when_poor:
            self.check_if_players_legal()
        # FIXME
        if not self.autoplay:
            self.show_table_status()

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
                if player.play_as:
                    support.prompt_start_hand(player, hand)
                self.play_hand(player,hand)

    def play_hand(self,player,hand):
        if player.play_as:
            action = support.prompt_play_hand(player,hand,self.dealer,self)
        else:
            action = player.decide_action(hand, self.dealer, self)
        self.check_if_action_legal(player,hand,action)
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
            player.total_bet_for_round += hand.bet
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
        assert(player.total_bet_for_round<=player.money)
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
                try:
                    assert(player.money >= 0)
                except:
                    logging.critical('\nError: player.money is negative somehow.')

    def hand_winnings(self,hand,dealers_hand):
        dealers_hand_value = dealers_hand.best_value
        if dealers_hand.is_blackjack and hand.is_blackjack:
            return 0
        elif dealers_hand.is_blackjack and not hand.is_blackjack:
            return -hand.bet
        elif hand.is_blackjack and not dealers_hand.is_blackjack:
            return hand.bet * self.blackjack_prize_mult
        elif hand.best_value > 21:
            return -hand.bet
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
            player.total_bet_for_round = 0
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

    @property
    def completion_percent(self):
        return (self.table_num/self.num_sim_rounds)*100

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

    def check_if_action_legal(self,player,hand,action):
        # TODO this is not accounting for betting more than you have for double down and splits.
        if player.strategy == StrategyOptions.DEALER:
            return
        if action not in self.legal_actions(hand, player):
            logging.critical("\nIllegal action.\n")

    def check_settings_for_sim(self):
        """Adjust table settings if not configured properly for simulation."""
        if self.boot_when_poor:
            logging.warning('\nTable configuration "boot_when_poor" must be False for simulations. Changing to False.')
            self.boot_when_poor = False
        # FIXME
        if not self.autoplay:
            logging.warning('\nTable configuration "autoplay" must be True for simulations. Changing to True.')
            self.autoplay = True
        for player in self.players:
            if player.play_as:
                logging.warning('\nPlayer configuration "play_as" must be False for simulations. Changing to False.')
                self.play_as = False