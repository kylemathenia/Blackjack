
from table import Table
from player import Player
from options import StrategyOptions
import copy

# Create players
jake = Player('Jake', StrategyOptions.HI_LOW_COUNT, money=5_000_000, standard_bet=50, play_as=False)
kyle = Player('Kyle',StrategyOptions.BASIC,money=5_000_000,standard_bet=50,play_as=False)

# Create table
t = Table([jake, kyle],num_decks=1,shoe_shuffle_depth=0,min_bet=5,max_bet=10000,
                 blackjack_multiple=1.5,hit_soft_17=True,double_after_split=True,autoplay=False)

# t.play()
t.sim_and_print(1_000_000)
t.simulate([100,200,300,400,500], 50)
# Find all the player sim results as shown below.
for player in t.players:
    player.ave_sim_results
    player.std_sim_results

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