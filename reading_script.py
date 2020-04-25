# takes data from the files crated by collecting script
# calculates and prints values for teams from the "teams" file


import csv
import statistics


team1=list()
team2=list()
team3=list()

team1scored=0
team1conceded=0

team2scored=0
team2conceded=0

team3scored=0
team3conceded=0

duos1=list()
duos2=list()
duos3=list()

duos1scored=0
duos1conceded=0

duos2scored=0
duos2conceded=0

duos3scored=0
duos3conceded=0

team1_avg_factor=list()
team2_avg_factor=list()
team3_avg_factor=list()

with open('teams') as teams_file:
    for line in teams_file:
        line=line.lower()
        players_split=line.split()
        players=[]
        for player in players_split:
            player=player.strip(',')
            players.append(player)
        players.sort()
        if not team1: 
            team1=players
        elif not team2: 
            team2=players
        else:
            team3=players
            
        duos=[]
        i=0
        for i in range(len(players)):
            j=i+1
            while j<len(players):
                duo=(players[i]+' '+players[j])
                duos.append(duo)
                j=j+1  
#this is a check if the list is empty
#if empty, then write into it
        if not duos1:
            duos1=duos
        elif not duos2:
            duos2=duos
        else:
            duos3=duos


with open('results_players.csv') as rp:
    read_rp = csv.DictReader(rp)
    for row in read_rp:
        if row['name'] in team1:
            team1scored=team1scored+int(row['scored'])
            team1conceded=team1conceded+int(row['conceded'])
            team1_avg_factor.append(int(row['scored'])/int(row['conceded']))
        if row['name'] in team2:
            team2scored=team2scored+int(row['scored'])
            team2conceded=team2conceded+int(row['conceded'])
            team2_avg_factor.append(int(row['scored'])/int(row['conceded']))
        if row['name'] in team3:
            team3scored=team3scored+int(row['scored'])
            team3conceded=team3conceded+int(row['conceded'])
            team3_avg_factor.append(int(row['scored'])/int(row['conceded']))
            
with open('results_duos.csv') as rp:
    read_rp = csv.DictReader(rp)
    for row in read_rp:
        if row['name'] in duos1:
            duos1scored=duos1scored+int(row['scored'])
            duos1conceded=duos1conceded+int(row['conceded'])
            team1_avg_factor.append(int(row['scored'])/int(row['conceded']))
        if row['name'] in duos2:
            duos2scored=duos2scored+int(row['scored'])
            duos2conceded=duos2conceded+int(row['conceded'])
            team2_avg_factor.append(int(row['scored'])/int(row['conceded']))
        if row['name'] in duos3:
            duos3scored=duos3scored+int(row['scored'])
            duos3conceded=duos3conceded+int(row['conceded'])
            team3_avg_factor.append(int(row['scored'])/int(row['conceded']))

            
team1_factor=team1scored/team1conceded
team2_factor=team2scored/team2conceded
if team3conceded != 0:
    team3_factor=team3scored/team3conceded

            
duos1_factor=duos1scored/duos1conceded
duos2_factor=duos2scored/duos2conceded
if duos3conceded != 0:
    duos3_factor=duos3scored/duos3conceded

superfactor1=(team1scored+duos1scored)/(team1conceded+duos1conceded)
superfactor2=(team2scored+duos2scored)/(team2conceded+duos2conceded)
if duos3conceded != 0:
    superfactor3=(team3scored+duos3scored)/(team3conceded+duos3conceded)

print('team1\n',team1,'\n',team1_factor)
print('duos1\n',duos1_factor)
print('total: ',superfactor1)
print('team2\n',team2,'\n',team2_factor)
print('duos2\n',duos2_factor)
print('total: ',superfactor2)
if team3conceded != 0:
    print('team3\n',team3,'\n',team3_factor)
    print('duos3\n',duos3_factor)
    print('total: ',superfactor3)
    
print('total goals scored, conceded')
    
print(team1scored+duos1scored,team1conceded+duos1conceded)
print(team2scored+duos2scored,team2conceded+duos2conceded)
if team3conceded != 0:
    print(team3scored+duos3scored,team3conceded+duos3conceded)
    
print('average of individual and duo factors')

print('team 1', statistics.mean(team1_avg_factor))
print('team 2', statistics.mean(team2_avg_factor))
if team3conceded != 0:
    print('team 3', statistics.mean(team3_avg_factor))


