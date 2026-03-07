from gameState import gameStateClass
from obstacleClasses import obstacle, obstacleCourse
import pytest

# Test cases
hitTestCases = [
    ([0], [250], 0.02),
    ([0, 0, 0, 0, 0], [100, 100, 100, 100, 100], 0.01),
    ([b'a', 0, 0, 0, 0], [200, 200, 200, 200, 200], 0.01),
    ([b'd', 0, 0], [100, 100, 300], 0.03),
    ([b'd', 0, 0, 0, 0], [300, 300, 300, 300, 300], 0.01),
    ([b'd', 0, b'a', 0, 0], [400, 400, 400, 400, 400], 0.01),
    ([b'd', 0, b'a', 0, b'd'], [400, 400, 400, 400, 400], 0.01),
    ([b'd', 0, b'a', b'w', 0], [80, 120, 80, 100, 120], 0.05),
    ([b'd', 0, b'a', b'w', b'w'], [80, 120, 80, 100, 120], 0.05),
]
# Tests collision with obstacle
@pytest.mark.parametrize("actions, waitTimes, speed", hitTestCases)
def test_Lose(actions, waitTimes, speed):
    # Initialize game
    gameState = gameStateClass(speed, "test")
    # Execute all keystrokes or waits
    for i in range(0,len(actions)):
        # Idle for waitTime amount
        for j in range(0, waitTimes[i]):
            gameState.idle()

        # Move if a key was pressed
        if actions[i] != 0:
            gameState.keyboard(actions[i])

        # Check that game was not won and was lost only after the last action
        if i != (len(actions) - 1):
            assert(gameState.gameWon == False)
            assert(gameState.gameLost == False)
        else:
            assert(gameState.gameWon == False)
            assert(gameState.gameLost == True)

winTestCases = [
    ([b'd', 0, b'a', b'w', b's', 0], [80, 120, 80, 100, 100, 25], 0.05),
    ([b'a', b'd', 0, b'w', b's', 0], [80, 100, 120, 80, 100, 25], 0.05)
]
# Tests collision with obstacle
@pytest.mark.parametrize("actions, waitTimes, speed", winTestCases)
def test_Win(actions, waitTimes, speed):
    # Initialize game
    gameState = gameStateClass(speed, "test")
    # Execute all keystrokes or waits
    for i in range(0,len(actions)):
        # Idle for waitTime amount
        for j in range(0, waitTimes[i]):
            gameState.idle()

        # Move if a key was pressed
        if actions[i] != 0:
            gameState.keyboard(actions[i])

        # Check that game was not lost and was won only after the last action
        if i != (len(actions) - 1):
            assert(gameState.gameWon == False)
            assert(gameState.gameLost == False)
        else:
            assert(gameState.gameWon == True)
            assert(gameState.gameLost == False)


loadTestCases = [
    ("test", ["lowBar", "highBar"], []),
    ("stage1", ["highBar", "rectangle", "rectangle", "rectangle", "highBar", "highBar", "lowBar", "rectangle", "lowBar"], [1, 0, -1, 0]),
    ("stage2", ["rectangle", "rectangle", "highBar", "lowBar", "rectangle", "highBar", "highBar"], [-1, 1, 0])
]
# Test loading the different stages
@pytest.mark.parametrize("stageName, stage, recPosition", loadTestCases)
def test_Load(stageName, stage, recPosition):
    # Initialize
    gameState = gameStateClass("0.5", stageName)
    # Test
    assert(gameState.obstacleTypes == stage)
    assert(gameState.recXPositions == recPosition)

# Test the keyboard functionality
def test_Keyboard():
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
    gameState.idle()
    gameState.keyboard(b'w')
    gameState.idle()
    gameState.keyboard(b'w')
    gameState.idle()
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
    gameState.idle()
    gameState.keyboard(b's')
    gameState.idle()
    gameState.keyboard(b's')
    gameState.idle()
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
def test_Idle(speed):
    gameState = gameStateClass(speed, "test")
    # Test stage object starting positions where to compare object movement
    startPos = [5, 10, 15]
    # Move objects by "speed" amount, once
    gameState.idle()
    for i in range(0, len(gameState.stage.obstacles)):
        assert(startPos[i] == gameState.stage.obstacles[i].z + speed)

    # Player should be hit by the rectangle at x = 0
    startZ = 5
    # Steps until hit, must take into account the rounding of obstacle z position when registering hits
    # round(obs.z, 0) means that object at z = 0.49 is considered hitting the player
    steps = int((startZ - 0.51) / speed)
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
def test_Reshape(shapes, dx, dy, y):
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
def test_MoveBack(shapes, zPositions, speed):
    obs = obstacle(shapes[0], zPositions[0])
    obs.moveBack(shapes[1], zPositions[1])
    assert(obs.shapeType == shapes[1])
    assert(obs.z == zPositions[1])
    # Simulate a game run and test if obstacle moves back
    gameState = gameStateClass(speed, "test")
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
def test_Move(shape, z, speed):
    obs = obstacle(shape, z)
    obs.moveObstacle(speed)
    assert(obs.z == z - speed)

moveAllTestCases = [
    (3, ["rectangle", "rectangle", "rectangle", "lowBar", "highBar"], [0, 1, -1], 0.02),
    (4, ["lowBar", "rectangle", "highBar", "highBar", "rectangle", "rectangle", "rectangle", "highBar", "highBar", "lowBar", "rectangle", "lowBar"], [0, 1, 0, -1, 0], 0.03),
    (5, ["highBar", "highBar", "rectangle", "rectangle", "rectangle", "highBar", "lowBar", "rectangle", "highBar", "highBar"], [0, -1, 1, 0], 0.05)
]
# Test moving all obstacles
@pytest.mark.parametrize("nObs, obstacleTypes, recXPositions, speed", moveAllTestCases)
def test_MoveAll(nObs, obstacleTypes, recXPositions, speed):
    # Initialize test
    course = obstacleCourse(nObs, obstacleTypes, recXPositions)
    # Starting positions of all obs, which are by default placed 5 distance units apart
    # start = 5, step = 5, exclusive end = (nObs + 1) * 5 => end = nObs * 5
    obsStart = range(5, (nObs + 1) * 5, 5)
    # Move all obs
    course.moveAllObs(speed)
    # Check that all obs moved
    for i in range(0, nObs):
        assert(obsStart[i] != course.obstacles[i].z)

relocateTestCases = [
    (3, ["lowBar", "lowBar", "lowBar", "rectangle", "rectangle", "rectangle"], [0, 1, -1]),
    (3, ["lowBar", "lowBar", "highBar", "highBar", "rectangle", "rectangle", "rectangle", "highBar", "highBar", "lowBar", "rectangle", "lowBar"], [1, 0, -1, 0]),
    (3, ["highBar", "highBar", "highBar", "rectangle", "rectangle", "highBar", "lowBar", "rectangle", "highBar", "highBar"], [-1, 1, 0])
]
# Test relocating an object in the x-axis
@pytest.mark.parametrize("nObs, obstacleTypes, recXPositions", relocateTestCases)
def test_Relocate(nObs, obstacleTypes, recXPositions):
    # Copy the rectangle x positions list, since it is mutated within the class
    inputRecXPos = recXPositions.copy()
    oldRecXPos = recXPositions.copy()
    course = obstacleCourse(nObs, obstacleTypes, inputRecXPos)
    # Relocate all obstacles
    i = 0
    # Initializing obstacleCourse already relocates rectangles, so all of the rectangles in the starting screen will reduce the number of elements in recXPositions by one
    # Therefore if we relocate outside of the game, we need to make sure that the obstacleCourse has enough rectangle positions, otherwise we will be trying to pop from
    # an empty array. This can be done by having no rectangles in the first nObs of shapes
    for obs in course.obstacles:
        course.relocate(obs)
        # If obstacle was a rectangle, check that it got the correct position from recXPositions
        if obs.shapeType == "rectangle":
            assert(obs.x == oldRecXPos[i])
            i += 1
        # If obstacle was not a rectangle, it should have x = 0
        else:
            assert(obs.x == 0)  
 