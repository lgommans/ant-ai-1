#!/usr/bin/env python

from antlib import *
import traceback

def moveAnt(ant, towards):
	''' Moves an ant one step. '''
	if isinstance(towards, tuple):
		newposition = (ant.position[0] + towards[0], ant.position[1] + towards[1])
		if towards[0] < -1 or towards[0] > 1 or towards[1] < -1 or towards[1] > 1:
			return False

		if newposition == ant.position:
			return False

		ant.position = newposition
		ant.health -= 1

	elif isinstance(towards, Object):
		x = 0
		y = 0
		if ant.position[0] < towards.position[0]:
			x = 1
		if ant.position[0] > towards.position[0]:
			x = -1
		if ant.position[1] > towards.position[1]:
			y = -1
		if ant.position[1] < towards.position[1]:
			y = 1

		return moveAnt(ant, (x, y))

	return True


