


def prompt_make_bet(player,table):
    while True:
        bet = input("\n{}, how much would you like to wager?\n")
        if not bet.isnumeric():
            print("\nInvalid entry. Not a number.")
        elif bet < table.min_bet or bet > table.max_bet:
            print("\nInvalid entry. ${} is not in the table bet range of ${} - ${}".format(
                bet,table.min_bet,table.max_bet))
        elif bet > player.money:
            print("\nInvalid entry. {} is poor. They only have ${}".format(
                player.name, player.money))
        else:
            return int(bet)


def prompt_play_hand(player,hand,dealer):
    while True:
        print("\nPlayer: {}, Money: {}, Bet: {}\n\n")

def prompt_start_hand(player,hand):
    print("\nPlayer: {}, Money: {}, Bet: {}\n\n".format(player.name,player.money,hand.bet))