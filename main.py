
from table import Table
from player import Player
from options import StrategyOptions
import simulations

def main():
    # Create players
    jake = Player('Jake', StrategyOptions.BASIC, money=5_000, standard_bet=25, play_as=False)
    kyle = Player('Kyle', StrategyOptions.BASIC, money=5_000, standard_bet=25, play_as=False)
    # Create tables
    multiplayer_table = Table([jake,kyle], num_decks=1, shoe_shuffle_depth=0, min_bet=25, max_bet=1000,
                  blackjack_multiple=1.5, hit_soft_17=True, double_after_split=True, autoplay=True,
                  boot_when_poor=False,round_lim=100_000)

    singleplayer_table = Table([jake], num_decks=1, shoe_shuffle_depth=0, min_bet=25, max_bet=1000,
                  blackjack_multiple=1.5, hit_soft_17=True, double_after_split=True, autoplay=True,
                  boot_when_poor=False,round_lim=100_000)

    # multiplayer_table.play()

    # Simulate
    simulations.one_player_one_table(singleplayer_table,num_rounds=200_000,sample_size=10,num_points=500,multiprocessing=True,save=False)

if __name__ == '__main__':
    main()


# We want to see:
# 1. What happens if you play basic strategy with different table rules.
# -Create a bunch of different tables and simulate.
# 2. What happens if you play basic strategy a little wrong compared to regular strategy.
# - Create one table and simulate.
# 3. What happens if the table has different min bets.
# - Create a bunch of different tables and simulate.

# The data from the simulation should be, for each player, a timeseries of mean scores, and standard deviations at those means.
# Arguments:
# x series as an argument, which is a list of the round numbers to record data at.
# Sample size.

# Returns:
# List of players.
# Each player sim_mean_scores sim_std_scores.