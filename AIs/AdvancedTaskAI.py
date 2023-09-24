# TODO: make them compatible with more than one enemy team

import math, random

from antlib import *
import publicFunctions

BATTLE = 0
GATHER = 1

class AI:
    def __init__(self, myteam, enemyteams):
        self.myteam = myteam
        self.enemyteams = enemyteams
        self.name = 'AdvancedTaskAI'

        self.antTasks = {}
        self.foodAnts = []
        self.battleAnts = []

    def antDied(self, ant):
        pass

    def loop(self, game):
        ourHealth = game.antHealth(self.myteam)
        enemyHealth = game.antHealth(self.enemyteams[0])
        deadAnts = list(self.foodAnts + self.battleAnts)
        for ant in game.ants[self.myteam]:
            if ant.id in self.antTasks:
                deadAnts.remove(ant)
            else:
                if ourHealth > enemyHealth * 1.5 and len(self.foodAnts) > 4:
                    chosenTask = BATTLE
                elif ourHealth < enemyHealth * 0.9:
                    chosenTask = GATHER
                else:
                    r = random.randrange(0, 100)
                    if r < 65:
                        chosenTask = GATHER
                    else:
                        chosenTask = BATTLE
                self.antTasks[ant.id] = chosenTask
                if chosenTask == BATTLE:
                    self.battleAnts.append(ant)
                if chosenTask == GATHER:
                    self.foodAnts.append(ant)

        for ant in deadAnts:
            if self.antTasks[ant.id] == GATHER:
                self.foodAnts.remove(ant)
            else:
                self.battleAnts.remove(ant)

        availableFoodAnts = list(self.foodAnts)
        for food in game.food:
            closestAnt = self.closestObject(food, availableFoodAnts)
            if closestAnt != None:
                availableFoodAnts.remove(closestAnt)
                publicFunctions.moveAnt(closestAnt, food)
        
        for ant in self.battleAnts:
            self.battle(ant, ourHealth, enemyHealth, game)

    def battle(self, ant, ourHealth, enemyHealth, game):
        if enemyHealth == 0 or (ourHealth / enemyHealth > 10 and len(game.ants[self.myteam]) > 50):
            publicFunctions.moveAnt(ant, game.queens[self.enemyteams[0]])
            return

        if ant.health < Ant.originalHealth * 0.75:
            cfood = self.closestFood(ant, game)
            if distance(ant, cfood) < Ant.originalHealth * 0.1:
                publicFunctions.moveAnt(ant, cfood)
                return
        publicFunctions.moveAnt(ant, self.closestEnemy(ant, game))

    def closestFood(self, ant, game):
        return self.closestObject(ant, game.food)

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

