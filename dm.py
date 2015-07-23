#!/usr/bin/env python

import sys
from time import sleep
from random import randrange as rand

from antlib import *
from publicFunctions import *

from ai1 import loop as ai1loop
from ai2 import loop as ai2loop

def read_grid(filename):
    execfile("gridObjects-" + filename + ".py")

def displayGrid():
    sys.stdout.write("\n" * 6)

    emptyTile = ' - '
    grid = [[ emptyTile for y in range(game.gridheight)] for x in range(game.gridwidth)]

    for obj in game.allObjects():
        if grid[obj.position[0]][obj.position[1]] != emptyTile:
            grid[obj.position[0]][obj.position[1]].replace(' ', '+')
        else:
            grid[obj.position[0]][obj.position[1]] = obj.displayAs

    for x in grid:
        for y in x:
            sys.stdout.write(str(y))
        sys.stdout.write("\n")

def spawn_food():
    i = 0
    while True:
        i += 1
        if i > 9000:
            print("WARN: No free space for food?")
            break

        x = rand(0, game.gridwidth)
        y = rand(0, game.gridheight)

        if occupied(game.allObjects(), (x, y)):
            continue

        game.food.append(Food((x, y)))
        break

def gameMaintenance():
    game.time += 1

    spawn_food()

    removeFood = []
    removeAnt = []

    for antteam in game.ants:
        for ant in game.ants[antteam]:
            for antteam2 in game.ants:
                if antteam2 != antteam:
                    for enemyant in game.ants[antteam2]:
                        if enemyant.position == ant.position:
                            # Enemyant and ant are are the same position!
                            enemyanthealth = enemyant.health

                            # Prevent them from using their health twice
                            if ant.lastAttack != game.time and ant.health >= 0:
                                enemyant.health -= math.sqrt(ant.health) * slowdeath
                            if enemyant.lastAttack != game.time and enemyanthealth >= 0:
                                ant.health -= math.sqrt(enemyanthealth) * slowdeath

                            enemyant.lastAttack = game.time
                            ant.lastAttack = game.time

                            if ant.health <= 0 and ant not in removeAnt:
                                removeAnt.append(ant)
                            if enemyant.health <= 0 and enemyant not in removeAnt:
                                removeAnt.append(enemyant)

            for queenteam in game.queens:
                if ant.position == game.queens[queenteam].position and queenteam != ant.team:
                    # ant is at the same location as this enemy queen!
                    game.queens[queenteam].health -= ant.health
                    if ant not in removeAnt:
                        removeAnt.append(ant)

                    if game.queens[queenteam].health <= 0:
                        print("Team " + queenteam + " lost!")
                        sys.exit(0)

            # If two ants reach a food at the same time, they both get it.
            for food in game.food:
                if ant.position == food.position and food.amount > 0:
                    ant.health += food.amount * (1 - Queen.foodTax)
                    ant.health = min(ant.health, ant.originalHealth)
                    game.queens[ant.team].health += food.amount * Queen.foodTax
                    game.queens[ant.team].health = min(game.queens[ant.team].health, Queen.originalHealth)
                    game.ants[ant.team].append(Ant(game.queens[ant.team].position, ant.team))
                    food.amount = 0
                    removeFood.append(food)

    for ant in removeAnt:
        game.ants[ant.team].remove(ant)

    for food in removeFood:
        game.food.remove(food)


# Initialization
slowdeath = 3 # When ants attack each other, they lose (sqrt(enemyant.health)*slowdeath)

game = Game((50, 79))

queenpos = (0, 0)
game.queens['L'] = Queen(game, queenpos, 'L')
game.ants['L'].append(Ant(game.queens['L'].position, 'L'))

queenpos = game.gridwidth - 1, game.gridheight - 1
game.queens['J'] = Queen(game, queenpos, 'J')
game.ants['J'].append(Ant(game.queens['J'].position, 'J'))

# Main loop
while True:
    gameMaintenance()
    ai1loop(game)
    ai2loop(game)
    displayGrid()
    sleep(0.1) 

