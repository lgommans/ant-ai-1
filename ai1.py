#!/usr/bin/env python

# TODO: avoid enemies while collecting food

import math

from antlib import *
import publicFunctions

myteam = 'L'
enemyteam = 'J'

def loop(game):
	if len(game.ants[enemyteam]) > 0:
		if groupHealth(game.ants[myteam]) <= groupHealth(game.ants[enemyteam]):
			goto(game, game.ants[myteam], game.food)
		else:
			goto(game, game.ants[myteam], game.ants[enemyteam])
	else:
		# No more enemy ants.
		if groupHealth(game.ants[myteam]) > game.queens[enemyteam].health:
			goto(game, game.ants[myteam], [game.queens[enemyteam]])
		else:
			goto(game, game.ants[myteam], game.food)

def goto(game, ants, objects):
	for ant in ants:
		closestObject = None
		for obj in objects:
			if distance(ant, obj) < distance(ant, closestObject):
				closestObject = obj

		publicFunctions.moveAnt(ant, closestObject)

def groupHealth(ants):
	total = 0
	for ant in ants:
		total += ant.health
	
	return total

