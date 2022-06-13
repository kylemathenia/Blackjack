
import visualizations
import support
import logging

def one_player_one_table(table,num_rounds=1_000,sample_size=1_000,num_points=100,multiprocessing=True,save=False,filename_base='one_player_one_table'):
    assert(len(table.players) == 1)
    if num_rounds < num_points:
        logging.warning(
            "\nnum_rounds argument must be greater than or equal num_points argument. Changing to num_points = num_rounds.\n")
        num_points = num_rounds
    increment = round(num_rounds / num_points)
    x_series = list(range(0,num_rounds+increment,increment))
    table.simulate(x_series, sample_size=sample_size, multiprocessing=multiprocessing)

    player = table.players[0]
    print('\n########## RESULTS ##########\n')
    for i, round_number in enumerate(x_series):
        ave_sim_results = player.sim_results.ave_sim_results[i]
        print('Round number: {:<20}Ave money: ${:.2f}{:<10}Ave winnings: ${:.2f}'.format(round_number,ave_sim_results,' ',ave_sim_results-player.starting_money))
    print('\nAverage loss per round: \n${:.4f}'.format(player.sim_results.ave_loss_per_round))
    print('\nSample size: \n{}'.format(sample_size))
    title = 'Basic Strategy - 25 Dollar Hands - 1,2,3 Sigma'
    if save:
        save_one_player_one_table(x_series,table,sample_size,filename_base=filename_base)
    visualizations.one_table_one_player(player,x_series,title,save=save,filename_base=filename_base)

def save_one_player_one_table(x_series,table,sample_size,filename_base='one_player_one_table'):
    filename=filename_base+'.txt'
    filename = support.add_ts_to_filename(filename)
    with open(filename, 'w') as f:
        player = table.players[0]
        f.write('\n########## RESULTS ##########\n')
        for i, round_number in enumerate(x_series):
            ave_sim_results = player.sim_results.ave_sim_results[i]
            f.write('\nRound number: {:<20}Ave money: ${:.2f}{:<10}Ave winnings: ${:.2f}'.format(round_number,ave_sim_results, ' ',ave_sim_results - player.starting_money))
        f.write('\n\nAverage loss per round: \n${:.4f}'.format(player.sim_results.ave_loss_per_round))
        f.write('\n\nSample size: \n{}'.format(sample_size))


def multiplayer_one_table(table,num_rounds=1_000,sample_size=1_000,num_points=100,multiprocessing=True,save=False,filename_base='one_player_one_table'):
    if num_rounds < num_points:
        logging.warning("\nnum_rounds argument must be greater than or equal num_points argument. Changing to num_points = num_rounds.\n")
        num_points=num_rounds
    increment = round(num_rounds / num_points)
    x_series = list(range(0,num_rounds+increment,increment))
    table.simulate(x_series, sample_size=sample_size, multiprocessing=multiprocessing)

    print('\n########## RESULTS ##########\n')
    for i, round_number in enumerate(x_series):
        print('\nRound number: {}'.format(round_number))
        for player in table.players:
            print('{:<10}\t Ave Money: ${:.2f}'.format(player.name,player.sim_results.ave_sim_results[i]))
    print('\nAVERAGE LOSS PER ROUND')
    for player in table.players:
        print('{:<10}\t ${:.4f}'.format(player.name,player.sim_results.ave_loss_per_round))
    print('\nPLAYER INFO')
    for player in table.players:
        print(player.info)
    print('\nSample size: \n{}'.format(sample_size))

    if save:
        save_multiplayer_one_table(x_series,table,sample_size,filename_base=filename_base)
    visualizations.strategy_comparison(table.players,x_series,save=save,filename_base=filename_base)

def save_multiplayer_one_table(x_series,table,sample_size,filename_base='multiplayer_one_table'):
    filename=filename_base+'.txt'
    filename = support.add_ts_to_filename(filename)
    with open(filename, 'w') as f:
        f.write('\n########## RESULTS ##########\n')
        for i, round_number in enumerate(x_series):
            f.write('\nRound number: {}\n'.format(round_number))
            for player in table.players:
                f.write('{:<10} Ave Money: ${:.2f}\n'.format(player.name, player.sim_results.ave_sim_results[i]))
        f.write('\n\nAVERAGE LOSS PER ROUND\n')
        for player in table.players:
            f.write('{:<10} ${:.4f}\n'.format(player.name, player.sim_results.ave_loss_per_round))
        f.write('\n\nPLAYER INFO\n')
        for player in table.players:
            f.write(player.info)
            f.write('\n')
        f.write('\n\nSample size: \n{}'.format(sample_size))