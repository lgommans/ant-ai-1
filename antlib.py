#!/usr/bin/env python

class Game:
	def __init__(self, gridsize):
		self.ants = {}
		self.queens = {}
		self.food = []
		self.gridsize = gridsize # width,height
	
	def allObjects(self):
		allObjs = []
		allObjs += self.food
		for team in self.ants:
			allObjs += self.ants[team]
		for team in self.queens:
			allObjs.append(self.queens[team])
		return allObjs

class Object:
	def __init__(self, x, y, displayAs):
		self.displayAs = displayAs
		self.x = x
		self.y = y

class Ant(Object):
	originalHealth = 100
	def __init__(self, x, y, team):
		super(Ant, self).__init__(x, y, ' A' + team)
		self.team = team
		self.health = Ant.originalHealth
		self.carrying = False

class Queen(Object):
	foodTax = 0.05
	originalHealth = 1000
	def __init__(self, x, y, team):
		super(Queen, self).__init__(x, y, ' Q' + team)
		self.team = team
		self.health = Queen.originalHealth

class Food(Object):
	amount = 100
	def __init__(self, x, y):
		super(Food, self).__init__(x, y, ' F ')

