# AdvancedTaskAI

# TODO: find trajectory of enemy ant and, if it's close, move there

import math, random

from antlib import *
import publicFunctions

myteam = 'J'
enemyteam = 'L'

game = None
ourHealth = 0
enemyHealth = 0

def loop(newGame):
    global game, ourHealth, enemyHealth
    game = newGame
    ourHealth = game.antHealth(myteam)
    enemyHealth = game.antHealth(enemyteam)

    availableFoodAnts = []
    while len(availableFoodAnts) < 5 and len(availableFoodAnts) < len(game.ants[myteam]):
        safestAnt = (None, float("inf"))
        for ant in game.ants[myteam]:
            if ant in availableFoodAnts:
                continue
            enemyDistance = float("inf")
            for enemyant in game.ants[enemyteam]:
                enemyDistance = min(enemyDistance, distance(ant, enemyant))
            if safestAnt[0] == None or enemyDistance > safestAnt[1]:
                safestAnt = (ant, enemyDistance)
        availableFoodAnts.append(safestAnt[0])

    for ant in game.ants[myteam]:
        if ant in availableFoodAnts:
            continue
        if enemyHealth == 0 or (ourHealth / enemyHealth > 10 and len(game.ants[myteam]) > 30):
            publicFunctions.moveAnt(ant, game.queens[enemyteam])
        elif ant.health < Ant.originalHealth * 0.75:
            availableFoodAnts.append(ant)
        else:
            publicFunctions.moveAnt(ant, closestEnemy(ant))

    foodDistances = {}
    for food in game.food:
        closestAnt = closestObject(food, availableFoodAnts)
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

