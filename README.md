# Running it

Simple: `python3 dm.py`

![Screenshot of running simulation](/screenshot.png?raw=true)

Changing which AI to use is done by changing the imports in dm.py, and
optionally the main simulation loop.

## Ant AI

This variant allows each ant to see the whole playing field and each other.

More realistically, but also more difficultly, would be when ants can only see
a little bit around them and have to communicate with chemical signals. Perhaps
in a next version.

## Files

dm.py is the Dungeon Master; the game controller. More documentation is TODO.

