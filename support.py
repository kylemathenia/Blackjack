"""Gameplay prompts, data processing, and misc support functions."""

import strategy
from options import ActionOptions as AO
from options import StrategyOptions
import numpy as np
from collections import namedtuple
import concurrent.futures
import logging
from datetime import datetime

Player_Sim_Results_NT =  namedtuple("Player_Sim_Results_NT", "ave_loss_per_round ave_sim_results std_sim_results percentile_sim_results")

action_to_num_map = {AO.STAND:'1',AO.HIT:'2',AO.DOUBLE_DOWN:'3',AO.SPLIT:'4',AO.BASIC_STRATEGY:'5',AO.HI_LOW_STRATEGY:'6'}
num_to_action_map = {'1':AO.STAND,'2':AO.HIT,'3':AO.DOUBLE_DOWN,'4':AO.SPLIT,'5':AO.BASIC_STRATEGY,'6':AO.HI_LOW_STRATEGY}


####################################################################################################################
# Prompts/Info
####################################################################################################################

def prompt_make_bet(player,table):
    while True:
        bet = input("\n{}, how much would you like to bet?\nCurrent money: ${}\n<ENTER> for standard bet.\n> ".format(player.name,player.money))
        if bet == '':
            return player.standard_bet
        if not bet.isnumeric():
            print("\nInvalid entry. Not a number.")
            continue
        bet = int(bet)
        if bet < table.min_bet or bet > table.max_bet:
            print("\nInvalid entry. ${} is not in the table bet range of ${} - ${}".format(
                bet,table.min_bet,table.max_bet))
        elif bet > player.money:
            print("\nInvalid entry. {} is poor. Only has ${}".format(
                player.name, player.money))
        else:
            return int(bet)

def prompt_play_hand(player,hand,dealer,table):
    show_hand_state(hand,dealer,player)
    return get_action(hand,player,table,dealer)

def show_hand_state(hand,dealer,player):
    dealers_hand = dealer.hands[0]
    dealer_card = dealers_hand.cards[0]
    print("\n\n\n####################################")
    print("Dealer showing:\n{}  \t{}\n\n{}'s hand:".format(dealer_card.card_value,dealer_card.name,player.name))
    for card in hand.cards:
        print("{}   \t{}".format(card.card_value,card.name))
    print("####################################")
    show_hand_total(hand)

def get_action(hand,player,table,dealer):
    legal_actions = table.legal_actions(hand, player)
    while True:
        print("\nChoose an action:")
        for action in legal_actions:
            print("{}\t{}".format(action_to_num_map[action],action.name))
        print("{}\t{}".format(action_to_num_map[AO.BASIC_STRATEGY], AO.BASIC_STRATEGY.name))
        print("{}\t{}".format(action_to_num_map[AO.HI_LOW_STRATEGY], AO.HI_LOW_STRATEGY.name))
        action_input = input("> ")
        try:
            action = num_to_action_map[action_input]
        except:
            print("\nInvalid entry.")
            continue
        if action == AO.BASIC_STRATEGY:
            action = strategy.decide_action(player, hand, dealer, table, StrategyOptions.BASIC)
        elif action == AO.HI_LOW_STRATEGY:
            action = strategy.decide_action(player, hand, dealer, table, StrategyOptions.HI_LOW_COUNT)
        if action not in legal_actions:
            print("\nInvalid entry.")
            print(legal_actions)
            print(action)
            action = strategy.decide_action(player, hand, dealer, table, StrategyOptions.HI_LOW_COUNT)
            continue
        else:
            print(action.name)
            return action

def show_new_card(new_card,hand):
    print("New card: {}   {}, New hand value: {}".format(new_card.card_value,new_card.name,hand.hand_values))
    # input('>')
    show_hand_total(hand)

def show_hand_total(hand):
    if hand.hand_soft:
        print("Total: {} or {}".format(hand.soft_total_low,hand.soft_total_high))
    else:
        print("Total: {}".format(hand.hard_sum))

def show_result(dealer,players,table):
    dealers_hand = dealer.hands[0]
    for player in players:
        if player.play_as:
            print('{}:'.format(player.name))
            for hand in player.hands:
                winnings = table.hand_winnings(hand,dealers_hand)
                print("$Winnings: {}\tHand: {}\tDealer: {}".format(winnings,hand.best_value,dealers_hand.best_value))
    if not table.simulating:
        input("\nPress <Enter>")

def prompts_exit_game():
    #TODO Keep track of player stats throughout the game a print them here. Highest money achieved. Num rounds played.
    #winning percentage, etc.
    print("\nExiting game.\n")

def prompt_start_hand(player,hand):
    print("\n########################################\nPlayer: {}, Money: {}, Bet: {}".format(
        player.name,player.money,hand.bet))


####################################################################################################################
# Data processing
####################################################################################################################

def find_ave_loss_per_round(ave_sim_results,x_series,starting_money):
    num_rounds = x_series[-1] + 1
    ending_money = ave_sim_results[-1]
    return (starting_money - ending_money) / num_rounds

def process_sim_data(main_table,table_results,x_series,):
    percentiles_we_care_about = [1, 5, 10, 15, 20, 25, 30, 32, 35, 40, 45, 50, 55, 60, 65, 68, 70, 75, 80, 85, 90,
                                 95, 99]
    logging.info('\nPROCESSING DATA - Large sample sizes or number of rounds may take a while.\n')
    # Reset data just in case.
    for player in main_table.players:
        player.all_sim_results = []
    # Put all the sim results for each player in a list.
    for table in table_results:
        for sim_player in table.players:
            for player in main_table.players:
                if sim_player.name == player.name:
                    player.all_sim_results.append(sim_player.gameplay_results)

    total_players = len(main_table.players)
    players_complete = 0
    total_round_i = len(main_table.players[0].all_sim_results[0])
    # Create the aggregated results across sample size for each player.
    for player in main_table.players:
        ave_sim_results = []
        std_sim_results = []
        percentile_sim_results = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [executor.map(process_data_each_round, [player],[round_i],[total_round_i],[percentiles_we_care_about]) for round_i in range(len(player.all_sim_results[0]))]
        for result in results:
            for subresult in result:
                # Find data from list of similar round number results.
                ave_sim_results.append(subresult['ave_sim_results'])
                std_sim_results.append(subresult['std_sim_results'])
                percentile_sim_results.append(subresult['percentile_sim_results'])

        percentile_sim_results = rearrange_percentile_results(percentile_sim_results,percentiles_we_care_about)
        ave_loss = find_ave_loss_per_round(ave_sim_results,x_series,player.starting_money)
        player.sim_results = Player_Sim_Results_NT(ave_loss, ave_sim_results, std_sim_results, percentile_sim_results)

        players_complete += 1
        percent_complete = round((players_complete/total_players)*100)
        logging.info("\n\n{}% TOTAL DATA PROCESSING COMPLETE.".format(percent_complete))

def process_data_each_round(player,round_i,total_round_i,percentiles_we_care_about):
    # Create a list of all the results from similar round increments.
    round_sim_results = []
    for sim_result in player.all_sim_results:
        round_sim_results.append(sim_result[round_i])
    results = {}
    # Find data from list of similar round number results.
    results['ave_sim_results'] = np.average(round_sim_results)
    results['std_sim_results'] = np.std(round_sim_results)
    results['percentile_sim_results'] = find_percentile_result_for_round(round_sim_results,percentiles_we_care_about)

    total_round_i = total_round_i - 1
    completion_percentages = [20,40,60,80,100]
    if round((round_i/total_round_i)*100) in completion_percentages:
        logging.info('\tPlayer: {}\t{}% complete.'.format(player.name,round((round_i/total_round_i)*100)))
    return results

def find_percentile_result_for_round(round_sim_results,percentiles_we_care_about):
    round_percentiles = {}
    for percentile in percentiles_we_care_about:
        result = np.percentile(round_sim_results, [percentile])
        round_percentiles[percentile] = result[0]
    return round_percentiles

def rearrange_percentile_results(percentile_sim_results,percentiles_we_care_about):
    new_results = {}
    for percentile in percentiles_we_care_about:
        percentile_series = []
        for i in range(len(percentile_sim_results)):
            percentile_series.append(percentile_sim_results[i][percentile])
        new_results[percentile] = percentile_series
    return new_results


####################################################################################################################
# Misc support
####################################################################################################################

def add_ts_to_filename(filename):
    split_fn = filename.split('.')
    dt = datetime.now()
    ts = str(datetime.timestamp(dt))
    ts.strip('.')
    return split_fn[0] + ts + '.' + split_fn[1]