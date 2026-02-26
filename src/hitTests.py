from gameGraphics import gameStateObject
from obstacleClasses import obstacle, obstacleCourse
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pytest

# Tests collision with obstacle
def testHit(actions, obstacleType, speed):
    # Initialize game
    gameState = gameStateObject(speed, test=True)
    # Load test stage
    gameState.load_stage("test")
    # Saves all hits or no-hits
    hitList = []
    # Used to check if game was won
    winList = []
    # Execute all keystrokes or waits
    for action in actions:
        # If a key was pressed
        if action != 0:
            gameState.keyboard(action)
        
        # Move obstacles and check if game was won
        win = gameState.stage.moveAllObs(speed)
        winList.append(win)
        # Check if player collided with obstacle
        hit = gameState.stage.checkHit(gameState.camX, gameState.camY)
        hitList.append(hit)

    # Game should not be won in these tests
    assert(winList.count(0) == 0)
    # Check that only the last action resulted in a hit, i.e. everything else was 0
    assert(hitList.contains(0) == (len(hitList) - 1))
    # Check that the hit obstacle was of correct type
    assert(hitList[-1][1] == obstacleType)

# Tests collision with obstacle
def testWin(actions, speed):
    # Initialize game
    gameState = gameStateObject(speed, test=True)
    # Load test stage
    gameState.load_stage("test")
    # Saves all hits or no-hits
    hitList = []
    # Used to check if game was won
    winList = []
    # Execute all keystrokes or waits
    for action in actions:
        # If a key was pressed
        if action != 0:
            gameState.keyboard(action)
        
        # Move obstacles and check if game was won
        win = gameState.stage.moveAllObs(speed)
        winList.append(win)
        # Check if player collided with obstacle
        hit = gameState.stage.checkHit(gameState.camX, gameState.camY)
        hitList.append(hit)

    # Game should not be lost in these tests
    assert(hitList.contains(0) == len(hitList))
    # Check that only the last action resulted in a win
    assert(winList[-1] == 0)
    assert(winList.contains(1) == 0)

# TODO: Add these tests
#
# gameGraphics.py
# 1 - load_stage()
#       Check that the correct stage was loaded
# 2 - keyboard()
#       Check that player moves correctly with keystrokes
#       And that no illegal moves are permitted
# 3 - idle()
#       Check that player does move back to y = 0 at correct time
#
# obstacleClasses.py
# 1 - reshape()
#       Check that object gets correct form after reshaping
# 2 - moveBack()
#       Check that obstacle is moved back to start
# 3 - moveObstacle()
#       Check that obstacle is moved forward by correct amount
# 4 - moveAllObs()
#       Same as with 2 and 3, but for all obstacles
# 5 - relocate()
#       Check that obstacle gets correct x-axis place
# 6 - checkHit()
#       Check that at no point in the game the player had same coordinates as a box
#       Could be used with testHit()