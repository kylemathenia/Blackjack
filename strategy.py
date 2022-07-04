

import pandas as pd
from options import ActionOptions as AO
from options import StrategyOptions,Cards
pd.set_option("display.max_rows", None, "display.max_columns", None)


def decide_bet(player,shoe,table):
    """Place bets for a hand. Each hand (if there are multiple) has a bet associated with it."""
    if player.strategy == StrategyOptions.BASIC:
        bet = player.standard_bet
    elif player.strategy == StrategyOptions.BASIC_HIT_HARD_16:
        bet = player.standard_bet
    elif player.strategy == StrategyOptions.BASIC_STAND_HARD_16:
        bet = player.standard_bet
    elif player.strategy == StrategyOptions.BASIC_NEVER_DD:
        bet = player.standard_bet
    elif player.strategy == StrategyOptions.BASIC_NEVER_SPLIT:
        bet = player.standard_bet
    ## used linear function which is not optitimal
    elif player.strategy == StrategyOptions.HI_LOW_COUNT:
        if shoe.true_count > 2:
            bet = player.standard_bet * shoe.true_count
        else:
            bet = player.standard_bet
    else:
        raise IOError
    return change_bet_if_poor(bet,player,table)

def change_bet_if_poor(bet,player,table):
    # TODO need to make sure to not bet more than is committed with other hands.
    if player.money < table.min_bet:
        return 0
    elif bet > player.money:
        return table.min_bet
    else:
        return bet

def decide_action(player,hand,dealer,table,strategy):
    if strategy == StrategyOptions.BASIC:
        action = basic_strategy_action(player,hand,dealer,table)

    elif strategy == StrategyOptions.BASIC_HIT_HARD_16:
        if not hand.hand_soft and hand.best_value == 16:
            action = AO.HIT
        else:
            action = basic_strategy_action(player,hand,dealer,table)

    elif strategy == StrategyOptions.BASIC_STAND_HARD_16:
        if not hand.hand_soft and hand.best_value == 16:
            action = AO.STAND
        else:
            action = basic_strategy_action(player,hand,dealer,table)

    elif strategy == StrategyOptions.BASIC_NEVER_DD:
        action = basic_strategy_action(player, hand, dealer, table)
        if action == AO.DD_OR_STAND or action == AO.DD_OR_HIT:
            action = no_double_down_action(action)
        elif action == AO.DOUBLE_DOWN:
            action = AO.HIT

    elif strategy == StrategyOptions.BASIC_NEVER_SPLIT:
        action = basic_strategy_action(player, hand, dealer, table)
        if action == AO.SPLIT:
            action = AO.HIT

    elif strategy == StrategyOptions.DEALER:
        action = dealer_strategy_action(hand,table)

    elif strategy == StrategyOptions.HI_LOW_COUNT:
        action = deviation_strategy_action(player,hand,dealer,table)

    else:
        raise KeyError

    if action == AO.DD_OR_STAND or action == AO.DD_OR_HIT or action == AO.DOUBLE_DOWN:
        action = check_double_down(action,hand,table,player)
    if action == AO.SPLIT:
        action = check_split(action, hand, table, player)
    return action

def basic_strategy_action(player,hand,dealer,table):
    dealer_card = dealer.hands[0].cards[0]
    if hand.is_double and len(player.hands)<3:
        double_card_index = hand.cards[0].card_value[-1]
        if split_map[dealer_card][double_card_index]:
            return AO.SPLIT
    if hand.hand_soft:
        action = basic_soft_hand_map[dealer_card][hand.soft_total_low]
    else:
        action = basic_hard_hand_map[dealer_card][hand.hard_sum]
    return action

def deviation_strategy_action(player, hand, dealer, table):
    dealer_card = dealer.hands[0].cards[0]
    true_count = table.shoe.true_count
    if hand.is_double and len(player.hands)<3:
        double_card_index = hand.cards[0].card_value[-1]
        split_deviation_entry = deviations_split_map[dealer_card][double_card_index]
        if split_deviation_entry[0] and len(split_deviation_entry) == 1:
            return AO.SPLIT
        if len(split_deviation_entry) == 3:
            dev_count = split_deviation_entry[-1]
            if dev_count <= true_count:
                return AO.SPLIT
    if hand.hand_soft:
        if len(deviations_soft_hand_map[dealer_card][hand.soft_total_low]) == 3:
            action_list = deviations_soft_hand_map[dealer_card][hand.soft_total_low]
            if true_count >= action_list[2]:
                action = action_list[0]
            else:
                action = action_list[1]
        else:
            action = deviations_soft_hand_map[dealer_card][hand.soft_total_low][0]
    else:
        if len(deviations_basic_hard_hand_map[dealer_card][hand.hard_sum]) == 3:
            action_list = deviations_basic_hard_hand_map[dealer_card][hand.hard_sum]
            deviation = action_list[2]
            if deviation < 0:
                if true_count <= deviation:
                    action = action_list[0]
                else:
                    action = action_list[1]
            if deviation > 0:
                if true_count >= deviation:
                    action = action_list[0]
                else:
                    action = action_list[1]
        else:
            action = deviations_basic_hard_hand_map[dealer_card][hand.hard_sum][0]
    return action

def dealer_strategy_action(hand,table):
    if hand.best_value > 17:
        return AO.STAND
    elif hand.hand_soft and hand.soft_total_high == 17:
        if table.hit_soft_17:
            return AO.HIT
        else:
            return AO.STAND
    elif hand.best_value == 17:
        return AO.STAND
    else:
        return AO.HIT

def check_double_down(action,hand,table,player):
    """Checks the action to see if it is a double down variety. Modifies action if double down isn't legal."""
    if action != AO.DD_OR_HIT and action != AO.DD_OR_STAND:
        return action
    elif len(hand.cards) > 2:
        return no_double_down_action(action)
    elif player.has_split_hands and not table.double_after_split:
        return no_double_down_action(action)
    elif hand.bet*2 > player.money:
        return no_double_down_action(action)
    elif (player.money - player.total_bet_for_round - hand.bet) < 0:
        return no_double_down_action(action)
    else:
        return AO.DOUBLE_DOWN

def check_split(action,hand,table,player):
    """Can only split if you have enough money to cover the other hand. Modifies action if double down isn't legal."""
    # Need to add a check to make sure the table allows multiple splits.
    if (player.bet_size*2)>player.money:
        pass
    if (player.money - player.total_bet_for_round) < hand.bet:
        return AO.HIT
    else:
        return AO.SPLIT

def no_double_down_action(action):
    if action == AO.DD_OR_STAND: return AO.STAND
    else: return AO.HIT






####################################################################################################################
# Creating the hash maps.
####################################################################################################################

def get_basic_hard_hand_map():
    """Basic strategy according to https://www.blackjackapprenticeship.com/blackjack-strategy-charts/"""
    df_below_9 = pd.DataFrame({
        Cards.TWO: [AO.HIT],
        Cards.THREE: [AO.HIT],
        Cards.FOUR: [AO.HIT],
        Cards.FIVE: [AO.HIT],
        Cards.SIX: [AO.HIT],
        Cards.SEVEN: [AO.HIT],
        Cards.EIGHT: [AO.HIT],
        Cards.NINE: [AO.HIT],
        Cards.TEN: [AO.HIT],
        Cards.JACK: [AO.HIT],
        Cards.QUEEN: [AO.HIT],
        Cards.KING: [AO.HIT],
        Cards.ACE: [AO.HIT]})
    hard_hand_df = pd.DataFrame({
        Cards.TWO: [AO.HIT, AO.DD_OR_HIT, AO.DD_OR_HIT, AO.HIT, AO.STAND, AO.STAND, AO.STAND, AO.STAND],
        Cards.THREE: [AO.DD_OR_HIT, AO.DD_OR_HIT, AO.DD_OR_HIT, AO.HIT, AO.STAND, AO.STAND, AO.STAND,
                          AO.STAND],
        Cards.FOUR: [AO.DD_OR_HIT, AO.DD_OR_HIT, AO.DD_OR_HIT, AO.STAND, AO.STAND, AO.STAND, AO.STAND,
                          AO.STAND],
        Cards.FIVE: [AO.DD_OR_HIT, AO.DD_OR_HIT, AO.DD_OR_HIT, AO.STAND, AO.STAND, AO.STAND, AO.STAND,
                          AO.STAND],
        Cards.SIX: [AO.DD_OR_HIT, AO.DD_OR_HIT, AO.DD_OR_HIT, AO.STAND, AO.STAND, AO.STAND, AO.STAND,
                          AO.STAND],
        Cards.SEVEN: [AO.HIT, AO.DD_OR_HIT, AO.DD_OR_HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT],
        Cards.EIGHT: [AO.HIT, AO.DD_OR_HIT, AO.DD_OR_HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT],
        Cards.NINE: [AO.HIT, AO.DD_OR_HIT, AO.DD_OR_HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT],
        Cards.TEN: [AO.HIT, AO.HIT, AO.DD_OR_HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT],
        Cards.JACK: [AO.HIT, AO.HIT, AO.DD_OR_HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT],
        Cards.QUEEN: [AO.HIT, AO.HIT, AO.DD_OR_HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT],
        Cards.KING: [AO.HIT, AO.HIT, AO.DD_OR_HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT],
        Cards.ACE: [AO.HIT, AO.HIT, AO.DD_OR_HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT]})
    df_above_16 = pd.DataFrame({
        Cards.TWO: [AO.STAND],
        Cards.THREE: [AO.STAND],
        Cards.FOUR: [AO.STAND],
        Cards.FIVE: [AO.STAND],
        Cards.SIX: [AO.STAND],
        Cards.SEVEN: [AO.STAND],
        Cards.EIGHT: [AO.STAND],
        Cards.NINE: [AO.STAND],
        Cards.TEN: [AO.STAND],
        Cards.JACK: [AO.STAND],
        Cards.QUEEN: [AO.STAND],
        Cards.KING: [AO.STAND],
        Cards.ACE: [AO.STAND]})
    df = pd.DataFrame()
    for i in range(4, 9):
        df = df.append(df_below_9)
    df = df.append(hard_hand_df)
    for i in range(17, 22):
        df = df.append(df_above_16)
    df.index = range(4, 22)
    return dict(df)

def get_basic_soft_hand_map():
    """Basic strategy according to https://www.blackjackapprenticeship.com/blackjack-strategy-charts/"""
    df = pd.DataFrame({
        Cards.TWO: [AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.DD_OR_STAND, AO.STAND, AO.STAND, AO.STAND],
        Cards.THREE: [AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.DD_OR_HIT, AO.DD_OR_STAND, AO.STAND, AO.STAND, AO.STAND],
        Cards.FOUR: [AO.HIT, AO.HIT, AO.DD_OR_HIT, AO.DD_OR_HIT, AO.DD_OR_HIT, AO.DD_OR_STAND, AO.STAND, AO.STAND, AO.STAND],
        Cards.FIVE: [AO.DD_OR_HIT, AO.DD_OR_HIT, AO.DD_OR_HIT, AO.DD_OR_HIT, AO.DD_OR_HIT, AO.DD_OR_STAND, AO.STAND, AO.STAND, AO.STAND],
        Cards.SIX: [AO.DD_OR_HIT, AO.DD_OR_HIT, AO.DD_OR_HIT, AO.DD_OR_HIT, AO.DD_OR_HIT, AO.DD_OR_STAND, AO.DD_OR_STAND, AO.STAND, AO.STAND],
        Cards.SEVEN: [AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.STAND, AO.STAND, AO.STAND, AO.STAND],
        Cards.EIGHT: [AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.STAND, AO.STAND, AO.STAND, AO.STAND],
        Cards.NINE: [AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.STAND, AO.STAND, AO.STAND],
        Cards.TEN: [AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.STAND, AO.STAND, AO.STAND],
        Cards.JACK: [AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.STAND, AO.STAND, AO.STAND],
        Cards.QUEEN: [AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.STAND, AO.STAND, AO.STAND],
        Cards.KING: [AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.STAND, AO.STAND, AO.STAND],
        Cards.ACE: [AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.HIT, AO.STAND, AO.STAND, AO.STAND]})
    df.index = range(3, 12)
    return dict(df)

def get_split_map():
    """Basic strategy according to https://www.blackjackapprenticeship.com/blackjack-strategy-charts/"""
    df = pd.DataFrame({
        Cards.TWO: [False, False, False, False, False, True, True, True, False, True],
        Cards.THREE: [False, False, False, False, True, True, True, True, False, True],
        Cards.FOUR: [True, True, False, False, True, True, True, True, False, True],
        Cards.FIVE: [True, True, False, False, True, True, True, True, False, True],
        Cards.SIX: [True, True, False, False, True, True, True, True, False, True],
        Cards.SEVEN: [True, True, False, False, False, True, True, False, False, True],
        Cards.EIGHT: [False, False, False, False, False, False, True, True, False, True],
        Cards.NINE: [False, False, False, False, False, False, True, True, False, True],
        Cards.TEN: [False, False, False, False, False, False, True, False, False, True],
        Cards.JACK: [False, False, False, False, False, False, True, False, False, True],
        Cards.QUEEN: [False, False, False, False, False, False, True, False, False, True],
        Cards.KING: [False, False, False, False, False, False, True, False, False, True],
        Cards.ACE: [False, False, False, False, False, False, True, False, False, True]})
    df.index = range(2, 12)
    return dict(df)

def get_deviations_basic_hard_hand_map():
    """Basic strategy according to https://www.blackjackapprenticeship.com/blackjack-strategy-charts/"""
    df_below_6 = pd.DataFrame({
        Cards.TWO: [[AO.HIT]],
        Cards.THREE: [[AO.HIT]],
        Cards.FOUR: [[AO.HIT]],
        Cards.FIVE: [[AO.HIT]],
        Cards.SIX: [[AO.HIT]],
        Cards.SEVEN: [[AO.HIT]],
        Cards.EIGHT: [[AO.HIT]],
        Cards.NINE: [[AO.HIT]],
        Cards.TEN: [[AO.HIT]],
        Cards.JACK: [[AO.HIT]],
        Cards.QUEEN: [[AO.HIT]],
        Cards.KING: [[AO.HIT]],
        Cards.ACE: [[AO.HIT]]})
    hard_hand_df = pd.DataFrame({
        Cards.TWO: [[AO.HIT], [AO.DD_OR_HIT, AO.HIT, 1], [AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.STAND, AO.HIT, 3], [AO.HIT, AO.STAND,-1], [AO.STAND], [AO.STAND], [AO.STAND]],
        Cards.THREE: [[AO.HIT], [AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.STAND, AO.HIT, 2], [AO.STAND], [AO.STAND], [AO.STAND], [AO.STAND]],
        Cards.FOUR: [[AO.HIT], [AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.HIT, AO.STAND,-.5], [AO.STAND], [AO.STAND], [AO.STAND], [AO.STAND]],
        Cards.FIVE: [[AO.HIT], [AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.STAND], [AO.STAND], [AO.STAND], [AO.STAND], [AO.STAND]],
        Cards.SIX: [[AO.DD_OR_HIT,AO.HIT, 2], [AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.STAND], [AO.STAND], [AO.STAND], [AO.STAND], [AO.STAND]],
        Cards.SEVEN: [[AO.HIT], [AO.DD_OR_HIT, AO.HIT, 3], [AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT]],
        Cards.EIGHT: [[AO.HIT], [AO.HIT], [AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT]],
        Cards.NINE: [[AO.HIT], [AO.HIT], [AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.HIT], [AO.HIT],[ AO.HIT], [AO.HIT], [AO.STAND, AO.HIT, 4]],
        Cards.TEN: [[AO.HIT], [AO.HIT], [AO.DD_OR_HIT,AO.HIT,4], [AO.DD_OR_HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.STAND,AO.HIT,4], [AO.STAND, AO.HIT,.5]],
        Cards.JACK: [[AO.HIT], [AO.HIT], [AO.DD_OR_HIT,AO.HIT,4], [AO.DD_OR_HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.STAND,AO.HIT,4], [AO.STAND, AO.HIT,.5]],
        Cards.QUEEN: [[AO.HIT], [AO.HIT], [AO.DD_OR_HIT,AO.HIT,4], [AO.DD_OR_HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.STAND,AO.HIT,4], [AO.STAND, AO.HIT,.5]],
        Cards.KING: [[AO.HIT], [AO.HIT], [AO.DD_OR_HIT,AO.HIT,4], [AO.DD_OR_HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.STAND,AO.HIT,4], [AO.STAND, AO.HIT,.5]],
        Cards.ACE: [[AO.HIT],[ AO.HIT], [AO.DD_OR_HIT,AO.HIT,4], [AO.DD_OR_HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT]]})
    df_above_16 = pd.DataFrame({
        Cards.TWO: [[AO.STAND]],
        Cards.THREE: [[AO.STAND]],
        Cards.FOUR: [[AO.STAND]],
        Cards.FIVE: [[AO.STAND]],
        Cards.SIX: [[AO.STAND]],
        Cards.SEVEN: [[AO.STAND]],
        Cards.EIGHT: [[AO.STAND]],
        Cards.NINE: [[AO.STAND]],
        Cards.TEN: [[AO.STAND]],
        Cards.JACK: [[AO.STAND]],
        Cards.QUEEN: [[AO.STAND]],
        Cards.KING: [[AO.STAND]],
        Cards.ACE: [[AO.STAND]]})
    df = pd.DataFrame()
    for i in range(4, 8):
        df = df.append(df_below_6)
    df = df.append(hard_hand_df)
    for i in range(17, 22):
        df = df.append(df_above_16)
    df.index = range(4, 22)
    return dict(df)

def get_deviations_soft_hand_map():
    """Basic strategy according to https://www.blackjackapprenticeship.com/blackjack-strategy-charts/"""
    df = pd.DataFrame({
        Cards.TWO: [[AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.DD_OR_HIT,AO.HIT, 1], [AO.DD_OR_STAND], [AO.STAND], [AO.STAND], [AO.STAND]],
        Cards.THREE: [[AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.DD_OR_HIT], [AO.DD_OR_STAND], [AO.STAND], [AO.STAND], [AO.STAND]],
        Cards.FOUR: [[AO.HIT], [AO.HIT], [AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.DD_OR_STAND], [AO.DD_OR_STAND,AO.STAND, 3], [AO.STAND], [AO.STAND]],
        Cards.FIVE: [[AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.DD_OR_STAND], [AO.DD_OR_STAND, AO.STAND, 1], [AO.STAND], [AO.STAND]],
        Cards.SIX: [[AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.DD_OR_HIT], [AO.DD_OR_STAND], [AO.DD_OR_STAND], [AO.STAND], [AO.STAND]],
        Cards.SEVEN: [[AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.STAND], [AO.STAND], [AO.STAND], [AO.STAND]],
        Cards.EIGHT: [[AO.HIT], [AO.HIT], [AO.HIT],[ AO.HIT], [AO.HIT], [AO.STAND], [AO.STAND], [AO.STAND], [AO.STAND]],
        Cards.NINE: [[AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.STAND], [AO.STAND], [AO.STAND]],
        Cards.TEN: [[AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.STAND], [AO.STAND], [AO.STAND]],
        Cards.JACK: [[AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.STAND], [AO.STAND], [AO.STAND]],
        Cards.QUEEN: [[AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.STAND], [AO.STAND], [AO.STAND]],
        Cards.KING: [[AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.STAND], [AO.STAND], [AO.STAND]],
        Cards.ACE: [[AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.HIT], [AO.STAND], [AO.STAND], [AO.STAND]]})
    df.index = range(3, 12)
    return dict(df)

def get_deviations_split_map():
    """Basic strategy according to https://www.blackjackapprenticeship.com/blackjack-strategy-charts/"""
    df = pd.DataFrame({
        Cards.TWO:      [[False], [False], [False], [False], [False], [True], [True], [True], [False], [True]],
        Cards.THREE:    [[False], [False], [False], [False], [True], [True], [True], [True], [False], [True]],
        Cards.FOUR:     [[True], [True], [False], [False], [True], [True], [True], [True], [True,False,6], [True]],
        Cards.FIVE:     [[True], [True], [False], [False], [True], [True], [True], [True], [True,False,5], [True]],
        Cards.SIX:      [[True], [True], [False], [False], [True], [True], [True], [True], [True,False,4], [True]],
        Cards.SEVEN:    [[True], [True], [False], [False], [False], [True], [True], [False], [False], [True]],
        Cards.EIGHT:    [[False], [False], [False], [False], [False], [False], [True], [True], [False], [True]],
        Cards.NINE:     [[False], [False], [False], [False], [False], [False], [True], [True], [False], [True]],
        Cards.TEN:      [[False], [False], [False], [False], [False], [False], [True], [False], [False], [True]],
        Cards.JACK:     [[False], [False], [False], [False], [False], [False], [True], [False], [False], [True]],
        Cards.QUEEN:    [[False], [False], [False], [False], [False], [False], [True], [False], [False], [True]],
        Cards.KING:     [[False], [False], [False], [False], [False], [False], [True], [False], [False], [True]],
        Cards.ACE:      [[False], [False], [False], [False], [False], [False], [True], [False], [False], [True]]})
    df.index = range(2, 12)
    return dict(df)


basic_hard_hand_map = get_basic_hard_hand_map()
basic_soft_hand_map = get_basic_soft_hand_map()
split_map = get_split_map()
deviations_basic_hard_hand_map = get_deviations_basic_hard_hand_map()
deviations_soft_hand_map = get_deviations_soft_hand_map()
deviations_split_map = get_deviations_split_map()