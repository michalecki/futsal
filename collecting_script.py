# calculates player and player couples goals scored - conceded based on collection of results


# TODO: clean and rewrite the code
# TODO: write with functions and/or OOP
# TODO: make a team selection tool


import re
#import json
import csv

#import defaultdict to handle easily lists as values in dictionary
#from collections import defaultdict

#open file
#test_file=open('test_file')
test_file=open('Wednesday Futsal scores raw.txt')
#read in the team into variable
#name(alphabetically sorted players)

#make a variable player name (name or label), goals scored, goals conceded

#make a variable player-player, goals scored, goals conceded

player_offensive=dict()
player_defensive=dict()

duo_offensive=dict()
duo_defensive=dict()

teams=dict()
teams_duo=dict()

#reads the file line by line:
#linenumber=0
for line in test_file:
#some little debugging
    #linenumber=linenumber+1
    #print(linenumber)
    
    #puts everything in a lowercase
    line=line.lower()
#notices a team and make a dict(label:list of players)
    if line.startswith('team') :
        #splits the line in words
        sp = line.split()
        #reads the first character of the team name
        a=line[5]
        
#makes a list of players, counting i gets rid of words "team" and the team name
        i=0
        players=list()
        for word in sp:
            word=word.strip(',')
            i=i+1
            if i>2 : players.append(word)
#sorts the list alphabetically
        players.sort()
#dictionary teams labeled with one word team name and list of players as a value
        teams[a]=players
#makes the duet list
        duos=list()
#loops through the players list        
        for i in range(len(players)):
            j=i+1
#makes the pairs first with remaining, second with remaining, etc            
            while j<len(players):
                
                duo=(players[i]+' '+players[j])
                duos.append(duo)
                j=j+1                
#saves the duos in a dictionary team label:list of duos                
        teams_duo[a]=duos
        
        
   
#the line starts with one of the team labels
    if line[0] in list(teams):
        #finds numbers in the scores
        num=re.findall('[0-9]+',line)
#loops through the players from the team mentioned first
        for player in teams[line[0]]:
            #adds goals scored
            player_offensive[player]=player_offensive.get(player,0)+int(num[0])
            #adds goals conceded
            player_defensive[player]=player_defensive.get(player,0)+int(num[1])
#loops through the players from the team mentioned in a second column 
        try:
            for player in teams[line[1]]:
                player_offensive[player]=player_offensive.get(player,0)+int(num[1])
                player_defensive[player]=player_defensive.get(player,0)+int(num[0])
#...or in the third column 
        except:
            for player in teams[line[2]]:
                player_offensive[player]=player_offensive.get(player,0)+int(num[1])
                player_defensive[player]=player_defensive.get(player,0)+int(num[0])
#duos
#loops through the duos from the team mentioned first
        for duo in teams_duo[line[0]]:
            #adds goals scored
            duo_offensive[duo]=duo_offensive.get(duo,0)+int(num[0])
            #adds goals conceded
            duo_defensive[duo]=duo_defensive.get(duo,0)+int(num[1])
#loops through the duos from the team mentioned in a second column 
        try:
            for duo in teams_duo[line[1]]:
                duo_offensive[duo]=duo_offensive.get(duo,0)+int(num[1])
                duo_defensive[duo]=duo_defensive.get(duo,0)+int(num[0])
#...or in the third column 
        except:
            for duo in teams_duo[line[2]]:
                duo_offensive[duo]=duo_offensive.get(duo,0)+int(num[1])
                duo_defensive[duo]=duo_defensive.get(duo,0)+int(num[0])



#with open('results','w') as f:
    #f.write('player_offensive\n')
    #json.dump(player_offensive,f)
    #f.write('\nplayer_defensive\n')
    #json.dump(player_defensive,f)
    #f.write('\nduo_offensive\n')
    #json.dump(duo_offensive,f)
    #f.write('\nduo_defensive\n')
    #json.dump(duo_defensive,f)


with open('results_players.csv','w') as f:
    fieldnames = ['name','scored','conceded']
    writer=csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for name in list(player_offensive):
        writer.writerow({'name': name, 'scored': player_offensive[name], 'conceded': player_defensive[name]})

with open('results_duos.csv','w') as f:
    fieldnames = ['name','scored','conceded']
    writer=csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for name in list(duo_offensive):
        writer.writerow({'name': name, 'scored': duo_offensive[name], 'conceded': duo_defensive[name]})

#add the parameter scor/conc
#another script to calculate parameters for a given team

#challenges:
    #make it object-oriented
    #make it with sql

