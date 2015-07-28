#!/usr/bin/env python

# RandomTaskAI
# TODO: Mark food as "I'm going there" so ants go for separate foods. (Basic version working.)
# TODO: Dynamic task assignment?
# TODO: (Dynamic) task switching?

import math, random

from antlib import *
import publicFunctions

myteam = 'L'
enemyteam = 'J'

class Tasks:
	GetFood = 1
	AttackQueen = 2
	AttackAnts = 3

anttasks = []
occupiedFood = []

def loop(game):
	global occupiedFood
	occupiedFood = []
	for ant in game.ants[myteam]:
		found = False
		for anttask in anttasks:
			if anttask["antid"] == ant.id:
				found = True
				performTask(game, ant, anttask["task"])
				break
		if not found:
			if len(anttasks) < 4:
				chosenTask = Tasks.GetFood
			else:
				r = random.randrange(0, 100)
				if r < 45:
					chosenTask = Tasks.GetFood
				elif r < 45 + 45:
					chosenTask = Tasks.AttackAnts
				else:
					chosenTask = Tasks.AttackQueen
			anttasks.append({ "antid": ant.id, "task": chosenTask })
			performTask(game, ant, chosenTask)

def performTask(game, ant, task):
	if task == Tasks.GetFood:
		nonOccupiedFood = list(game.food)
		for food in occupiedFood:
			nonOccupiedFood.remove(food)
		if len(nonOccupiedFood) == 0:
			task = Tasks.AttackAnts
		else:
			goto(game, [ant], nonOccupiedFood)
	if task == Tasks.AttackAnts:
		if len(game.ants[enemyteam]) == 0:
			task = Tasks.AttackQueen
		else:
			goto(game, [ant], game.ants[enemyteam])
	if task == Tasks.AttackQueen:
		goto(game, [ant], [game.queens[enemyteam]])

def goto(game, ants, objects):
	for ant in ants:
		closestObject = None
		for obj in objects:
			if distance(ant, obj) < distance(ant, closestObject):
				closestObject = obj

		if isinstance(closestObject, Food):
			occupiedFood.append(closestObject)

		publicFunctions.moveAnt(ant, closestObject)

