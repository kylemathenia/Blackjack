#!/usr/bin/env python
from table import Table
from player import Player
from options import StrategyOptions
import simulations

def main():
    # Create players
    jake = Player('Jake', StrategyOptions.BASIC, money=1_000, standard_bet=25, play_as=False)
    kyle = Player('Kyle', StrategyOptions.BASIC_STAND_HARD_16, money=1_000, standard_bet=25, play_as=False)
    dillon = Player('Dillon', StrategyOptions.BASIC_HIT_HARD_16, money=1_000, standard_bet=25, play_as=False)
    diego = Player('Diego', StrategyOptions.BASIC_NEVER_DD, money=1_000, standard_bet=25, play_as=False)
    jung = Player('Jung', StrategyOptions.BASIC_NEVER_SPLIT, money=1_000, standard_bet=25, play_as=False)


    multiplayer_table = Table([jake,kyle,dillon,diego,jung], num_decks=1, shoe_shuffle_depth=0, min_bet=25, max_bet=1000,
                  blackjack_multiple=1.5, hit_soft_17=True, double_after_split=True, autoplay=True,
                  boot_when_poor=False,round_lim=1_000_000)
    multiplayer_table.play()

    # Create a table and sim.
    multiplayer_table = Table([jake,kyle,dillon,diego,jung], num_decks=1, shoe_shuffle_depth=0, min_bet=25, max_bet=1000,
                  blackjack_multiple=1.5, hit_soft_17=True, double_after_split=True, autoplay=True,
                  boot_when_poor=False,round_lim=1_000_000)
    simulations.multiplayer_table(multiplayer_table,num_rounds=1_000,sample_size=1_000,num_points=200,multiprocessing=True,save=False)

    # singleplayer_table = Table([jake], num_decks=1, shoe_shuffle_depth=0, min_bet=25, max_bet=1000,
    #               blackjack_multiple=1.5, hit_soft_17=True, double_after_split=True, autoplay=True,
    #               boot_when_poor=False,round_lim=100_000)

    singleplayer_table = Table([jake], num_decks=5, shoe_shuffle_depth=10, min_bet=25, max_bet=1000,
                  blackjack_multiple=1.5, hit_soft_17=False, double_after_split=False, autoplay=True,
                  boot_when_poor=False,round_lim=1_000_000)

    # multiplayer_table.play()

    # Simulate
    # Ideal: 150,000 rounds, 10,000 sample size, 500 num points. $5000 player money, $25 hands.
    # simulations.singleplayer_table(singleplayer_table,num_rounds=1000,sample_size=10_000,num_points=500,multiprocessing=True,save=True,filename_base='oneplayer_onetable_1krounds_5kmoney')
    # simulations.singleplayer_table(singleplayer_table,num_rounds=150_000,sample_size=15_000,num_points=500,multiprocessing=True,save=False,filename_base='oneplayer_onetable_150krounds_5kmoney')
    # Ideal: 10,000 rounds, 20,000 sample size, 500 num points
    # simulations.multiplayer_one_table(multiplayer_table,num_rounds=1_000,sample_size=10_000,num_points=500,multiprocessing=True,save=True)

if __name__ == '__main__':
    main()


# TODO
"""
-Make this a package so people can download, import and run their own simulations or play. 
-Make plots for different table configurations.
"""