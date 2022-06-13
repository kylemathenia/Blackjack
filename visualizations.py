
from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np
from datetime import datetime

def one_table_multi_player(players,x_series):
    y_min = None
    y_max = 0
    for player in players:
        # if (max(player.std_sim_results) + max(player.ave_sim_results)) > y_max:
        #     y_max = max(player.std_sim_results) + max(player.ave_sim_results)
        # if y_min is None:
        #     y_min = min(player.ave_sim_results) - max(player.std_sim_results)
        # elif (min(player.std_sim_results) + min(player.ave_sim_results)) < y_min:
        #     y_min = min(player.ave_sim_results) - max(player.std_sim_results)

        if max(player.top10_percentile_sim_results) > y_max:
            y_max = max(player.top10_percentile_sim_results)
        if y_min is None:
            y_min = min(player.bot10_percentile_sim_results)
        elif min(player.bot10_percentile_sim_results) < y_min:
            y_min = min(player.bot10_percentile_sim_results)

    for i, player in enumerate(players):
        plt.figure(i)
        error = [player.top10_percentile_sim_results,player.bot10_percentile_sim_results]
        plt.plot(x_series, player.ave_sim_results,c='red')
        plt.plot(x_series, player.top10_percentile_sim_results, c='black')
        plt.plot(x_series, player.bot10_percentile_sim_results, c='black')



        # plt.errorbar(x_series, player.ave_sim_results, yerr=error, fmt='o-', ecolor='black', capsize=3, c='red')
        # plt.errorbar(x_series, player.ave_sim_results, yerr=player.std_sim_results, fmt='o-', ecolor='black', capsize=3, c='red')
        plt.ylim([y_min,y_max])
    plt.show()


def one_table_one_player(player, x_series,title,percentiles=None,filename='one_table_one_player.png',save=False):
    x_axis_multiplier=1000
    if percentiles is None:
        percentiles = [68, 95, 99]

    filename = add_ts_to_filename(filename)

    x_series = [num/x_axis_multiplier for num in x_series]
    max_percentile = max(percentiles)
    min_percentile = 100 - max_percentile
    percentile_results = player.sim_results.percentile_sim_results
    y_min = min(percentile_results[min_percentile])
    y_max = max(percentile_results[max_percentile])

    fig, ax = plt.subplots()
    ax.plot(x_series, player.sim_results.ave_sim_results,c='black')
    for percentile in percentiles:
        ax.fill_between(x_series, percentile_results[100-percentile], percentile_results[percentile], alpha=0.3,color='darkcyan')

    plt.ylim([y_min,y_max])
    plt.xlabel('Blackjack Rounds ({})'.format(x_axis_multiplier))
    plt.ylabel('Money ($)')
    plt.title(title)
    if save:
        plt.savefig(filename, dpi=1000, orientation='portrait')
    plt.show()


def find_y_lims(min_series = None, max_series = None):
    y_min = None
    y_max = 0
    if max(max_series) > y_max:
        y_max = max(max_series)
    if y_min is None:
        y_min = min(min_series)
    elif min(min_series) < y_min:
        y_min = min(min_series)

def add_ts_to_filename(filename):
    split_fn = filename.split('.')
    dt = datetime.now()
    ts = str(datetime.timestamp(dt))
    ts.strip('.')
    return split_fn[0] + ts + '.' + split_fn[1]