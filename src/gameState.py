# Import obstacle class
from obstacleClasses import obstacleCourse

# This holds the game state data and methods that need to access that data
class gameStateClass:

    # For ending the game
    gameLost = False
    gameWon = False

    # Holds the camera position data
    camX = 0.0
    camY = 0.0
    camZ = 0.0

    # Times the jump and slide
    jumpTime = 0
    slideTime = 0

    # Holds the game speed data
    gameSpeed = 0.02

    # Number of obstacles in world
    nObs = 3

    # Initialize course stack
    # Defines the obstacle course
    obstacleTypes = []

    # Initialize rectangle locations stack
    # Defines the rectangle obstacles x-axis positions
    # Bars will always be in the same position
    recXPositions = []

    # Defines current stage name
    stageName = None

    # Defines obstacle behaviour
    stage = None

    # Set speed and testing at construction
    def __init__(self, speed, stageName):
        self.gameSpeed = float(speed)
        self.stageName = stageName
        # Load stage
        self.load_stage()

    # Initializes the stage data
    def load_stage(self):
        if self.stageName == "stage1":
            # Defines the obstacle course
            self.obstacleTypes = ["lowBar", "rectangle", "highBar", "highBar", "rectangle", "rectangle", "rectangle", "highBar", "highBar", "lowBar", "rectangle", "lowBar"]
            # Defines the rectangle starting positions
            self.recXPositions = [0, 1, 0, -1, 0]
        elif self.stageName == "stage2":
            self.obstacleTypes = ["highBar", "highBar", "rectangle", "rectangle", "rectangle", "highBar", "lowBar", "rectangle", "highBar", "highBar"]
            self.recXPositions = [0, -1, 1, 0]
        # Testing stage
        elif self.stageName == "test":
            self.obstacleTypes = ["rectangle", "rectangle", "rectangle", "lowBar", "highBar"]
            self.recXPositions = [0, 1, -1]
        # Choose from two stages
        
        # Set up the obstacle course
        self.stage = obstacleCourse(self.nObs, self.obstacleTypes, self.recXPositions)

    # Defines keyboard input
    # WASD controls
    # The x and y parameters determine the mouse location when key is pressed and are required by the glutKeyboardFunc
    def keyboard(self, key):
        # Can't move in the air or when sliding
        if self.jumpTime == 0 and self.slideTime == 0:
            # W = up
            if key == b'w':
                if self.camY != 0.5:
                    self.camY += 0.5
            # A = left
            if key == b'a':
                if self.camX != 1:
                    self.camX += 1
            # S = down
            if key == b's':
                if self.camY != -0.5:
                    self.camY -= 0.5
            # D = right
            if key == b'd':
                if self.camX != -1:
                    self.camX -= 1

    # Defines what happens at idle, i.e. update obstacles and refresh display
    def idle(self):
        # If player in air
        if self.camY == 0.5:
            # And jump time ended
            if self.jumpTime == 36:
                # Bring to ground and reset timer
                self.camY = 0
                self.jumpTime = 0
            # If not, increment jump timer
            else:
                self.jumpTime += 1

        # If player sliding
        if self.camY == -0.5:
            # And slide time ended
            if self.slideTime == 36:
                # Bring to standing and reset timer
                self.camY = 0
                self.slideTime = 0
            # If not, increment slide timer
            else:
                self.slideTime += 1

        # Move obstacles and check if game was won
        self.gameWon = self.stage.moveAllObs(self.gameSpeed)

        # Check if player hit an obstacle and if game was lost
        self.gameLost = self.stage.checkHit(self.camX, self.camY)[0]
