# RandomAI

import math, random

from antlib import *
import publicFunctions

class AI:
    def __init__(self, myteam, enemyteams):
        self.myteam = myteam
        self.enemyteams = enemyteams

    def loop(self, game):
        for ant in game.ants[self.myteam]:
            i = 0
            while True:
                i += 1
                if i > 9001:
                    print("Nowhere to go?")
                    break

                c1 = random.choice((-1, 0, 1))
                c2 = random.choice((-1, 0, 1))
                newpos = (ant.position[0] + c1, ant.position[1] + c2)
                if self.possible(game, newpos[0], newpos[1]):
                    publicFunctions.moveAnt(ant, (c1, c2))
                    break

    def possible(self, game, x, y):
        if x < 0 or y < 0 or x >= game.gridwidth or y >= game.gridheight:
            return False
        return True

