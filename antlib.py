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
    def __init__(self, dimensions, ais):
        self.ants = {}
        self.queens = {}
        self.food = []
        self.gridwidth = dimensions[0]
        self.gridheight = dimensions[1]
        self.time = 0
        self.newid = 0

        queenPositions = iter((
            (0                 , 0                  ),
            (self.gridwidth - 1, self.gridheight - 1),
            (self.gridwidth - 1, 0                  ),
            (0                 , self.gridheight - 1),
        ))

        self.teams = {}
        for team in ais:
            otherteams = list(ais.keys())
            otherteams.remove(team)
            self.teams[team] = ais[team].AI(myteam=team, enemyteams=otherteams)
            self.queens[team] = Queen(self, next(queenPositions), team)
            self.ants[team] = []
            self.addAnt(team)  # start each team off with one ant to gather food

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

    def addAnt(self, team):
        self.ants[team].append(Ant(team, self.newid, self.queens[team].position))
        self.newid += 1


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
    def __init__(self, team, newid, position):
        super().__init__(position, ' A' + team)
        self.team = team
        self.health = Ant.originalHealth
        self.lastAttack = 0
        self.id = newid

class Queen(Object):
    foodTax = 0.05  # 0-1
    originalHealth = 1000
    def __init__(self, game, position, team):
        super().__init__(position, ' Q' + team)
        self.team = team
        self.health = Queen.originalHealth
        self.id = game.newid
        game.newid += 1

class Food(Object):
    amount = 100
    def __init__(self, game, position):
        super().__init__(position, ' F ')
        self.id = game.newid
        game.newid += 1
        self.amount = Food.amount

