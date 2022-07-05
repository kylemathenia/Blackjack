#!/usr/bin/env python
from table import Table
from player import Player
from options import StrategyOptions
import simulations

def main():
    # Single-player sim
    ####################################################################################################################
    # Create a player.
    jake = Player('Jake', StrategyOptions.BASIC, money=1_000, standard_bet=25, play_as=False)
    # Create a table.
    singleplayer_table = Table([jake], num_decks=5, shoe_shuffle_depth=10, min_bet=25, max_bet=1000,
                  blackjack_multiple=1.5, hit_soft_17=False, double_after_split=False)
    # Simulate a single-player table.
    simulations.singleplayer_table(singleplayer_table,num_rounds=1_000,sample_size=1_000,num_points=200,
                                   multiprocessing=True,save=True,filename_base='single-player')

    # Multi-player sim
    ####################################################################################################################
    # Simulate multiple players with different strategies.
    jake = Player('Jake', StrategyOptions.BASIC, money=1_000, standard_bet=25, play_as=False)
    kyle = Player('Kyle', StrategyOptions.BASIC_STAND_HARD_16, money=1_000, standard_bet=25, play_as=False)
    dillon = Player('Dillon', StrategyOptions.BASIC_HIT_HARD_16, money=1_000, standard_bet=25, play_as=False)
    diego = Player('Diego', StrategyOptions.BASIC_NEVER_DD, money=1_000, standard_bet=25, play_as=False)
    jung = Player('Jung', StrategyOptions.BASIC_NEVER_SPLIT, money=1_000, standard_bet=25, play_as=False)

    multiplayer_table = Table([jake,kyle,dillon,diego,jung], num_decks=5, shoe_shuffle_depth=10, min_bet=25, max_bet=1000,
                  blackjack_multiple=1.5, hit_soft_17=True, double_after_split=True)
    simulations.multiplayer_table(multiplayer_table,num_rounds=1_000,sample_size=1_000,num_points=200,
                                  multiprocessing=True,save=False,filename_base='multi-player')

    # Play as a player.
    ####################################################################################################################

    # Play blackjack as a player.
    jake = Player('Jake', StrategyOptions.BASIC, money=1_000, standard_bet=25, play_as=True)
    multiplayer_table = Table([jake,kyle,dillon,diego,jung], num_decks=5, shoe_shuffle_depth=10, min_bet=25, max_bet=1000,
                  blackjack_multiple=1.5, hit_soft_17=True, double_after_split=True)
    multiplayer_table.play()


if __name__ == '__main__':
    main()
