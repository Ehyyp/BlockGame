from gameState import gameStateClass
from obstacleClasses import obstacle, obstacleCourse
import pytest

# Test cases
hitTestCases = [
    ([0, 0, 0, 0, 0], "rectangle", 1),
    ([b'a', 0, 0, 0, 0], "rectangle", 2),
    ([b'd', 0, 0, 0, 0], "rectangle", 3),
    ([b'd', 0, b'a', 0, 0], "lowBar", 4),
    ([b'd', 0, b'a', 0, b'd'], "lowBar", 4),
    ([b'd', 0, b'a', b'w', 0], "lowBar", 5),
    ([b'd', 0, b'a', b'w', b'w'], "lowBar", 5),
]
# Tests collision with obstacle
@pytest.mark.parametrize("actions, obstacleType, speed", hitTestCases)
def testHit(actions, obstacleType, speed):
    # Initialize game
    gameState = gameStateClass(speed, "test")
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
        win = int(gameState.stage.moveAllObs(speed))
        winList.append(win)
        # Check if player collided with obstacle
        hit = gameState.stage.checkHit(gameState.camX, gameState.camY)
        hitList.append(hit)

    # Game should not be won in these tests
    assert(winList.count(0) == 0)
    # Check that only the last action resulted in a hit, i.e. everything else was False
    for i in range(0, len(hitList) - 1):
        assert(hitList[i][0] == False)
    assert(hitList[-1][0] == True)
    # Check that the hit obstacle was of correct type
    assert(hitList[-1][1] == obstacleType)

winTestCases = [
    ([b'd', 0, b'a', b'w', b'w'], 5),
    ([b'a', b'd', 0, b'w', b's'], 5)
]
# Tests collision with obstacle
@pytest.mark.parametrize("actions, speed", winTestCases)
def testWin(actions, speed):
    # Initialize game
    gameState = gameStateClass(speed, "test")
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
    for hit in hitList:
        assert(hit[0] == False)
    # Check that only the last action resulted in a win
    assert(winList[-1] == 0)
    assert(winList.contains(1) == 0)

loadTestCases = [
    ("test", ["rectangle", "rectangle", "rectangle", "lowBar", "highBar"], [0, 1, -1]),
    ("stage1", ["lowBar", "rectangle", "highBar", "highBar", "rectangle", "rectangle", "rectangle", "highBar", "highBar", "lowBar", "rectangle", "lowBar"], [0, 1, 0, -1, 0, -1]),
    ("stage2", ["highBar", "highBar", "rectangle", "rectangle", "rectangle", "highBar", "lowBar", "rectangle", "highBar", "highBar"], [0, -1, 1, 0])
]
# Test loading the different stages
@pytest.mark.parametrize("stageName, stage, recPosition", loadTestCases)
def testLoad(stageName, stage, recPosition):
    # Initialize
    gameState = gameStateClass("0.5", stageName)
    # Test
    assert(gameState.obstacleTypes == stage)
    assert(gameState.recXPositions == recPosition)

# Test the keyboard functionality
def testKeyboard():
    # Initialize game with extremely low speed, so that no object hits when testing keyboard functionality
    gameState = gameStateClass("0.00001", "test")
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

idleTestCases = [
    (0.01),
    (0.02),
    (0.05)
]
# Test that idle function moves objects and registeres hits correctly
@pytest.mark.parametrize("speed", idleTestCases)
def testIdle(speed):
    gameState = gameStateClass(speed, "test")
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
    
reshapeTestCases = [
    (["rectangle", "lowBar"], 3, 0.8, -0.6),
    (["highBar", "lowBar"], 3, 0.8, -0.6),
    (["rectangle", "highBar"], 3, 0.8, 0.3),
    (["lowBar", "highBar"], 3, 0.8, 0.3),
    (["lowBar", "rectangle"], 1, 3, 0),
    (["highBar", "rectangle"], 1, 3, 0),
]
# Tests the obstacle.reshape function
@pytest.mark.parametrize("shapes, dx, dy, y", reshapeTestCases)
def testReshape(shapes, dx, dy, y):
    # Test reshaping from shapes[0] to shapes[1]
    obs = obstacle(shapes[0], 5)
    assert(obs.shapeType == shapes[0])
    assert(obs.z == 5)
    obs.reshape(shapes[1])
    assert(obs.dx == dx)
    assert(obs.dy == dy)
    assert(obs.y == y)

moveBackTestCases = [
    (["rectangle", "rectangle"], [-1, 15], 0.02),
    (["rectangle", "highBar"], [-1, 15], 0.02),
    (["rectangle", "lowBar"], [-1, 15], 0.02),
    (["lowBar", "rectangle"], [-1, 15], 0.02),
    (["lowBar", "highBar"], [-1, 15], 0.02),
    (["lowBar", "lowBar"], [-1, 15], 0.02),
    (["highBar", "rectangle"], [-1, 15], 0.02),
    (["highBar", "highBar"], [-1, 15], 0.02),
    (["highBar", "lowBar"], [-1, 15], 0.02),
]
# Test moving the obstacle back from behind the player
@pytest.mark.parametrize("shapes, zPositions, speed", moveBackTestCases)
def testMoveBack(shapes, zPositions, speed):
    obs = obstacle(shapes[0], zPositions[0])
    obs.moveBack(shapes[1], zPositions[1])
    assert(obs.shapeType == shapes[1])
    assert(obs.z == zPositions[1])
    # Simulate a game run and test if obstacle moves back
    gameState = gameStateClass(speed, test=True)
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

moveTestCases = [
    ("rectangle", 5, 0.01),
    ("lowBar", 3, 0.02),
    ("highBar", 10, 0.1)
]
# Test the obstacle.moveObstacle() method
@pytest.mark.parametrize("shape, z, speed", moveTestCases)
def testMove(shape, z, speed):
    obs = obstacle(shape, z)
    obs.moveObstacle(speed)
    assert(obs.z == z - speed)

moveAllTestCases = [
    (3, ["rectangle", "rectangle", "rectangle", "lowBar", "highBar"], [0, 1, -1], 0.02),
    (3, ["lowBar", "rectangle", "highBar", "highBar", "rectangle", "rectangle", "rectangle", "highBar", "highBar", "lowBar", "rectangle", "lowBar"], [0, 1, 0, -1, 0, -1], 0.03),
    (3, ["highBar", "highBar", "rectangle", "rectangle", "rectangle", "highBar", "lowBar", "rectangle", "highBar", "highBar"], [0, -1, 1, 0], 0.05)
]
# Test moving all obstacles
@pytest.mark.parametrize("nObs, obstacleTypes, recXPositions, speed", moveAllTestCases)
def testMoveAll(nObs, obstacleTypes, recXPositions, speed):
    # Initialize test
    course = obstacleCourse(nObs, obstacleTypes, recXPositions, test=True)
    # Get positions of all obs
    obs = course.obstacles
    # Move all obs
    course.moveAllObs(speed)
    # Check that all obs moved
    for i in range(0, len(obs)):
        assert(obs[i].z != course.obstacles[i].z)

relocateTestCases = [
    (3, ["rectangle", "rectangle", "rectangle", "lowBar", "highBar"], [0, 1, -1]),
    (3, ["lowBar", "rectangle", "highBar", "highBar", "rectangle", "rectangle", "rectangle", "highBar", "highBar", "lowBar", "rectangle", "lowBar"], [0, 1, 0, -1, 0, -1]),
    (3, ["highBar", "highBar", "rectangle", "rectangle", "rectangle", "highBar", "lowBar", "rectangle", "highBar", "highBar"], [0, -1, 1, 0])
]
# Test relocating an object in the x-axis
@pytest.mark.parametrize("nObs, obstacleTypes, recXPositions", relocateTestCases)
def testRelocate(nObs, obstacleTypes, recXPositions):
    course = obstacleCourse(nObs, obstacleTypes, recXPositions, test=True)
    # Relocate all obstacles
    i = 0
    for obs in course.obstacles:
        course.relocate(obs)
        # If obstacle was a rectangle, check that it got the correct position from recXPositions
        if obs.shapeType == "rectangle":
            assert(obs.x == recXPositions[i])
            i += 1
        # If obstacle was not a rectangle, it should have x = 0
        else:
            assert(obs.x == 0)  
 