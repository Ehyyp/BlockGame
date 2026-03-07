"""
Use pytest to test game_state.py and obstacle_classes.py
Graphics are not tested, as github actions does not allow
importing glut.
"""
import pytest
from game_state import GameStateClass
from obstacle_classes import Obstacle, ObstacleCourse

# Test cases
hit_test_cases = [
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
@pytest.mark.parametrize("actions, wait_times, speed", hit_test_cases)
def test_lose(actions, wait_times, speed):
    # Initialize game
    game_state = GameStateClass(speed, "test")
    # Execute all keystrokes or waits
    for i, action in enumerate(actions):
        # Idle for waitTime amount
        for _ in range(0, wait_times[i]):
            game_state.idle()

        # Move if a key was pressed
        if action != 0:
            game_state.keyboard(action)

        # Check that game was not won and was lost only after the last action
        if i != (len(actions) - 1):
            assert game_state.game_won is False
            assert game_state.game_lost is False
        else:
            assert game_state.game_won is False
            assert game_state.game_lost is True

win_test_cases = [
    ([b'd', 0, b'a', b'w', b's', 0], [80, 120, 80, 100, 100, 25], 0.05),
    ([b'a', b'd', 0, b'w', b's', 0], [80, 100, 120, 80, 100, 25], 0.05)
]
# Tests collision with obstacle
@pytest.mark.parametrize("actions, wait_times, speed", win_test_cases)
def test_win(actions, wait_times, speed):
    # Initialize game
    game_state = GameStateClass(speed, "test")
    # Execute all keystrokes or waits
    for i, action in enumerate(actions):
        # Idle for waitTime amount
        for _ in range(0, wait_times[i]):
            game_state.idle()

        # Move if a key was pressed
        if action != 0:
            game_state.keyboard(action)

        # Check that game was not lost and was won only after the last action
        if i != (len(actions) - 1):
            assert game_state.game_won is False
            assert game_state.game_lost is False
        else:
            assert game_state.game_won is True
            assert game_state.game_lost is False


load_test_cases = [
    ("test", ["lowBar", "highBar"], [], 0.02, 36, 36),
    ("stage1", ["highBar", "rectangle", "rectangle", "rectangle", "highBar",
                "highBar", "lowBar", "rectangle", "lowBar"], [1, 0, -1, 0],
                0.05, 50, 50),
    ("stage2", ["rectangle", "rectangle", "highBar", "lowBar", "rectangle",
                "highBar", "highBar"], [-1, 1, 0], 5, 100, 100)
]
# Test loading the different stages
@pytest.mark.parametrize("stage_name, stage, rec_position, speed, jump_reset," \
                         "slide_reset", load_test_cases)
def test_load(stage_name, stage, rec_position, speed, jump_reset, slide_reset):
    # pylint: disable=too-many-positional-arguments
    # pylint: disable=too-many-arguments
    # All arguments need to be tested

    # Initialize
    game_state = GameStateClass(speed, stage_name, jump_reset, slide_reset)
    # Test
    assert game_state.game_speed == speed
    assert game_state.jump_reset == jump_reset
    assert game_state.slide_reset == slide_reset
    assert game_state.stage.type_stack == stage
    assert game_state.stage.rec_x_positions == rec_position

# Test moving the player in x-axis
def test_wasd():
    # Initialize game with extremely low speed, so that no object hits when
    # testing keyboard functionality
    game_state = GameStateClass("0.00001", "test")
    # Check that initial position is correct
    assert game_state.cam_x == 0
    assert game_state.cam_y == 0
    assert game_state.cam_z == 0
    # Test that A and D keys move the player correctly
    game_state.keyboard(b'a')
    assert game_state.cam_x == 1
    game_state.keyboard(b'd')
    assert game_state.cam_x == 0
    game_state.keyboard(b'd')
    assert game_state.cam_x == -1
    game_state.keyboard(b'w')
    assert game_state.cam_y == 0.5

# Test jumping
jump_test_cases = [
    (36),
    (50),
    (100)
]
@pytest.mark.parametrize("jump_reset", jump_test_cases)
def test_jump(jump_reset):
    # Initialize game with extremely low speed, so that no object hits when
    # testing keyboard functionality
    game_state = GameStateClass("0.00001", "test", jump_reset=jump_reset)
    # Test that jumping moves player up
    game_state.keyboard(b'w')
    assert game_state.cam_y == 0.5
    # Test that jump timer grows
    game_state.idle()
    assert game_state.jump_time == 1
    # Test that player moves back to ground after jump timer resets
    for i in range(jump_reset):
        game_state.idle()
        if game_state.jump_time == 0:
            assert game_state.cam_y == 0
            break
        assert i != 99

# Test sliding
slide_test_cases = [
    (36),
    (50),
    (100)
]
@pytest.mark.parametrize("slide_reset", slide_test_cases)
def test_slide(slide_reset):
    # Initialize game with extremely low speed, so that no object hits when
    # testing keyboard functionality
    game_state = GameStateClass("0.00001", "test", slide_reset=slide_reset)
    # Test that sliding moves player down
    game_state.keyboard(b's')
    assert game_state.cam_y == -0.5
    # Test that slide timer grows
    game_state.idle()
    assert game_state.slide_time == 1
    # Test that player moves back up after slide timer resets
    for i in range(slide_reset):
        game_state.idle()
        if game_state.slide_time == 0:
            assert game_state.cam_y == 0
            break
        assert i != 99

# Test sliding
illegal_moves_test_cases = [
    (36, 36),
    (50, 10),
    (100, 100)
]
@pytest.mark.parametrize("jump_reset, slide_reset", illegal_moves_test_cases)
def test_illegal_moves(jump_reset, slide_reset):
    # Initialize game with extremely low speed, so that no object hits when
    # testing keyboard functionality
    game_state = GameStateClass("0.00001", "test", jump_reset, slide_reset)
    # Test that player can't make illegal moves
    # X can be = -1, 0 or 1
    game_state.keyboard(b'a')
    game_state.keyboard(b'a')
    game_state.keyboard(b'a')
    assert game_state.cam_x == 1
    game_state.keyboard(b'd')
    game_state.keyboard(b'd')
    game_state.keyboard(b'd')
    assert game_state.cam_x == -1
    # Bring player to middle
    game_state.keyboard(b'a')
    # Y can be 0.5, 0 or -0.5
    game_state.keyboard(b'w')
    game_state.idle()
    game_state.keyboard(b'w')
    game_state.idle()
    game_state.keyboard(b'w')
    game_state.idle()
    assert game_state.cam_y == 0.5
    # Player cannot move in air
    game_state.keyboard(b'a')
    assert game_state.cam_x == 0
    game_state.keyboard(b'b')
    assert game_state.cam_x == 0
    # Bring player back down
    for _ in range(jump_reset):
        game_state.idle()
    # Test same when sliding
    game_state.keyboard(b's')
    game_state.idle()
    game_state.keyboard(b's')
    game_state.idle()
    game_state.keyboard(b's')
    game_state.idle()
    assert game_state.cam_y == -0.5
    # Player cant move when sliding
    game_state.keyboard(b'a')
    assert game_state.cam_x == 0
    game_state.keyboard(b'b')
    assert game_state.cam_x == 0
    # Bring player back to middle
    for _ in range(slide_reset):
        game_state.idle()
    # Player should now be in the middle
    assert game_state.cam_x == 0
    assert game_state.cam_y == 0
    assert game_state.cam_z == 0

idle_test_cases = [
    (0.01),
    (0.02),
    (0.05)
]
# Test that idle function moves objects and registeres hits correctly
@pytest.mark.parametrize("speed", idle_test_cases)
def test_idle(speed):
    game_state = GameStateClass(speed, "test")
    # Test stage object starting positions where to compare object movement
    start_pos = [5, 10, 15]
    # Move objects by "speed" amount, once
    game_state.idle()
    for i, obstacle in enumerate(game_state.stage.obstacles):
        assert start_pos[i] == obstacle.z + speed

    # Player should be hit by the rectangle at x = 0
    start_z = 5
    # Steps until hit, must take into account the rounding of obstacle z
    # position when registering hits round(obs.z, 0) means that object
    # at z = 0.49 is considered hitting the player
    steps = int((start_z - 0.51) / speed)
    for i in range(0, steps):
        game_state.idle()
        assert game_state.game_lost is False
    # Last step
    game_state.idle()
    assert game_state.game_lost is True

reshape_test_cases = [
    (["rectangle", "lowBar"], 3, 0.8, -0.6),
    (["highBar", "lowBar"], 3, 0.8, -0.6),
    (["lowBar", "lowBar"], 3, 0.8, -0.6),
    (["rectangle", "highBar"], 3, 0.8, 0.3),
    (["lowBar", "highBar"], 3, 0.8, 0.3),
    (["highBar", "highBar"], 3, 0.8, 0.3),
    (["lowBar", "rectangle"], 1, 3, 0),
    (["highBar", "rectangle"], 1, 3, 0),
    (["highBar", "rectangle"], 1, 3, 0),
    (["highBar", "notARealShape"], 0, 0, 0),
    (["rectangle", "thisIsNotAShape"], 0, 0, 0),
    (["lowBar", "notValid"], 0, 0, 0)
]
# Tests the obstacle.reshape function
@pytest.mark.parametrize("shapes, dx, dy, y", reshape_test_cases)
def test_reshape(shapes, dx, dy, y):
    # Test reshaping from shapes[0] to shapes[1]
    obs = Obstacle(shapes[0], 5)
    assert obs.shape_type == shapes[0]
    assert obs.z == 5
    # If the next shape is not defined, reshape should raise ValueError
    if (shapes[1] != "rectangle") and (shapes[1] != "lowBar") and (shapes[1] != "highBar"):
        with pytest.raises(ValueError):
            obs.reshape(shapes[1])
    # Otherwise dimensions and y location should change
    else:
        obs.reshape(shapes[1])
        assert obs.dx == dx
        assert obs.dy == dy
        assert obs.y == y

move_back_test_cases = [
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
@pytest.mark.parametrize("shapes, z_positions, speed", move_back_test_cases)
def test_move_back(shapes, z_positions, speed):
    obs = Obstacle(shapes[0], z_positions[0])
    obs.move_back(shapes[1], z_positions[1])
    assert obs.shape_type == shapes[1]
    assert obs.z == z_positions[1]
    # Simulate a game run and test if obstacle moves back
    game_state = GameStateClass(speed, "test")
    steps = int(game_state.stage.obstacles[0].z / speed) + 1
    # Get the z position of last obstacle, first obstacle should move to this position
    last_z = game_state.stage.obstacles[-1].z
    # First obstacle is a rectangle at x = 0, dodge
    game_state.keyboard(b'a')
    # Move obstacle to behind player
    for _ in range(0, steps):
        game_state.idle()
    # Check if obstacle moved back
    assert game_state.stage.obstacles[0].z == last_z

move_test_cases = [
    ("rectangle", 5, 0.01),
    ("lowBar", 3, 0.02),
    ("highBar", 10, 0.1)
]
# Test the obstacle.moveobstacle() method
@pytest.mark.parametrize("shape, z, speed", move_test_cases)
def test_move(shape, z, speed):
    obs = Obstacle(shape, z)
    obs.move_obstacle(speed)
    assert obs.z == z - speed

move_all_test_cases = [
    (3, ["rectangle", "rectangle", "rectangle", "lowBar", "highBar"], [0, 1, -1], 0.02),
    (4, ["lowBar", "rectangle", "highBar", "highBar", "rectangle", "rectangle", "rectangle",
         "highBar", "highBar", "lowBar", "rectangle", "lowBar"], [0, 1, 0, -1, 0], 0.03),
    (5, ["highBar", "highBar", "rectangle", "rectangle", "rectangle", "highBar", "lowBar",
         "rectangle", "highBar", "highBar"], [0, -1, 1, 0], 0.05)
]
# Test moving all obstacles
@pytest.mark.parametrize("n_obs, obstacle_types, rec_x_positions, speed", move_all_test_cases)
def test_move_all(n_obs, obstacle_types, rec_x_positions, speed):
    # Initialize test
    course = ObstacleCourse(n_obs, obstacle_types, rec_x_positions)
    # Starting positions of all obs, which are by default placed 5 distance units apart
    # start = 5, step = 5, exclusive end = (n_obs + 1) * 5 => end = n_obs * 5
    obs_start = range(5, (n_obs + 1) * 5, 5)
    # Move all obs
    course.move_all_obs(speed)
    # Check that all obs moved
    for i in range(0, n_obs):
        assert obs_start[i] != course.obstacles[i].z

relocate_test_cases = [
    (3, ["lowBar", "lowBar", "lowBar"], []),
    (5, ["rectangle", "highBar", "lowBar", "rectangle", "lowBar", "highBar", "rectangle",
         "lowBar", "rectangle", "highBar"], [1, 0, -1, 0]),
    (1, ["rectangle", "rectangle", "rectangle"], [-1, -1, -1]),
    (3, ["rectangle", "rectangle", "rectangle"], [-1, -1, -1]),
]
# Test relocating an object in the x-axis
@pytest.mark.parametrize("n_obs, obstacle_types, rec_x_positions", relocate_test_cases)
def test_relocate(n_obs, obstacle_types, rec_x_positions):
    course = ObstacleCourse(n_obs, obstacle_types, rec_x_positions)
    # Initializing ObstacleCourse already relocates rectangles, so all of the rectangles in
    # the starting screen will reduce the number of elements in rec_x_positions by one.
    # Therefore if we relocate outside of the game, we need to make sure that the
    # ObstacleCourse has enough rectangle positions, otherwise we will be trying to pop from
    # an empty array. This can be done by having no rectangles in the first n_obs of shapes
    for obs in course.obstacles:
        # If obstacle is a rectangle, relocate and check that it got the correct position
        # from rec_x_positions
        if obs.shape_type == "rectangle":
            # If all positions are used and rectangle is relocated, relocating should raise
            # ValueError
            if len(course.rec_x_positions) == 0:
                with pytest.raises(ValueError):
                    course.relocate(obs)
            else:
                # Save correct x location of relocated before it is popped from the array
                x_correct = course.rec_x_positions[0]
                course.relocate(obs)
                assert obs.x == x_correct
        # If obstacle is not a rectangle, it should get x = 0
        else:
            course.relocate(obs)
            assert obs.x == 0
