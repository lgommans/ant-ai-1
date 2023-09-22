# SimpleAI

import math

from antlib import *
import publicFunctions

class AI:
    def __init__(self, myteam, enemyteams):
        self.myteam = myteam
        self.enemyteams = enemyteams

    def loop(self, game):
        enemyants = []
        enemyqueens = []
        for enemyteam in self.enemyteams:
            enemyants += game.ants[enemyteam]
            enemyqueens.append(game.queens[enemyteam])

            if len(enemyants) > 0:
                if self.groupHealth(game.ants[self.myteam]) <= self.groupHealth(game.ants[enemyteam]):
                    self.goto(game, game.ants[self.myteam], game.food)
                else:
                    self.goto(game, game.ants[self.myteam], enemyants)
            else:
                # No more enemy ants.
                if self.groupHealth(game.ants[self.myteam]) > game.queens[enemyteam].health:
                    self.goto(game, game.ants[self.myteam], enemyqueens)
                else:
                    self.goto(game, game.ants[self.myteam], game.food)

    def goto(self, game, ants, objects):
        for ant in ants:
            closestObject = None
            for obj in objects:
                if distance(ant, obj) < distance(ant, closestObject):
                    closestObject = obj
            publicFunctions.moveAnt(ant, closestObject)

    def groupHealth(self, ants):
        total = 0
        for ant in ants:
            total += ant.health

        return total

