from gameGraphics import gameStateObject
from obstacleClasses import obstacle, obstacleCourse
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
#import pytest

# Tests collision with obstacle
# TODO: Check that at no point in the game the player had same coordinates as a box
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

# Test loading the different stages
def testLoad(stageNames, stages, recPositions):
    for i in range(0, len(stageNames)):
        # Initialize
        gameState = gameStateObject("0.5", test=True)
        gameState.load_stage(stageNames[i])
        # Test
        assert(gameState.obstacleTypes == stages[i])
        assert(gameState.recXPositions == recPositions[i])

# Test the keyboard functionality
def testKeyboard():
    # Initialize game with extremely low speed, so that no object hits when testing keyboard functionality
    gameState = gameStateObject("0.00001", test=True)
    gameState.load_stage("test")
    # Check that initial position is correct
    assert(gameState.camX == 0)
    assert(gameState.camY == 0)
    assert(gameState.camZ == 0)
    # Test that WASD keys move the player correctly
    gameState.keyboard(b'a')
    assert(gameState.camX == 1)
    gameState.keyboard(b'd')
    assert(gameState.camX == 0)
    gameState.keyboard(b'd')
    assert(gameState.camX == -1)
    gameState.keyboard(b'w')
    assert(gameState.camY == 0.5)
    # Test that jumping causes the jump timer to grow
    gameState.idle()
    assert(gameState.jumpTime == 1)
    # Test that player moves back to ground after jump timer resets
    for i in range(100):
        gameState.idle()
        if gameState.jumpTime == 0:
            assert(gameState.camY == 0)
            break
        assert(i != 99)
    
    # Sliding
    gameState.keyboard(b's')
    assert(gameState.camY == -0.5)
    gameState.idle()
    assert(gameState.slideTime == 1)
    # Test that player moves back up after timer resets
    for i in range(100):
        gameState.idle()
        if gameState.slideTime == 0:
            assert(gameState.camY == 0)
            break
        assert(i != 99)

    # Test that player can't make illegal moves
    # X can be = -1, 0 or 1
    gameState.keyboard(b'a')
    gameState.keyboard(b'a')
    gameState.keyboard(b'a')
    assert(gameState.camX == 1)
    gameState.keyboard(b'd')
    gameState.keyboard(b'd')
    gameState.keyboard(b'd')
    assert(gameState.camX == -1)
    # Bring player to middle
    gameState.keyboard(b'a')
    # Y can be 0.5, 0 or -0.5
    gameState.keyboard(b'w')
    gameState.keyboard(b'w')
    gameState.keyboard(b'w')
    assert(gameState.camY == 0.5)
    # Player also cannot move in air
    gameState.keyboard(b'a')
    assert(gameState.camX == 0)
    gameState.keyboard(b'b')
    assert(gameState.camX == 0)
    # Bring player back down
    for i in range(100):
        gameState.idle()
    # Test same when sliding
    gameState.keyboard(b's')
    gameState.keyboard(b's')
    gameState.keyboard(b's')
    assert(gameState.camY == -0.5)
    # Player cant move when sliding
    gameState.keyboard(b'a')
    assert(gameState.camX == 0)
    gameState.keyboard(b'b')
    assert(gameState.camX == 0)
    # Bring player back to middle
    for i in range(100):
        gameState.idle()
    # Player should now be in the middle
    assert(gameState.camX == 0)
    assert(gameState.camY == 0)
    assert(gameState.camZ == 0)

# Test that idle function moves objects and registeres hits correctly
def testIdle(speed):
    gameState = gameStateObject(speed, test=True)
    gameState.load_stage("test")
    # Objects should move
    obstacles = gameState.stage.obstacles
    gameState.idle()
    for i in range(0, len(obstacles)):
        assert(obstacles[i].z == gameState.stage.obstacles[i].z - speed)

    # Player should be hit by the rectangle at x = 0
    startZ = obstacles[0].z
    # Steps until hit, minus one
    steps = int(startZ / speed) - 2
    for i in range(0, steps):
        gameState.idle()
        assert(gameState.gameLost == False)
    # Last step
    gameState.idle()
    assert(gameState.gameLost == True)
    
# Tests the obstacle.reshape function
def testReshape(shapes, dx, dy, dz):
    # Test reshaping from shapes[0] to shapes[1]
    obs = obstacle(shapes[0], 5)
    assert(obs.shapeType == shapes[0])
    assert(obs.z == 5)
    obs.reshape(shapes[1])
    assert(obs.dx == dx)
    assert(obs.dy == dy)
    assert(obs.dz == dz)

# Test moving the obstacle back from behind the player
def testMoveBack(shapes, zPositions, speed):
    obs = obstacle(shapes[0], zPositions[0])
    obs.moveBack(shapes[1], zPositions[1])
    assert(obs.shapeType == shapes[1])
    assert(obs.z == zPositions[1])
    # Simulate a game run and test if obstacle moves back
    gameState = gameStateObject(speed, test=True)
    gameState.load_stage("test")
    steps = int(gameState.stage.obstacles[0].z / speed) + 1
    # Get the z position of last obstacle, first obstacle should move to this position
    lastZ = gameState.stage.obstacles[-1].z
    # First obstacle is a rectangle at x = 0, dodge
    gameState.keyboard(b'a')
    # Move obstacle to behind player
    for i in range(0, steps):
        gameState.idle()
    # Check if obstacle moved back
    assert(gameState.stage.obstacles[0].z == lastZ)

# Test the obstacle.moveObstacle() method
def testMove(shape, z, speed):
    obs = obstacle(shape, z)
    obs.moveObstacle(speed)
    assert(obs.z == z - speed)

# Test moving all obstacles
def testMoveAll():
    bruh = 5

# Test relocating an object in the x-axis
def testRelocate():
    bruh = 5