
import visualizations

def one_player_one_table(table,num_rounds=1_000,sample_size=1_000,num_points=100,multiprocessing=True,save=False):
    assert(len(table.players) == 1)
    increment = int(num_rounds/num_points)
    x_series = list(range(0,num_rounds+increment,increment))
    table.simulate(x_series, sample_size=sample_size, multiprocessing=multiprocessing)

    player = table.players[0]
    print('\n########## RESULTS ##########\n')
    for i, round_number in enumerate(x_series):
        ave_sim_results = player.sim_results.ave_sim_results[i]
        print('Round number: {:<20}Ave money: ${:.2f}{:<10}Ave winnings: ${:.2f}'.format(round_number,ave_sim_results,' ',ave_sim_results-player.starting_money))
    print('\nAverage loss per round: \n${:.4f}'.format(player.sim_results.ave_loss_per_round))
    print('\nSample size: \n{}'.format(sample_size))
    title = 'Basic Strategy - 25 Dollar Hands'
    visualizations.one_table_one_player(player,x_series,title,save=save)