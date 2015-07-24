#!/usr/bin/env python

# RandomTaskAI
# TODO: Does anyone attack enemy ants?!
# TODO: Mark food as "I'm going there" so ants go for separate foods.
# TODO: Dynamic task assignment?
# TODO: (Dynamic) task switching?

import math, random

from antlib import *
import publicFunctions

myteam = 'J'
enemyteam = 'L'

class Tasks:
	GetFood = 1
	AttackQueen = 2
	AttackAnts = 3

anttasks = []

def loop(game):
	for ant in game.ants[myteam]:
		found = False
		for anttask in anttasks:
			if anttask["antid"] == ant.id:
				found = True
				performTask(game, ant, anttask["task"])
				break
		if not found:
			r = random.randrange(0, 100)
			if r < 45:
				chosenTask = Tasks.GetFood
			elif r < 35:
				chosenTask = Tasks.AttackAnts
			else:
				chosenTask = Tasks.AttackQueen
			anttasks.append({ "antid": ant.id, "task": chosenTask })
			performTask(game, ant, chosenTask)

def performTask(game, ant, task):
	if task == Tasks.GetFood:
		goto(game, [ant], game.food)
	if task == Tasks.AttackAnts:
		goto(game, [ant], game.ants[enemyteam])
	if task == Tasks.AttackQueen:
		goto(game, [ant], [game.queens[enemyteam]])

def goto(game, ants, objects):
	for ant in ants:
		closestObject = None
		for obj in objects:
			if distance(ant, obj) < distance(ant, closestObject):
				closestObject = obj

		publicFunctions.moveAnt(ant, closestObject)

