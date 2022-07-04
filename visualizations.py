"""Visualization functions for blackjack table simulations."""

from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np
import support


def strategy_comparison(players,x_series,title = 'Strategy Comparison - Median Player',filename_base='one_table_one_player',save=False):
    filename = filename_base + '.png'
    filename = support.add_ts_to_filename(filename)

    x_axis_multiplier=1
    x_series = [num/x_axis_multiplier for num in x_series]
    y_min = None
    y_min = 0
    y_max = 0
    for player in players:
        med_results = player.sim_results.percentile_sim_results[50]
        if max(med_results) > y_max:
            y_max = max(med_results)
        if y_min is None:
            y_min = min(med_results)
        elif min(med_results) < y_min:
            y_min = min(med_results)

    for i, player in enumerate(players):
        y_series = player.sim_results.percentile_sim_results[50]
        new_x_series = np.linspace(min(x_series), max(x_series), 1000)
        spl = make_interp_spline(x_series, y_series, k=5)
        pretty_spline = spl(new_x_series)
        plt.plot(new_x_series, pretty_spline)

    plt.xlabel('Blackjack Rounds ({})'.format(x_axis_multiplier))
    plt.ylabel('Money ($)')
    plt.title(title)
    plt.ylim([y_min,y_max])
    legend = []
    for player in players:
        legend.append(player.strategy.name)
    plt.legend(legend, title="Strategies")
    if save:
        plt.savefig(filename, dpi=1000, orientation='portrait')
    plt.show()


def one_table_one_player(player,x_series,title,percentiles=None,filename_base='one_table_one_player',save=False):
    filename = filename_base + '.png'
    filename = support.add_ts_to_filename(filename)

    if percentiles is None:
        percentiles = [68,95,99]
    x_axis_multiplier=1000
    x_series = [num/x_axis_multiplier for num in x_series]
    max_percentile = max(percentiles)
    min_percentile = 100 - max_percentile
    percentile_results = player.sim_results.percentile_sim_results
    y_min = min(percentile_results[min_percentile])
    y_max = max(percentile_results[max_percentile])

    fig, ax = plt.subplots()
    even_money = [player.starting_money for i in x_series]
    ax.plot(x_series,even_money,':',color='grey')
    ax.fill_between(x_series, percentile_results[50], percentile_results[50], alpha=1,color='black')
    for percentile in percentiles:
        ax.fill_between(x_series, percentile_results[100-percentile], percentile_results[percentile], alpha=0.3,color='darkcyan')

    plt.ylim([y_min,y_max])
    plt.xlabel('Blackjack Rounds ({})'.format(x_axis_multiplier))
    plt.ylabel('Money ($)')
    plt.title(title)
    if save:
        plt.savefig(filename, dpi=1000, orientation='portrait')
    plt.show()

