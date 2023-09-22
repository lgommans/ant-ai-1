# AdvancedTaskAI

import math, random

from antlib import *
import publicFunctions

myteam = 'L'
enemyteam = 'J'

antTasks = {}
BATTLE = 0
GATHER = 1
foodAnts = []
battleAnts = []
game = None

def loop(newGame):
    global game
    game = newGame
    ourHealth = game.antHealth(myteam)
    enemyHealth = game.antHealth(enemyteam)
    deadAnts = list(foodAnts + battleAnts)
    for ant in game.ants[myteam]:
        if ant.id in antTasks:
            deadAnts.remove(ant)
        else:
            if ourHealth > enemyHealth * 1.5 and len(foodAnts) > 4:
                chosenTask = BATTLE
            elif ourHealth < enemyHealth * 0.9:
                chosenTask = GATHER
            else:
                r = random.randrange(0, 100)
                if r < 65:
                    chosenTask = GATHER
                else:
                    chosenTask = BATTLE
            antTasks[ant.id] = chosenTask
            if chosenTask == BATTLE:
                battleAnts.append(ant)
            if chosenTask == GATHER:
                foodAnts.append(ant)

    for ant in deadAnts:
        if antTasks[ant.id] == GATHER:
            foodAnts.remove(ant)
        else:
            battleAnts.remove(ant)

    availableFoodAnts = list(foodAnts)
    for food in game.food:
        closestAnt = closestObject(food, availableFoodAnts)
        if closestAnt != None:
            availableFoodAnts.remove(closestAnt)
            publicFunctions.moveAnt(closestAnt, food)
    
    for ant in battleAnts:
        battle(ant, ourHealth, enemyHealth)

def battle(ant, ourHealth, enemyHealth):
    if enemyHealth == 0 or (ourHealth / enemyHealth > 10 and len(game.ants[myteam]) > 50):
        publicFunctions.moveAnt(ant, game.queens[enemyteam])
        return

    if ant.health < Ant.originalHealth * 0.75:
        cfood = closestFood(ant)
        if distance(ant, cfood) < Ant.originalHealth * 0.1:
            publicFunctions.moveAnt(ant, cfood)
            return
    publicFunctions.moveAnt(ant, closestEnemy(ant))

def closestFood(ant):
    return closestObject(ant, game.food)

def closestEnemy(ant):
    if len(game.ants[enemyteam]) > 0:
        return closestObject(ant, game.ants[enemyteam])
    return game.queens[enemyteam]

def closestObject(obj, collection):
    closestItem = None
    for item in collection:
        if distance(obj, item) < distance(obj, closestItem):
            closestItem = item
    return closestItem

