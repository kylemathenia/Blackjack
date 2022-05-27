import strategy
from options import ActionOptions as AO
from options import StrategyOptions

action_to_num_map = {AO.STAND:'1',AO.HIT:'2',AO.DOUBLE_DOWN:'3',AO.SPLIT:'4',AO.BASIC_STRATEGY:'5',AO.HI_LOW_STRATEGY:'6'}
num_to_action_map = {'1':AO.STAND,'2':AO.HIT,'3':AO.DOUBLE_DOWN,'4':AO.SPLIT,'5':AO.BASIC_STRATEGY,'6':AO.HI_LOW_STRATEGY}

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
    print("\n\n\n\n\n\n\n\n\n####################################")
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
    if not table.autoplay:
        input("\nPress <Enter>")

def prompts_exit_game():
    #TODO Keep track of player stats throughout the game a print them here. Highest money achieved. Num rounds played.
    #winning percentage, etc.
    print("\nExiting game.\n")


def prompt_start_hand(player,hand):
    print("\n########################################\nPlayer: {}, Money: {}, Bet: {}".format(
        player.name,player.money,hand.bet))

def show_sim_results(table):
    print("\n\nSIM RESULTS:\n")
    print("Number of rounds: {}\n".format(table.num_rounds))
    for player in table.players:
        print("Player: {}\nMoney: ${}\nWinnings: {}".format(player.name,player.money,player.money-player.starting_money))