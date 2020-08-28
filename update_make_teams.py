import data_cleaning
import data_processing



data_cleaning.three_game_join('Futsal scores raw.txt')
data_table = data_cleaning.make_array('scores.txt')
players = data_processing.player_performance(data_table)
pairs = data_processing.pair_performance(data_table)

players_pool = []

data_processing.choose_teams(players_pool, players, pairs).to_csv('teams.csv')

#to compare two teams
# BLUE = []
# RED = []
#
# data_processing.make_prediction(RED, BLUE, players, pairs)
