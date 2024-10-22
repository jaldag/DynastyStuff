import requests
import json
import pyperclip

rosterIDs = ['ianpeterson', 'LMiller', 'Roensb', 'DLokk', 'RainMan001', 'joshhancock92', 
'jsamp17', 'GluteSloot', 'brenlen', 'Seanzie', 'Fergilatr', 'Globo_Gym']

positionList = ['Total', 'All Offense', 'All Defense', 'QB+Flex', 'RB', 'WR', 'TE', 'WRT', 'IDP', 'DL', 'LB', 'DB']

y2022League = 776558166568747008
y2023League = 917208843661271040
y2024League = 1048343675169927168

#numWeeks = 14 #Set this value if you want through a specific week, instead of where the real world is
numWeeks = requests.get('https://api.sleeper.app/v1/state/nfl').json()['display_week']

values = dict()
for a in range(1, 13):
	values[a] = {key: 0.0 for key in positionList}

def addValue(roster_id, position, value):
	values[roster_id][position] = round(value + values[roster_id][position], 2)

for x in range(1, numWeeks + 1):
	matchup = requests.get('https://api.sleeper.app/v1/league/1048343675169927168/matchups/' + str(x)).json()
	for val in matchup:
		scores = val['starters_points']
		user = val['roster_id']
		addValue(user, 'QB+Flex', scores[0])
		addValue(user, 'RB', scores[1])
		addValue(user, 'RB', scores[2])
		addValue(user, 'WR', scores[3])
		addValue(user, 'WR', scores[4])
		addValue(user, 'TE', scores[5])
		addValue(user, 'WRT', scores[6])
		addValue(user, 'WRT', scores[7])
		addValue(user, 'WRT', scores[8])
		addValue(user, 'QB+Flex', scores[9])
		addValue(user, 'IDP', scores[10])
		addValue(user, 'DL', scores[11])
		addValue(user, 'DL', scores[12])
		addValue(user, 'DL', scores[13])
		addValue(user, 'LB', scores[14])
		addValue(user, 'LB', scores[15])
		addValue(user, 'LB', scores[16])
		addValue(user, 'DB', scores[17])
		addValue(user, 'DB', scores[18])
		addValue(user, 'DB', scores[19])
		for y in range(0, 20) :
			addValue(user, 'Total', scores[y])
		for y in range(0, 10) :
			addValue(user, 'All Offense', scores[y])
		for y in range(10, 20) :
			addValue(user, 'All Defense', scores[y])

sortedValues = []
for pos in positionList:
	sortedValues.append([])

for z in range(len(positionList)):
	position = positionList[z]
	sortedPosition = sorted(values.items(), key=lambda x : x[1][position], reverse=True)
	for val in sortedPosition:
		player = rosterIDs[val[0] - 1]
		sortedValues[z].append(player + ", " + str(round(val[1][position] / numWeeks, 2)))

header = "Total, ,All Offense, ,All Defense, , ,QB+Flex, ,RB, ,WR, ,TE, ,WRT, ,IDP, ,DL, ,LB, ,DB, "
res = '\n'.join("{},{},{}, ,{},{},{},{},{},{},{},{},{}".format(a,b,c,d,e,f,g,h,i,j,k,l) for a,b,c,d,e,f,g,h,i,j,k,l in zip(*sortedValues))
pyperclip.copy(header + '\n' + res)
print('Values saved in clipboard for up to Week ' + str(numWeeks))