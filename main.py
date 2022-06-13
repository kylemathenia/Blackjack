
from table import Table
from player import Player
from options import StrategyOptions
import simulations

def main():
    # Create players
    jake = Player('Jake', StrategyOptions.BASIC, money=5_000, standard_bet=25, play_as=False)
    kyle = Player('Kyle', StrategyOptions.BASIC_STAND_HARD_16, money=5_000, standard_bet=25, play_as=False)
    dillon = Player('Dillon', StrategyOptions.BASIC_HIT_HARD_16, money=5_000, standard_bet=25, play_as=False)
    diego = Player('Diego', StrategyOptions.BASIC_NEVER_DD, money=5_000, standard_bet=25, play_as=False)
    jung = Player('Jung', StrategyOptions.BASIC_NEVER_SPLIT, money=5_000, standard_bet=25, play_as=False)

    # Create tables
    multiplayer_table = Table([jake,kyle,dillon,diego,jung], num_decks=1, shoe_shuffle_depth=0, min_bet=25, max_bet=1000,
                  blackjack_multiple=1.5, hit_soft_17=True, double_after_split=True, autoplay=True,
                  boot_when_poor=False,round_lim=100_000)

    singleplayer_table = Table([jake], num_decks=1, shoe_shuffle_depth=0, min_bet=25, max_bet=1000,
                  blackjack_multiple=1.5, hit_soft_17=True, double_after_split=True, autoplay=True,
                  boot_when_poor=False,round_lim=100_000)

    # multiplayer_table.play()

    # Simulate
    # Ideal: 300,000 rounds, 10,000 sample size, 500 num points
    # simulations.one_player_one_table(singleplayer_table,num_rounds=300_000,sample_size=10_000,num_points=500,multiprocessing=True,save=True,filename_base='one_player_one_table_300000_rounds')
    # Ideal: 10,000 rounds, 20,000 sample size, 500 num points
    simulations.multiplayer_one_table(multiplayer_table,num_rounds=100,sample_size=2000,num_points=500,multiprocessing=True,save=False)

if __name__ == '__main__':
    main()


# We want to see:
# 1. What happens if you play basic strategy with different table rules.
# -Create a bunch of different tables and simulate.
# 2. What happens if you play basic strategy a little wrong compared to regular strategy.
# - Create one table and simulate.
# 3. What happens if the table has different min bets.
# - Create a bunch of different tables and simulate.