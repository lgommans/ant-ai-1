#!/usr/bin/env python3

# TODO: use curses? Or pygame?
# TODO: change AI loading method (see ai1-*.py)

import sys, math
from time import sleep
from random import randrange as rand
from colorama import Fore as fgcol, Back as bgcol, Style as charbrightness

from antlib import *
from publicFunctions import *
from external import NonBlockingConsole

from ai1refactored import AI as AI1
from ai5 import loop as ailoop

def color(team = None):
	# NOTE: to get colors, remove the return line below
	return ''
	if team == None:
		return bgcol.RESET
	elif team == 'none':
		return bgcol.GREEN
	elif team == 'J':
		return bgcol.RED
	elif team == 'L':
		return bgcol.YELLOW

def read_grid(filename):
	execfile("gridObjects-" + filename + ".py")

def cls():
	# Not exactly cls ('clear screen'), but it's enough
	sys.stdout.write("\n" * 6)

def displayStats():
	global enabled

	if enabled['antCount']:
		displayStat("Ant count", len(game.ants['L']), len(game.ants['J']))

	if enabled['antHealth']:
		displayStat("Ants health", game.antHealth('L'), game.antHealth('J'))

	if enabled['queenHealth']:
		displayStat("Queen health", game.queens['L'].health, game.queens['J'].health)

	sys.stdout.write(color() + "\n")

def displayStat(title, statL, statJ):
	if statJ != 0:
		n = round(statL / statJ * 100)
		perc = ''
		if n > 101:
			perc = color('L')
		if n < 99:
			perc = color('J')
		perc += str(n) + "%" + color()
	else:
		perc = 'INF'
	sys.stdout.write(color() + title + " " + color('L') + "L: " + str(round(statL)) + color() + "; " + color('J') + "J: " + str(round(statJ)) + color() + " (L/J=" + perc + "). \t")

def displayGrid():
	outstr = ''
	emptyTile = color() + ' - '
	grid = [[ emptyTile for y in range(game.gridheight)] for x in range(game.gridwidth)]

	for obj in game.allObjects():
		text = ''
		if hasattr(obj, 'team'):
			if obj.team == 'J':
				text = color('J')
			else:
				text = color('L')
		else:
			text = color('none')
		
		text += obj.displayAs
		if grid[obj.position[0]][obj.position[1]] != emptyTile:
			text = text.replace(' ', '+')
		grid[obj.position[0]][obj.position[1]] = text + color()

	for x in grid:
		for y in x:
			outstr += str(y)
		outstr += "\n"
	
	print(outstr)

def spawn_food():
	i = 0
	while True:
		i += 1
		if i > 9000:
			print("WARN: No free space for food?")
			break

		x = rand(0, game.gridwidth)
		y = rand(0, game.gridheight)

		if occupied(game.allObjects(), (x, y)):
			continue

		game.food.append(Food(game, (x, y)))
		break

def gameMaintenance():
	game.time += 1

	removeFood = []
	removeAnt = []

	for antteam in game.ants:
		for ant in game.ants[antteam]:
			if ant.health <= 0:
				if ant not in removeAnt:
					removeAnt.append(ant)
				continue
			for antteam2 in game.ants:
				if antteam2 != antteam:
					for enemyant in game.ants[antteam2]:
						if enemyant.position == ant.position:
							# Enemyant and ant are are the same position!
							enemyanthealth = enemyant.health

							# Prevent them from using their health twice
							if ant.lastAttack != game.time and ant.health >= 0:
								enemyant.health -= math.sqrt(ant.health) * slowdeath
							if enemyant.lastAttack != game.time and enemyanthealth >= 0:
								ant.health -= math.sqrt(enemyanthealth) * slowdeath

							enemyant.lastAttack = game.time
							ant.lastAttack = game.time

							if ant.health <= 0 and ant not in removeAnt:
								removeAnt.append(ant)
							if enemyant.health <= 0 and enemyant not in removeAnt:
								removeAnt.append(enemyant)

			for queenteam in game.queens:
				if ant.position == game.queens[queenteam].position and queenteam != ant.team:
					# ant is at the same location as this enemy queen!
					game.queens[queenteam].health -= ant.health
					if ant not in removeAnt:
						removeAnt.append(ant)

					if game.queens[queenteam].health <= 0:
						print("Team " + queenteam + " lost!")
						sys.exit(0)

			# If two ants reach a food at the same time, a random one gets it
			for food in game.food:
				if ant.position == food.position and food.amount > 0:
					ant.health += food.amount * (1 - Queen.foodTax)
					ant.health = min(ant.health, ant.originalHealth)
					game.queens[ant.team].health += food.amount * Queen.foodTax
					game.queens[ant.team].health = min(game.queens[ant.team].health, Queen.originalHealth)
					Ant(game, ant.team)
					food.amount = 0
					removeFood.append(food)

	for ant in removeAnt:
		game.ants[ant.team].remove(ant)

	for food in removeFood:
		game.food.remove(food)
	
	if len(game.ants['J']) == 0 and len(game.ants['L']) == 0:
		print("There are no winners in this game.")
		sys.exit(0)

def inputHandling():
	global framedelay, drawevery

	# NonBlockingConsole gets keystrokes from the console. It's a bit whacky, but the best I've been able to find without writing something elaborate or multi-threaded myself.
	# Users need to hit enter after typing a character, but it's good enough for now.
	nbc = NonBlockingConsole()
	char = nbc.get_data()
	if char != False:
		if char == 'q':
			sys.exit(0)
		elif char == '+':
			framedelay /= 1.2
		elif char == '-':
			framedelay *= 1.2
		elif char == '=':
			drawevery *= 1.5
		elif char == '_':
			drawevery /= 1.5

# Initialization
slowdeath = 3 # When ants attack each other, they lose (sqrt(enemyant.health)*slowdeath)
framedelay = 0.1
drawevery = 1
enabled = { 'antHealth': True, 'queenHealth': True, 'antCount': True }

game = Game((51, 51))

queenpos = (0, 0)
game.queens['L'] = Queen(game, queenpos, 'L')
Ant(game, 'L')

queenpos = game.gridwidth - 1, game.gridheight - 1
game.queens['J'] = Queen(game, queenpos, 'J')
Ant(game, 'J')

ai1 = AI1(myteam='L', enemyteams=['J'])

for i in range(0, 10):
	spawn_food()

# Main loop
while True:
	for i in range(0, 2):
		spawn_food()
	gameMaintenance()
	inputHandling()
	ai1.loop(game)
	ailoop(game)
	if game.time % math.ceil(drawevery) == 0:
		cls()
		displayStats()
		displayGrid()
	sleep(framedelay) 

