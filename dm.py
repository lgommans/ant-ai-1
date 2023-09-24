#!/usr/bin/env python3

# TODO: use curses? Or pygame?

import sys, math, random, time
from colorama import Fore as fgcol, Back as bgcol, Style as charbrightness

from antlib import *
from publicFunctions import *
from external import NonBlockingConsole

from AIs import *

def color(team = None):
    if not colorsEnabled:
        return

    if team == None:
        return bgcol.RESET
    elif team == 'none':
        return bgcol.GREEN
    elif team == 'J':
        return bgcol.RED
    elif team == 'L':
        return bgcol.BLUE

def read_grid(filename):
    execfile("gridObjects-" + filename + ".py")

def cls():
    # Not exactly cls ('clear screen'), but it's enough
    sys.stdout.write("\n" * 6)

def displayStats():
    global enabled

    if enabled['antCount']:
        displayStat("Ant count", len(game.ants['L']), len(game.ants['J']))

    if enabled['antHealth']:
        displayStat("Ants health", game.antHealth('L'), game.antHealth('J'))

    if enabled['queenHealth']:
        displayStat("Queen health", game.queens['L'].health, game.queens['J'].health)

    if enabled['time']:
        fps = game.time / (time.time() - starttime)
        if fps > 10:
            fps = round(fps)
        elif fps > 1:
            fps = round(fps, 1)
        else:
            fps = round(fps, 2)
        sys.stdout.write(f"frame#{game.time:_}; FPS: {fps}\t")

    sys.stdout.write(color() + "\n")

def displayStat(title, statL, statJ):
    if statJ != 0:
        n = round(statL / statJ * 100)
        perc = ''
        if n > 101:
            perc = color('L')
        if n < 99:
            perc = color('J')
        perc += str(n) + "%" + color()
    else:
        perc = 'INF'
    sys.stdout.write(title + " " + color('L') + "L: " + str(round(statL)) + color() + "; " + color('J') + "J: " + str(round(statJ)) + color() + " (L/J=" + perc + "). \t" + color())

def displayGrid():
    outstr = ''
    emptyTile = color() + ' - '
    grid = [[ emptyTile for y in range(game.gridheight)] for x in range(game.gridwidth)]

    for obj in game.allObjects():
        text = ''
        if hasattr(obj, 'team'):
            if obj.team == 'J':
                text = color('J')
            else:
                text = color('L')
        else:
            text = color('none')

        text += obj.displayAs
        if grid[obj.position[0]][obj.position[1]] != emptyTile:
            text = text.replace(' ', '+')
        grid[obj.position[0]][obj.position[1]] = text + color()

    for x in grid:
        for y in x:
            outstr += str(y)
        outstr += "\n"

    print(outstr)

def spawn_food():
    i = 0
    while True:
        i += 1
        if i > 9000:
            print("WARN: No free space for food?")
            break

        x = random.randrange(0, game.gridwidth)
        y = random.randrange(0, game.gridheight)

        if occupied(game.allObjects(), (x, y)):
            continue

        game.food.append(Food(game, (x, y)))
        break

def gameMaintenance():
    game.time += 1

    removeFood = {}
    removeAnt = {}

    teamorder = list(game.teams.keys())
    random.shuffle(teamorder)
    for antteam1 in game.teams:
        for ant in game.ants[antteam1]:
            if ant in removeAnt:
                continue
            if ant.health <= 0:
                if ant not in removeAnt:
                    removeAnt[ant] = True
                continue
            for antteam2 in game.teams:
                if antteam2 == antteam1:
                    continue
                for enemyant in game.ants[antteam2]:
                    if enemyant in removeAnt:
                        continue
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
                            removeAnt[ant] = True
                        if enemyant.health <= 0 and enemyant not in removeAnt:
                            removeAnt[enemyant] = True

            for queenteam in game.queens:
                if ant.position == game.queens[queenteam].position and queenteam != ant.team:
                    # ant is at the same location as this enemy queen!
                    game.queens[queenteam].health -= ant.health
                    if ant.id not in removeAnt:
                        removeAnt[ant] = True

                    if game.queens[queenteam].health <= 0:
                        print("Team " + queenteam + " lost!")
                        displayStats()
                        sys.exit(0)

    # If two ants reach a food at the same time, they get an equal share
    for food in game.food:
        candidates = []
        teamShares = {}
        for team in game.ants:
            for ant in game.ants[team]:
                if ant.position == food.position:
                    candidates.append(ant)
                    teamShares[ant.team] = 0  # initialize the key in the array
        if len(candidates) > 0:
            for ant in candidates:
                amount = food.amount / len(candidates)
                teamShares[ant.team] += amount
                ant.health += amount * (1 - Queen.foodTax)
                ant.health = min(ant.health, ant.originalHealth)
                game.queens[ant.team].health += amount * Queen.foodTax
                game.queens[ant.team].health = min(game.queens[ant.team].health, Queen.originalHealth)
                removeFood[food] = True

            # only spawn the ant for the team that got most of the food. Not sure if this should be even stricter, like 0.9, or spawning an ant with proportional health or so...
            teamWithGreatestShare = max(teamShares, key=teamShares.get)
            if teamShares[teamWithGreatestShare] > 0.5:
                game.addAnt(ant.team)

    for ant in removeAnt:
        game.teams[ant.team].antDied(ant)
        game.ants[ant.team].remove(ant)

    for food in removeFood:
        game.food.remove(food)

    if len(game.ants['J']) == 0 and len(game.ants['L']) == 0:
        print("There are no winners in this game.")
        sys.exit(0)

def inputHandling():
    global framedelay, drawevery, headless

    # NonBlockingConsole gets keystrokes from the console. It's a bit whacky, but the best I've been able to find without writing something elaborate or multi-threaded myself.
    # Users need to hit enter after typing a character, but it's good enough for now.
    nbc = NonBlockingConsole()
    char = nbc.get_data()
    if char != False:
        if char == 'q':
            sys.exit(0)
        elif char == '+':
            framedelay /= 1.3
        elif char == '-':
            framedelay *= 1.3
        elif char == '=':
            drawevery *= 1.5
        elif char == '_':
            drawevery /= 1.5
        elif char == 'h':
            headless = not headless
            if headless:
                print('Headless mode on (use ? for help)')
        elif char == '?':
            print('? this help overview')
            print('q quit')
            print('+ sleep less long between frames')
            print('- sleep longer between frames')
            print('= increase frame skipping')
            print('_ decrease frame skipping')
            print('h toggle headless mode')

# Initialization
starttime = time.time()
slowdeath = 3 # When ants attack each other, they lose (sqrt(enemyant.health)*slowdeath)
framedelay = 0.1
drawevery = 1
enabled = { 'antHealth': True, 'queenHealth': True, 'antCount': True, 'time': True }
colorsEnabled = True
headless = False

game = Game(dimensions=(49, 49), ais={
    'L': AdvancedTaskAI2,
    'J': AdvancedTaskAI,
})

for i in range(0, 10):
    spawn_food()

# Main loop
while True:
    for i in range(0, 2):
        spawn_food()
    gameMaintenance()
    inputHandling()
    teamorder = list(game.teams.keys())
    random.shuffle(teamorder)
    for team in teamorder:
        game.teams[team].loop(game)
    if not headless:
        if game.time % math.ceil(drawevery) == 0:
            cls()
            displayStats()
            displayGrid()
        time.sleep(framedelay)

