import math

def distance(obj1, obj2):
	''' Returns Pythagorean distance. '''

	# Exception case: the distance from something to nothing is infinity. Any object is closer than no object.
	if obj1 == None or obj2 == None:
		return float('inf') # Always higher than any other value except itself

	dist = math.sqrt(abs(obj1.position[0] - obj2.position[0]) ** 2 + abs(obj1.position[1] - obj2.position[1]) ** 2)
	return dist

def occupied(objects, position):
	occupied = False
	for obj in objects:
		if obj.position[0] == position[0] and obj.position[1] == position[1]:
			return True

	return False

class Game:
	def __init__(self, dimensions):
		self.ants = {}
		self.queens = {}
		self.food = []
		self.gridwidth = dimensions[0]
		self.gridheight = dimensions[1]
		self.time = 0
		self.newid = 0
	
	def allObjects(self):
		allObjs = []
		allObjs += self.food
		for team in self.ants:
			allObjs += self.ants[team]
		for team in self.queens:
			allObjs.append(self.queens[team])
		return allObjs

	def noFood(self, objects):
		nofood = []
		for obj in objects:
			if not isinstance(obj, Food):
				nofood.append(obj)

		return nofood
	
	def antHealth(self, team):
		total = 0
		for ant in self.ants[team]:
			total += ant.health
		return total

class Object:
	def __init__(self, position, displayAs = None):
		self.displayAs = displayAs
		self.position = position

class Ant(Object):
	originalHealth = 100
	def __init__(self, game, team):
		super().__init__(game.queens[team].position, ' A' + team)
		self.team = team
		self.health = Ant.originalHealth
		self.lastAttack = 0
		self.id = game.newid
		game.newid += 1
		game.ants[team].append(self)

class Queen(Object):
	foodTax = 0.05
	originalHealth = 1000
	def __init__(self, game, position, team):
		super().__init__(position, ' Q' + team)
		self.team = team
		self.health = Queen.originalHealth
		self.id = game.newid
		game.newid += 1
		game.ants[team] = []

class Food(Object):
	amount = 100
	def __init__(self, game, position):
		super().__init__(position, ' F ')
		self.id = game.newid
		game.newid += 1
		self.amount = Food.amount

