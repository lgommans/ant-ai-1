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

    grid = [[ " - " for x in range(game.gridsize[0])] for y in range(game.gridsize[1])]

    for obj in game.allObjects():
        grid[obj.x][obj.y] = obj.displayAs

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

        x = rand(0, game.gridsize[0])
        y = rand(0, game.gridsize[1])

        occupied = False
        for obj in game.allObjects():
            if obj.x == x and obj.y == y:
                occupied = True
                break

        if occupied:
            continue

        game.food.append(Food(x, y))
        break

def gridMaintenance():
    removeFood = []
    for antteam in game.ants:
        for ant in game.ants[antteam]:
            for queenteam in game.queens:
                if ant.x == game.queens[queenteam].x \
                    and ant.y == game.queens[queenteam].y \
                    and game.queens[queenteam] != ant.team:
                    game.queens[queenteam].health -= ant.health
                    if game.queens[queenteam].health <= 0:
                        print("Team " + queenteam + " lost!")
                        sys.exit(0)

            # If two ants reach a food at the same time, they both get it.
            for food in game.food:
                if ant.x == food.x and ant.y == food.y:
                    ant.health += Food.amount * (1 - Queen.foodTax)
                    ant.health = min(ant.health, ant.originalHealth)
                    game.queens[ant.team].health += Food.amount * Queen.foodTax
                    game.queens[ant.team].health = min(game.queens[ant.team].health, Queen.originalHealth)
                    removeFood.append(food)

    for food in removeFood:
        game.food.remove(food)

# Constants
directionx = [ 0,  1,  1,  1,  0, -1, -1, -1]
directiony = [-1, -1,  0,  1,  1,  1,  0, -1]

# Initialization
game = Game((35, 35))
#read_grid("mygrid")

game.queens['L'] = Queen(0, 0, 'L')
game.queens['J'] = Queen(game.gridsize[0] - 1, game.gridsize[1] - 1, 'J')

game.ants['L'] = []
game.ants['L'].append(Ant(1, 1, 'L'))

game.ants['J'] = []
game.ants['J'].append(Ant(game.gridsize[0] - 2, game.gridsize[1] - 2, 'J'))

# Main loop
while True:
    spawn_food()
    ai1loop(game)
    ai2loop(game)
    displayGrid()
    gridMaintenance()
    sleep(0.2) 
