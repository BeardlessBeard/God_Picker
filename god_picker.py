#!/usr/bin/env python3

import sys
import random
from pprint import pprint
import requests
import json
from bs4 import BeautifulSoup

class GodsMap:
    def __init__(self):
        self.find = {}
        return

    def addGod(self, god):
        self.find.update({god.id:god})
        return

class God:
    def __init__(self, ID, Role, Name):
        self.id = ID
        self.role = Role
        self.name = Name
        self.kills = 0
        self.deaths = 0
        self.assists = 0
        self.wins = 0
        self.losses = 0
        self.score = 0
        return
    def setKills(self, Kills):
        self.kills += Kills
        return
    def setDeaths(self, Deaths):
        self.deaths += Deaths
        return
    def setAssists(self, Assists):
        self.assists += Assists
        return
    def setWins(self, Wins):
        self.wins += Wins
        return
    def setLosses(self, Losses):
        self.losses += Losses
        return
    def setKDA(self, KDA):
        self.kda = KDA
        return

def main():

    if(len(sys.argv) != 3):
        raise Exception('Usage: console(pc/xb/ps4) username')

    if(sys.argv[1] != 'pc' and sys.argv[2] != 'xb' and sys.argv[2] != 'pc'):
        raise Exception('pc/xb/ps4 specified incorrectly')

    quote_page = 'http://smite.guru/profile/'+sys.argv[1]+'/'+sys.argv[2]+'/gods'

    page = requests.get(quote_page)
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find('div', class_='container flex-container')

#Commented code used to find god id numbers (antiquated)
    #god_data = str(data)
    #god_data = god_data[61:12482]

    #god_data = god_data.split('&quot;')
    #god_data = list(filter(lambda a: a != '{', god_data))
    #god_data = list(filter(lambda a: a != ':', god_data))
    #god_data = list(filter(lambda a: a != ',', god_data))
    #god_data = list(filter(lambda a: a != 'slug_id', god_data))
    #god_data = list(filter(lambda a: a != 'class', god_data))
    #god_data = list(filter(lambda a: a != 'name', god_data))
    ##god_data = list(filter(lambda a: a != ':{', god_data))
    #god_data = list(filter(lambda a: a != '},', god_data))
    #god_data = list(filter(lambda a: a != '}}', god_data))

    #for i in range(0,len(god_data)):
        #if(god_data[i] == ':{'):
            #name = god_data[i+3]
            #role = god_data[i+2]
            #id = god_data[i-1]
            #god = God(name, role, id)
            #godsArray.append(god)

    #for i in godsArray:
        #print(i.id+' '+i.role+' '+i.name)

    gods = GodsMap()
    idArray = []
    god_id = open("god_id", 'r')

    while 1:
        line = god_id.readline()
        if not line:
            break
        line = line.split()
        id = line[0]
        role = line[1]
        name = line[2]
        for i in range(3, len(line)):
            name += ' '+line[i]
        god = God(id, role, name)
        gods.addGod(god)
        idArray.append(id)

    match_data = str(data.find('div', class_='widget-content table-responsive'))
    match_data = match_data[71:-27]
    match_data = json.loads(match_data)
    #match_data = json.load(open('stats.json'))
    for m in match_data:
        id = m['god']
        kills = m['kills']
        deaths = m['deaths']
        assists = m['assists']
        losses = m['losses']
        wins = m['wins']
        god = gods.find[str(id)]
        god.setKills(kills)
        god.setDeaths(deaths)
        god.setLosses(losses)
        god.setWins(wins)
        god.setAssists(assists)

    assassins = []
    warriors = []
    guardians =  []
    mages = []
    hunters = []

    for id in idArray:
        god = gods.find[str(id)]
        gp = god.wins + god.losses
        if(gp == 0):
            continue
        if(gp > 100):
            WLscore = god.wins*(god.wins/gp)/((gp-100)*0.25)
        else:
            WLscore = god.wins*god.wins/gp
        if(god.deaths == 0):
            continue
        if(god.role == "Assassin"):
            kda = (god.kills*1.5+god.assists*0.5)/god.deaths
            god.setKDA(kda)
            god.score = WLscore + god.kda * 10
            for i in range(0, int(god.score)):
                assassins.append(god)
        elif(god.role == "Warrior"):
            kda = (god.kills*1.25+god.assists*0.75)/god.deaths
            god.setKDA(kda)
            god.score = WLscore + god.kda * 10
            for i in range(0, int(god.score)):
                warriors.append(god)
        elif(god.role == "Mage"):
            kda = (god.kills*1.5+god.assists*0.5)/god.deaths
            god.setKDA(kda)
            god.score = WLscore + god.kda * 10
            for i in range(0, int(god.score)):
                mages.append(god)
        elif(god.role == "Hunter"):
            kda = (god.kills*1.5+god.assists*0.5)/god.deaths
            god.setKDA(kda)
            god.score = WLscore + god.kda * 10
            for i in range(0, int(god.score)):
                hunters.append(god)
        elif(god.role == "Guardian"):
            kda = (god.kills+god.assists)/god.deaths
            god.setKDA(kda)
            god.score = WLscore + god.kda * 10
            for i in range(0, int(god.score)):
                guardians.append(god)
        else:
            print("role not recognized")
            continue

    while 1:
        roles = input("Enter class(es) or enter 'exit': ")
        roles = roles.split()
        tmp = []
        skip = 0
        for r in roles:
            if(r == "Guardian" or r == 'guardian' or r == 'g' or r == 'G'):
                tmp += guardians
            elif(r == "Mage" or r == 'mage' or r == 'm' or r == 'M'):
                tmp += mages
            elif(r == "Hunter" or r == 'hunter' or r == 'h' or r == 'H'):
                tmp += hunters
            elif(r == "Warrior" or r == 'warrior' or r == 'w' or r == 'W'):
                tmp += warriors
            elif(r == "Assassin" or r == 'assassin' or r == 'a' or r == 'A'):
                tmp += assassins
            elif(r == 'exit'):
                exit()
            else:
                print("\nRole %s not recognized\n" % r)
                print("Roles are:\nAssassin\nGuardian\nHunter\nMage\nWarrior\n")
                skip = 1
                break
        if(skip == 1):
            continue
        index = random.randint(0, len(tmp))
        god = tmp[index]
        print("\nGod Name:     %15s" % god.name)
        print("Class:        %15s\n" % god.role)
        print("Wins:         %15d" % god.wins)
        print("Losses:       %15d" % god.losses)
        print("Win Percent:  %15.2f" % (god.wins/(god.wins+god.losses)))
        print("Kills:        %15d" % god.kills)
        print("Deaths:       %15d" % god.deaths)
        print("Assists:      %15d" % god.assists)
        print("Weighted KDA: %15.2f" % god.kda)
        print("Score:        %15.2f" % god.score)
        print("Pick chance:  %15.2f\n" % (god.score/len(tmp)*100))
        print('Note: weighted KDA and score are different for each class\n')

if __name__ == "__main__":
    exit(main())
