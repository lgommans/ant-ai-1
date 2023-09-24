# TODO: make them compatible with more than one enemy team
# TODO: find trajectory of enemy ant and, if it's close, move there

import math, random

from antlib import *
import publicFunctions

class AI:
    def __init__(self, myteam, enemyteams):
        self.myteam = myteam
        self.enemyteams = enemyteams
        self.name = 'AdvancedTaskAI2'

    def queenDied(self, team):
        if team in self.enemyteams:
            self.enemyteams.remove(team)

    def antDied(self, ant):
        pass

    def loop(self, game):
        self.ourHealth = game.antHealth(self.myteam)
        self.enemyHealth = game.antHealth(self.enemyteams[0])

        availableFoodAnts = []
        while len(availableFoodAnts) < 5 and len(availableFoodAnts) < len(game.ants[self.myteam]):
            safestAnt = (None, float("inf"))
            for ant in game.ants[self.myteam]:
                if ant in availableFoodAnts:
                    continue
                enemyDistance = float("inf")
                for enemyant in game.ants[self.enemyteams[0]]:
                    enemyDistance = min(enemyDistance, distance(ant, enemyant))
                if safestAnt[0] == None or enemyDistance > safestAnt[1]:
                    safestAnt = (ant, enemyDistance)
            availableFoodAnts.append(safestAnt[0])

        for ant in game.ants[self.myteam]:
            if ant in availableFoodAnts:
                continue
            if self.enemyHealth == 0 or (self.ourHealth / self.enemyHealth > 10 and len(game.ants[self.myteam]) > 30):
                publicFunctions.moveAnt(ant, game.queens[self.enemyteams[0]])
            elif ant.health < Ant.originalHealth * 0.75:
                availableFoodAnts.append(ant)
            else:
                publicFunctions.moveAnt(ant, self.closestEnemy(ant, game))

        foodDistances = {}
        for food in game.food:
            closestAnt = self.closestObject(food, availableFoodAnts)
            if closestAnt != None:
                if closestAnt not in foodDistances:
                    foodDistances[closestAnt] = {}
                foodDistances[closestAnt][food] = distance(food, closestAnt)
        
        for ant in foodDistances:
            closestFood = None
            for food in foodDistances[ant]:
                if closestFood == None or foodDistances[ant][food] < foodDistances[ant][closestFood]:
                    closestFood = food
            publicFunctions.moveAnt(ant, closestFood)
            availableFoodAnts.remove(ant)
        
        for ant1 in availableFoodAnts:
            for ant2 in availableFoodAnts:
                if ant1 == ant2:
                    continue
                if ant1.position == ant2.position:
                    obj = Object((ant2.position[0] + random.choice((-1, 0)), ant2.position[1] + random.choice((-1, 0))))
                    while obj.position[0] < 0 or obj.position[1] < 0 or obj.position[0] >= game.gridwidth or obj.position[1] >= game.gridheight:
                        obj = Object((ant2.position[0] + random.choice((-1, 0)), ant2.position[1] + random.choice((-1, 0))))
                    publicFunctions.moveAnt(ant2, obj)

    def closestEnemy(self, ant, game):
        if len(game.ants[self.enemyteams[0]]) > 0:
            return self.closestObject(ant, game.ants[self.enemyteams[0]])
        return game.queens[self.enemyteams[0]]

    def closestObject(self, obj, collection):
        closestItem = None
        for item in collection:
            if distance(obj, item) < distance(obj, closestItem):
                closestItem = item
        return closestItem

