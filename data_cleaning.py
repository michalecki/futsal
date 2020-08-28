'''
scripts to clean and preprocess the data
'''

import re
import pandas as pd


def three_game_join(file):
    '''
    sums up the results of short games in case of three team session
    :param file: raw results file
    :return: clean file with teams and results
    '''
    test_file = open(file)
    test_result = open('scores.txt', 'w')
    flag = 0
    team_names = []
    games = {}
    for line in test_file:

        line = line.lower()

        if flag == 3:
            if line.startswith('team'):
                flag = 0
                # if not empty print results
                if games:
                    for score in games:
                        test_result.write(f'{score} {games[score][0]}-{games[score][1]}\n')
                # empty the results
                games = {}
            if line[0] in team_names:
                # finds numbers in the scores
                num = re.findall('[0-9]+', line)
                games[line[0:4]] = [games.get(line[0:4], [0, 0])[0] + int(num[0]),
                                    games.get(line[0:4], [0, 0])[1] + int(num[1])]




        # the line starts with one of the team labels
        elif line[0] in team_names:
            flag = 0
            test_result.write(line)

        # notices a team and counts how many team in a row
        if line.startswith('team'):
            flag += 1
            # reads the first character of the team name
            if line[5] not in team_names:
                team_names.append(line[5])
            test_result.write(line)

    test_file.close()
    test_result.close()


def make_array(file):
    '''
    reads in all the scores into a np array of 4 columns and number-of-games rows
    The columns are: [team1], [team2], score team1 (int), score team2 (int)
    :param file: cleaned scores file
    :return: np array
    '''
    scores_array = pd.DataFrame(columns=['Team1', 'Team2', 'T1 score', 'T2 score'])
    teams = {}

    with open(file) as sco:
        for line in sco:
            if line.startswith('team'):
                # splits the line in words and strips commas
                sp = [word.strip(',') for word in line.split()]
                teams[line[5]] = sp[2:]
            if line[0] in list(teams):
                team1 = teams[line[0]]
                if line[1] in list(teams):
                    team2 = teams[line[1]]
                elif line[2] in list(teams):
                    team2 = teams[line[2]]
                num = re.findall('[0-9]+', line)
                score1 = int(num[0])
                score2 = int(num[1])
                single_score = pd.DataFrame({'Team1': [team1], 'Team2': [team2],
                                             'T1 score': score1, 'T2 score': score2})

                scores_array = scores_array.append(single_score, ignore_index=True)


    return scores_array




# three_game_join('Wednesday Futsal scores raw.txt')
# print(make_array('scores.txt'))

