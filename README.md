# Blackjack
 
Simulate blackjack for different table configurations and player strategies. Some interesting takeaways were:
1) How slowly you lose money playing perfect basic strategy. 
2) How much quicker you lose money if you play basic strategy just a little bit wrong.
3) How much quicker you lose money if you are close to bankrupt, or don't bring a decent bank roll. 
4) You have roughly a 1/100 shot of playing a lifetime worth of $25 blackjack hands and actually coming out ahead. Not great odds, but better than I would have guessed. 

![alt text](output/oneplayer_onetable_150krounds_5kmoney1655298090.039737.png)

![alt text](output/one_player_one_table1655153761.20704.png)

Notice how the median player's money wicks down if they are close to zero. Can't recover once you are bankrupt. Bring enough money so that your loss rate stays low. 

Playing $25 hands, the loss rate is:
- Basic strategy:                     $0.155 per round
- Basic strategy, stand on hard 16:   $0.24 per round
- Basic strategy, never split:        $0.423 per round
- Basic strategy, hit on hard 16:     $0.417 per round
- Basic strategy, never double down:  $0.500 per round
