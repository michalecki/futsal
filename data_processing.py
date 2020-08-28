'''
scripts to analyze the data
'''

import pandas as pd
import itertools


def player_performance(dat_fram):
    '''
    goes through the results and collects goals scored and conceded by the teams
    with a player on the teamsheet
    :param dat_fram: team, team, score, score
    :return: data frame: player (index), scored, conceded
    '''

    sc_dict = {}
    con_dict = {}

    for game in range(len(dat_fram)):


        for player in dat_fram['Team1'][game]:
            sc_dict[player] = sc_dict.get(player, 0) + dat_fram['T1 score'][game]
            con_dict[player] = con_dict.get(player, 0) + dat_fram['T2 score'][game]

        for player in dat_fram['Team2'][game]:
            sc_dict[player] = sc_dict.get(player, 0) + dat_fram['T2 score'][game]
            con_dict[player] = con_dict.get(player, 0) + dat_fram['T1 score'][game]



    scored_df = pd.DataFrame.from_dict(sc_dict, orient='index', columns=['scored'])
    conc_df = pd.DataFrame.from_dict(con_dict, orient='index', columns=['conceded'])

    player_scores = scored_df.join(conc_df)
    # player_scores['player'] = player_scores.index

    return player_scores

def make_pair_list(team):
    '''
    makes a list of the player pairs
    :param team: list of players
    :return: list of player pairs
    '''
    pairs = []

    team.sort()

    # making the pairs list
    for i in range(len(team)):
        j = i + 1
        # makes the pairs first with remaining, second with remaining, etc            
        while j < len(team):
            duo = (team[i] + ' ' + team[j])
            pairs.append(duo)
            j = j + 1
            
    return pairs
            
def pair_performance(dat_fram):
    '''
    goes through the results and collects goals scored and conceded by the teams
    with a player pair on the teamsheet
    :param dat_fram: team, team, score, score
    :return: data frame: player pair (index), scored, conceded
    '''
    sc_dict = {}
    con_dict = {}

    for game in range(len(dat_fram)):
        pairs1 = make_pair_list(dat_fram['Team1'][game])
        pairs2 = make_pair_list(dat_fram['Team2'][game])


        for pair in pairs1:

                sc_dict[pair] = sc_dict.get(pair, 0) + dat_fram['T1 score'][game]
                con_dict[pair] = con_dict.get(pair, 0) + dat_fram['T2 score'][game]


        for pair in pairs2:
            sc_dict[pair] = sc_dict.get(pair, 0) + dat_fram['T2 score'][game]
            con_dict[pair] = con_dict.get(pair, 0) + dat_fram['T1 score'][game]



    scored_df = pd.DataFrame.from_dict(sc_dict, orient='index', columns=['scored'])
    conc_df = pd.DataFrame.from_dict(con_dict, orient='index', columns=['conceded'])

    pair_scores = scored_df.join(conc_df)


    return pair_scores

def calculate_ratio(team_data):
    '''
    helper function to add the scored/conceded ratio column
    :param team_data: dataframe
    :return: dataframe with a column added
    '''
    team_data['s/c ratio'] = team_data['scored'] / team_data['conceded']
    return team_data


def team_strength(team, players, pairs, option='avg_all'):
    '''
    Calculates the team strength. Parameter option defines the base of the estimation.
    Output value is higher for stronger team.
    :param team: list of players
    :param players: dataframe, player scored-conceded data
    :param pairs: dataframe, pair scored-conceded data
    :param option:
    avg_all = average of scored/conceded ratio of players and pairs in the team
    avg_pla = average of scored/conceded ratio of players in the team
    avg_pai = average of scored/conceded ratio of pairs in the team
    sum_all = ratio of scored/conceded summed for all players and pairs in the team
    sum_pla = ratio of scored/conceded summed for all players in the team
    sum_pai = ratio of scored/conceded summed for all pairs in the team
    :return: float, team strength
    '''
    #sorting the names to avoid double pairs
    team.sort()
    #retreiving the players from the database
    # team_players = players.loc[players.index.intersection(team), :]
    team_players = players.loc[team]
    #retreiving the pairs from the database
    # team_pairs = pairs.loc[pairs.index.intersection(make_pair_list(team)), :]
    team_pairs = pairs.loc[make_pair_list(team)]
    # print(players.loc[team])
    # print(players)


    if option == 'avg_all':
        calculate_ratio(team_players)
        calculate_ratio(team_pairs)
        ratio_sum = team_players['s/c ratio'].sum() + team_pairs['s/c ratio'].sum()
        ratio_len = len(team_players) + len(team_pairs)
        return ratio_sum / ratio_len

    elif option == 'avg_pla':
        calculate_ratio(team_players)
        return team_players['s/c ratio'].mean()

    elif option == 'avg_pai':
        calculate_ratio(team_pairs)
        return team_pairs['s/c ratio'].mean()

    elif option == 'sum_all':
        all_goals = team_players.sum() + team_pairs.sum()
        return all_goals['scored'] /all_goals['conceded']

    elif option == 'sum_pla':
        all_goals = team_players.sum()
        return all_goals['scored'] /all_goals['conceded']

    elif option == 'sum_pai':
        all_goals = team_pairs.sum()
        return all_goals['scored'] /all_goals['conceded']

    else:
        print('Wrong parameter')


def predict_results_test(data_fram, players, pairs, draw_margin, option_list):
    '''
    A function to calculate the team coefficients using different methods and compare the
    scores predictions with the results in the training data.
    Saves the expanded dataframe to "data_fram_predictions.csv" file.
    :param data_fram: team lineups and scores
    :param players: player scored-conceded data
    :param pairs: pair scored-conceded data
    :param draw_margin: float, good guess is below 0.05
    :param option_list: list of the options to calculate the team strength
    :return: dictionary with the number of correct predictions per method
    '''

    for option in option_list:
        data_fram[f'team1_{option}'] = [team_strength(data_fram['Team1'][i], players, pairs, option)
                                     for i in range(len(data_fram))]
        data_fram[f'team2_{option}'] = [team_strength(data_fram['Team2'][i], players, pairs, option)
                                     for i in range(len(data_fram))]
        data_fram[f'result_{option}'] = [1 if data_fram[f'team1_{option}'][i] > data_fram[f'team2_{option}'][i]
                                      else 0 if abs(data_fram[f'team1_{option}'][i]
                                                    - data_fram[f'team2_{option}'][i]) < draw_margin
        else 2 for i in range(len(data_fram))]

    data_fram['result'] = [0 if data_fram['T1 score'][i] == data_fram['T2 score'][i]
                        else 2 if data_fram['T1 score'][i] < data_fram['T2 score'][i]
                        else 1 for i in range(len(data_fram))]

    tr_err = {}
    for option in option_list:
        for i in range(len(data_fram)):
            if data_fram['result'][i] == data_fram[f'result_{option}'][i]:
                test = 1
            else:
                test = 0
            tr_err[option] = tr_err.get(option, 0) + test

    # data_fram.to_csv('data_fram_predictions.csv')

    return tr_err


def find_draw_margin(data_fram, players, pairs, option_list):
    '''
    Finds the optimal draw margin for all the parametrization methods
    :param data_fram: team lineups and scores
    :param players: player scored-conceded data
    :param pairs: pair scored-conceded data
    :return: dataframe, with margin and number of correct predictions
    '''
    errors = pd.DataFrame()

    draw_margin_range = [x / 1000 for x in range(0, 30)]
    for draw_margin in draw_margin_range:
        err = predict_results_test(data_fram, players, pairs, draw_margin, option_list)
        err['margin'] = draw_margin
        errors = errors.append(err, ignore_index=True)

    print(errors)

    return errors

def k_fold_draw_margin(data_fram, option_list):
    '''
    Makes the k-fold verification over the whole data from data_frame
    Returns the amount of correct prediction for different draw margins.
    :param data_fram: input data
    :param option_list: the list of the options to calculate team strength
    :return:
    '''
    for draw_margin in range(10):
        sum_pred = {}
        for i in range(len(data_fram)):
            # k_ind = random.randrange(0, len(scores))
            k_ind = i
            k_row = pd.DataFrame(data_fram.iloc[k_ind])
            k_row = k_row.T.reset_index()
            scores_k = data_fram.drop(k_ind)
            scores_k = scores_k.reset_index()
            player_scores = player_performance(scores_k)
            pair_scores = pair_performance(scores_k)

            pred = predict_results_test(k_row, player_scores, pair_scores, draw_margin / 100, option_list)

            for option in option_list:
                sum_pred[option] = sum_pred.get(option, 0) + pred[option]
        print('Draw margin: ', draw_margin / 100)
        print(sum_pred)


def choose_teams(pool, players, pairs, option='avg_pla'):
    '''
    lists 3 most even teams that can be made from the pool of players
    :param pool: list
    :param players: data frame from player_performance function
    :param pairs: data frame from pair_performance function
    :param option: team strength calculation method
    :return:
    '''
    lineups = pd.DataFrame(columns=['Team1', 'Team2', 'T1_value', 'T2_value', 'diff'])
    for i in range(len(pool)):
        pool[i] = pool[i].lower()
    pool.sort()
    teams = []
    #pick teams
    for team in itertools.combinations(pool, 5):
        t1 = list(team)
        t2 = [name for name in pool if name not in t1]
        if True:
            t1_v = team_strength(t1, players, pairs)
            t2_v = team_strength(t2, players, pairs)
            single_line = pd.DataFrame({'Team1': [t1], 'Team2': [t2],
                                         'T1_value': t1_v, 'T2_value': t2_v, 'diff': t1_v-t2_v})

            lineups = lineups.append(single_line, ignore_index=True)

    return lineups

def make_prediction(team1, team2, players, pairs):
    '''
    prints out predictions for chosen teams
    :param team1: list of players
    :param team2: list of players
    :param players: player params
    :param pairs: pair params
    :return: print out with the predictions
    '''
    #cleans the team input
    team1 = team1.lower()
    t1 = team1.split(', ')
    team2 = team2.lower()
    t2 = team2.split(', ')

#<<<['avg_all', 'avg_pla', 'avg_pai', 'sum_all', 'sum_pla', 'sum_pai']
    option_list = ['avg_all', 'avg_pla', 'avg_pai', 'sum_all', 'sum_pla', 'sum_pai']
    #calculate the favourites according to different metrics
    for option in option_list:
        t1r = team_strength(t1, players, pairs, option)
        t2r = team_strength(t2, players, pairs, option)
        print(f'Calculation method: {option}')
        print(f'Team1:Team2 {t1r:.3f}:{t2r:.3f}\n')


