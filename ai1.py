#!/usr/bin/env python

import math

from antlib import *
import publicFunctions

myteam = 'L'
enemyteam = 'J'

def loop(game):
	if len(game.ants[enemyteam]) > 0:
		if groupHealth(game.ants[myteam]) <= groupHealth(game.ants[enemyteam]):
			collectFood(game.ants[myteam], game.food)
		else:
			attack(game.ants[myteam], game.ants[enemyteam])
	else:
		# No more enemy ants.
		if groupHealth(game.ants[myteam]) > game.queens[enemyteam].health:
			attack(game.ants[myteam], game.queens[enemyteam])
		else:
			collectFood(game.ants[myteam])

def attack(collection, collection2):
	pass

def collectFood(ants, foods):
	# TODO: avoid enemies while collecting food
	for ant in ants:
		closestFood = None
		for food in foods:
			if distance(ant, food) < distance(ant, closestFood):
				closestFood = food

		publicFunctions.moveAnt(ant, closestFood)

def distance(obj1, obj2):
	''' Returns Pythagorean distance. '''

	# Exception case: the distance from something to nothing is infinity. Any object is closer than no object.
	if obj1 == None or obj2 == None:
		return float('inf') # Always higher than any other value except itself

	dist = math.sqrt(abs(obj1.x - obj2.x) ** 2 + abs(obj1.y - obj2.y) ** 2)
	return dist

def groupHealth(ants):
	total = 0
	for ant in ants:
		total += ant.health
	
	return total

