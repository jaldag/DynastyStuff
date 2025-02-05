import requests
import json
import pyperclip

rosterIDs = ['ianpeterson', 'LMiller', 'Roensb', 'DLokk', 'RainMan001', 'joshhancock92', 
'jsamp17', 'GluteSloot', 'brenlen', 'Seanzie', 'Fergilatr', 'Globo_Gym']

positionList = ['Total', 'All Offense', 'All Defense', 'QB+Flex', 'RB', 'WR', 'TE', 'WRT', 'IDP', 'DL', 'LB', 'DB']

y2022League = 776558166568747008
y2023League = 917208843661271040
y2024League = 1048343675169927168
y2025League = 1181324955627573248

leagues = [str(y2022League), str(y2023League), str(y2024League), str(y2025League)]
matrix = [[0 for x in range(13)] for x in range(13)]

for league in leagues:
	for numWeek in range(1, 20):
		transactions = requests.get('https://api.sleeper.app/v1/league/' + league + '/transactions/' + str(numWeek)).json()
		for val in transactions:
			if len(val['roster_ids']) > 1:
				matrix[val['roster_ids'][0]][val['roster_ids'][1]] = matrix[val['roster_ids'][0]][val['roster_ids'][1]] + 1
				matrix[val['roster_ids'][1]][val['roster_ids'][0]] = matrix[val['roster_ids'][1]][val['roster_ids'][0]] + 1
matrix.pop(0)
for x in range(len(matrix)):
	matrix[x].pop(0)
matrix.insert(0, rosterIDs)

header = "," + ','.join(rosterIDs)
res = '\n'.join("{},{},{},{},{},{},{},{},{},{},{},{},{}".format(a,b,c,d,e,f,g,h,i,j,k,l,m) for a,b,c,d,e,f,g,h,i,j,k,l,m in zip(*matrix))
pyperclip.copy(header + '\n' + res)
print('Values saved in clipboard')