#!/usr/bin/env python

# SimpleAI

import math

from antlib import *
import publicFunctions

def initAI(myteam, enemyteams):
    AI(myteam, enemyteams)

class AI:
    def __init__(self, myteam, enemyteams):
        self.myteam = myteam
        self.enemyteams = enemyteams

    def loop(self, game):
        enemyants = []
        enemyqueens = []
        for enemyteam in enemyteams:
            enemyants += game.ants[enemyteam]
            enemyqueens += game.queens[enemyteam]

        if len(enemyants) > 0:
            if self.groupHealth(enemyteam) <= self.groupHealth(enemyteam):
                self.goto(game, game.ants[myteam], game.food)
            else:
                self.goto(game, game.ants[myteam], enemyants)
        else:
            # No more enemy ants.
            if self.groupHealth(game.ants[myteam]) > game.queens[enemyteam].health:
                self.goto(game, game.ants[myteam], enemyqueens)
            else:
                self.goto(game, game.ants[myteam], game.food)

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

