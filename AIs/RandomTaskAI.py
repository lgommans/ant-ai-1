import math, random

from antlib import *
import publicFunctions

class Tasks:
    GetFood = 1
    AttackQueen = 2
    AttackAnts = 3

class AI:
    def __init__(self, myteam, enemyteams):
        self.myteam = myteam
        self.enemyteams = enemyteams
        self.name = 'RandomTaskAI'

        self.anttasks = {}

    def queenDied(self, team):
        if team in self.enemyteams:
            self.enemyteams.remove(team)

    def antDied(self, ant):
        del self.anttasks[ant.id]

    def loop(self, game):
        self.occupiedFood = []
        for ant in game.ants[self.myteam]:
            if ant.id in self.anttasks:
                self.performTask(game, ant, self.anttasks[ant.id])
            else:
                if len(self.anttasks) < 4:
                    chosenTask = Tasks.GetFood
                else:
                    r = random.randrange(0, 100)
                    if r < 45:
                        chosenTask = Tasks.GetFood
                    elif r < 45 + 45:
                        chosenTask = Tasks.AttackAnts
                    else:
                        chosenTask = Tasks.AttackQueen
                self.anttasks[ant.id] = chosenTask
                self.performTask(game, ant, chosenTask)

    def performTask(self, game, ant, task):
        if task == Tasks.GetFood:
            nonOccupiedFood = list(game.food)
            for food in self.occupiedFood:
                nonOccupiedFood.remove(food)
            if len(nonOccupiedFood) == 0:
                task = Tasks.AttackAnts
            else:
                # TODO rather than going to the nearest unoccupied food, we should be looking from the food's perspective which ant is closest. We might be sending an ant to its closest food, on the other side of the game, and then marking it as occupied
                self.goto(game, ant, nonOccupiedFood)
                return

        fewestEnemiesTeam = None
        for et in self.enemyteams:
            if fewestEnemiesTeam is None or len(game.ants[et]) < len(game.ants[fewestEnemiesTeam]):
                fewestEnemiesTeam = et

        if task == Tasks.AttackAnts:
            if len(game.ants[fewestEnemiesTeam]) == 0:
                task = Tasks.AttackQueen
            else:
                self.goto(game, ant, game.ants[fewestEnemiesTeam])

        if task == Tasks.AttackQueen:
            self.goto(game, ant, [game.queens[fewestEnemiesTeam]])

    def goto(self, game, ant, objects):
        closestObject = None
        for obj in objects:
            if distance(ant, obj) < distance(ant, closestObject):
                closestObject = obj

        if isinstance(closestObject, Food):
            self.occupiedFood.append(closestObject)

        publicFunctions.moveAnt(ant, closestObject)

