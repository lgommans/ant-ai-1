#!/usr/bin/env python

from antlib import *

def moveAnt(ant, towards):
	''' Moves an ant one step. '''
	if isinstance(towards, tuple):
		print("Moving ant towards " + str(towards))
		if towards[0] < -1 or towards[0] > 1 or towards[1] < -1 or towards[1] > 1:
			return False

		ant.x += towards[0]
		ant.y += towards[1]
		ant.health -= 1

	elif isinstance(towards, Object):
		x = 0
		y = 0
		if ant.x < towards.x:
			x = 1
		if ant.x > towards.x:
			x = -1
		if ant.y > towards.y:
			y = -1
		if ant.y < towards.y:
			y = 1

		moveAnt(ant, (x, y))

	return True


