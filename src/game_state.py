"""
gameState.py module defines the gameStateClass, which holds game
data, such as if the game was lost or won and player position.

It also defines methods for manipulating the game state, i.e.
loading a stage and idle and keyboard functions.
"""
# Import obstacle class
from obstacle_classes import ObstacleCourse

class GameStateClass:
    """
    Holds game data and defines methods to manipulate the game state.
    """

    # pylint: disable=too-many-instance-attributes
    # All attributes are reasonable

    # For ending the game
    game_lost = False
    game_won = False

    # Holds the camera position data
    cam_x = 0.0
    cam_y = 0.0
    cam_z = 0.0

    # Defines max air and sliding times
    jump_reset = 36
    slide_reset = 36

    # Times the jump and slide
    jump_time = 0
    slide_time = 0

    # Holds the game speed data
    game_speed = 0.02

    # Number of obstacles
    n_obs = 3

    # Defines obstacle behaviour
    stage = None

    # Set speed and testing at construction
    # If jump and slide reset times are given, set them as well
    def __init__(self, speed, stage_name, jump_reset=None, slide_reset=None):
        self.game_speed = float(speed)
        # Set jump and slide reset times if given
        if (jump_reset is not None) and (slide_reset is not None):
            self.jump_reset = jump_reset
            self.slide_reset = slide_reset
        # Load stage with given name and number of obstacles
        self.load_stage(stage_name)

    def load_stage(self, stage_name):
        """
        Initialize the stage object by defining the shape types that the obstacles
        will have through the game and the rectangle x-axis positions
        """
        # Initialize obstacle and rectangle position lists
        obstacle_types = None
        rec_x_positions = None

        if stage_name == "stage1":
            # Defines the obstacle course
            obstacle_types = ["lowBar", "rectangle", "highBar", "highBar", "rectangle",
                                  "rectangle", "rectangle", "highBar", "highBar", "lowBar",
                                  "rectangle", "lowBar"]
            # Defines the rectangle starting positions
            rec_x_positions = [0, 1, 0, -1, 0]
        elif stage_name == "stage2":
            obstacle_types = ["highBar", "highBar", "rectangle", "rectangle", "rectangle",
                                  "highBar", "lowBar", "rectangle", "highBar", "highBar"]
            rec_x_positions = [0, -1, 1, 0]
        # Testing stage
        elif stage_name == "test":
            obstacle_types = ["rectangle", "rectangle", "rectangle", "lowBar", "highBar"]
            rec_x_positions = [0, 1, -1]
        # Choose from two stages

        # Set up the obstacle course
        self.stage = ObstacleCourse(self.n_obs, obstacle_types, rec_x_positions)

    def keyboard(self, key):
        """
        Defines keyboard input used by GLUT.
        WASD controls
        """
        # Can't move in the air or when sliding
        if self.jump_time == 0 and self.slide_time == 0:
            # W = up
            if key == b'w':
                if self.cam_y != 0.5:
                    self.cam_y += 0.5
            # A = left
            if key == b'a':
                if self.cam_x != 1:
                    self.cam_x += 1
            # S = down
            if key == b's':
                if self.cam_y != -0.5:
                    self.cam_y -= 0.5
            # D = right
            if key == b'd':
                if self.cam_x != -1:
                    self.cam_x -= 1

    def idle(self):
        """
        Defines what happens at idle, i.e. move player back to y = 0 if
        jump or slide timers have run out, move obstacle and check if
        player hit an obstacle
        """
        # If player in air
        if self.cam_y == 0.5:
            # And jump time ended
            if self.jump_time == self.jump_reset:
                # Bring to ground and reset timer
                self.cam_y = 0
                self.jump_time = 0
            # If not, increment jump timer
            else:
                self.jump_time += 1

        # If player sliding
        if self.cam_y == -0.5:
            # And slide time ended
            if self.slide_time == self.slide_reset:
                # Bring to standing and reset timer
                self.cam_y = 0
                self.slide_time = 0
            # If not, increment slide timer
            else:
                self.slide_time += 1

        # Move obstacles and check if game was won
        self.game_won = self.stage.move_all_obs(self.game_speed)

        # Check if player hit an obstacle and if game was lost
        self.game_lost = self.stage.check_hit(self.cam_x, self.cam_y)
