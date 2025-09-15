import requests
import json
import pyperclip

with open('players.json', 'r') as f:
	playersDB = json.load(f)

rosterIDs = ['ianpeterson', 'LMiller', 'Roensb', 'DLokk', 'RainMan001', 'joshhancock92', 
'jsamp17', 'GluteSloot', 'brenlen', 'Seanzie', 'Fergilatr', 'Globo_Gym']

positionList = ['Total', 'All Offense', 'All Defense']

y2022League = 776558166568747008
y2023League = 917208843661271040
y2024League = 1048343675169927168
y2025League = 1181324955627573248

#numWeeks = 14 #Set this value if you want through a specific week, instead of where the real world is
numWeeks = requests.get('https://api.sleeper.app/v1/state/nfl').json()['display_week']

values = dict()
for a in range(1, 13):
	values[a] = {key: 0.0 for key in positionList}

def addValue(roster_id, position, value):
	values[roster_id][position] = round(value + values[roster_id][position], 2)


for x in range(1, numWeeks + 1):
	matchup = requests.get('https://api.sleeper.app/v1/league/1181324955627573248/matchups/' + str(x)).json()
	for val in matchup:
		user = val['roster_id']
		playerPoints = val['players_points']
		
		qbs, rbs, wrs, tes, dls, lbs, dbs = list(), list(), list(), list(), list(), list(), list()

		for playerPoint in sorted(playerPoints.items(), key=lambda x: x[1], reverse=True):
			player = playerPoint[0]
			if 'QB' in playersDB[player]['fantasy_positions']:
				qbs.append(player)
			if 'RB' in playersDB[player]['fantasy_positions']:
				rbs.append(player)
			if 'WR' in playersDB[player]['fantasy_positions']:
				wrs.append(player)
			if 'TE' in playersDB[player]['fantasy_positions']:
				tes.append(player)
			if 'DL' in playersDB[player]['fantasy_positions']:
				dls.append(player)
			if 'LB' in playersDB[player]['fantasy_positions']:
				lbs.append(player)
			if 'DB' in playersDB[player]['fantasy_positions']:
				dbs.append(player)
		
		rbPoints = playerPoints[rbs[0]] + playerPoints[rbs[1]]
		del rbs[1]
		del rbs[0]
		wrPoints = playerPoints[wrs[0]] + playerPoints[wrs[1]]
		del wrs[1]
		del wrs[0]

		qbPoints = playerPoints[qbs[0]]
		del qbs[0]
		tePoints = playerPoints[tes[0]]
		del tes[0]

		superFlex = qbs + rbs + wrs + tes 
		flex = rbs + wrs + tes 

		superFlex.sort(key=lambda x, playerPoints=playerPoints: playerPoints[x], reverse=True)
		flex.sort(key=lambda x, playerPoints=playerPoints: playerPoints[x], reverse=True)

		flexPoints = playerPoints[flex[0]] + playerPoints[flex[1]] + playerPoints[flex[2]]
		superFlex.remove(flex[0])
		superFlex.remove(flex[1])
		superFlex.remove(flex[2])
		superFlexPoints = playerPoints[superFlex[0]]

		offensivePoints = round(qbPoints + rbPoints + wrPoints + tePoints + superFlexPoints + flexPoints, 2)

		defenses = list(dict.fromkeys(dls + lbs + dbs))
		defenses.sort(key=lambda x, playerPoints=playerPoints: playerPoints[x], reverse=True)

		dlWin, lbWin, dbWin = list(), list(), list()

		for defender in defenses:
			if defender in dls and len(dlWin) <= 3:
				if len(dlWin) < 3:
					dlWin.append(defender)
				else:
					for dl in dlWin:
						if playersDB[dl]['fantasy_positions'] in lbWin and len(lbWin) < 3:
							lbWin.append(dl)
							dlWin.remove(dl)
							dlWin.append(defender)
							break
						if playersDB[dl]['fantasy_positions'] in dbWin and len(dbWin) < 3:
							dbWin.append(dl)
							dlWin.remove(dl)
							dlWin.append(defender)
							break

			if defender in lbs and len(lbWin) <= 3 and defender not in dlWin:
				if len(lbWin) < 3:
					lbWin.append(defender)
				else:
					for lb in lbWin:
						if playersDB[lb]['fantasy_positions'] in dlWin and len(dlWin) < 3:
							lbWin.append(lb)
							dlWin.remove(lb)
							lbWin.append(defender)
							break
						if playersDB[lb]['fantasy_positions'] in dbWin and len(dbWin) < 3:
							dbWin.append(lb)
							dlWin.remove(lb)
							lbWin.append(defender)
							break
			if defender in dbs and len(dbWin) <= 3 and defender not in dlWin and defender not in lbWin:
				if len(dbWin) < 3:
					dbWin.append(defender)
				else:
					for db in dbWin:
						if playersDB[db]['fantasy_positions'] in lbWin and len(lbWin) < 3:
							lbWin.append(db)
							dlWin.remove(db)
							dbWin.append(defender)
							break
						if playersDB[db]['fantasy_positions'] in dlWin and len(dlWin) < 3:
							dbWin.append(db)
							dlWin.remove(db)
							dbWin.append(defender)
							break
						
		dlPoints = round(sum(playerPoints[x] for x in dlWin), 2)
		lbPoints = round(sum(playerPoints[x] for x in lbWin), 2)
		dbPoints = round(sum(playerPoints[x] for x in dbWin), 2)
		for defender in defenses:
			if defender not in dlWin and defender not in lbWin and defender not in dbWin:
				dstFlexPoints = playerPoints[defender]
				break

		defensivePoints = round(dlPoints + lbPoints + dbPoints + dstFlexPoints, 2)

		totalPoints = round(offensivePoints + defensivePoints, 2)

		addValue(user, 'Total', totalPoints)
		addValue(user, 'All Offense', offensivePoints)
		addValue(user, 'All Defense', defensivePoints)

sortedValues = []
for pos in positionList:
	sortedValues.append([])

for z in range(len(positionList)):
	position = positionList[z]
	sortedPosition = sorted(values.items(), key=lambda x : x[1][position], reverse=True)
	for val in sortedPosition:
		player = rosterIDs[val[0] - 1]
		sortedValues[z].append(player + ", " + str(round(val[1][position] / numWeeks, 2)))

header = "Total, ,All Offense, ,All Defense"
res = '\n'.join("{},{},{}".format(a,b,c) for a,b,c in zip(*sortedValues))
pyperclip.copy(header + '\n' + res)
print('Values saved in clipboard for up to Week ' + str(numWeeks))