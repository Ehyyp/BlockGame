from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

# This is used to handle the obstacle data
# This includes the position and shape of the obstacle
class obstacle:
    # Dimensions
    x = None
    y = None
    z = None
    # Shape
    dx = None
    dy = None
    dz = 0.1
    # shapeType, which is square or bar
    shapeType = None

    # Constructs the obstacle with specified type
    def __init__(self, shapeType, z):
        # y coordinate is based on the type of obstacle
        if shapeType == "rectangle":
            self.y = 0
        elif shapeType == "lowBar":
            self.y = -0.6
        elif shapeType == "highBar":
            self.y = 0.3
        
        # x position for bars is always 0, for rectangles it is determined in the obstacleCourse class
        self.x = 0
        # z start position given
        self.z = z

        # Reshape the obstacle to correct type
        self.shapeType = shapeType
        self.reshape(shapeType)

    # Reshapes the object
    def reshape(self, shape):
        # Reshaping changes the dimensions and y position,
        # as y position is dependent only on the obstacles shape type
        if shape == "rectangle":
            self.dx = 1
            self.dy = 3
            self.y = 0
        elif shape == "lowBar":
            self.dx = 3
            self.dy = 0.8
            self.y = -0.6
        elif shape == "highBar":
            self.dx = 3
            self.dy = 0.8
            self.y = 0.3
        else:
            raise ValueError("Expected types are rectangle, lowBar and highBar!")

    # Move the obstacle back to start
    # shapeType specifies new shape for object
    def moveBack(self, shapeType, zPos):
        # Move to start
        self.z = zPos
        # Update shape type
        self.shapeType = shapeType
        # Change shape
        self.reshape(self.shapeType)
    
    # Uses OpenGL to draw the obstacle
    def drawObstacle(self):
        # Push new matrix
        glPushMatrix()
        # Move to obstacle start
        glTranslatef(self.x, self.y, self.z)
        # Set color to red
        glColor3f(255, 0, 0)
        # Draw with dimensions
        drawBox(self.dx, self.dy, self.dz)
        # Set color back to white
        glColor3f(1, 1, 1)
        # Pop matrix
        glPopMatrix()

    # Move object in z-axis by "speed" amount
    def moveObstacle(self, speed):
        self.z -= speed


# Controls all of the obstacles
class obstacleCourse:
    # Holds all the obstacle objects and their shape type stacks
    # shape type stack is a stack that determines the obstacles shape type through the game
    # recXPositions holds the rectangle obstacles starting x positions
    obstacles = []
    typeStack = []
    recXPositions = []

    # Initialize obstacles list with number of obstacles and the obstacle shape types stack
    def __init__(self, numObstacles, obstacleTypes, recXPositions):
        self.recXPositions = recXPositions
        # Defines first obstacles starting position
        startPos = 5
        # Initialize each obstacle
        for i in range(0, numObstacles):
            # Get first type of obstacle
            shapeType = obstacleTypes.pop(0)
            # Add to list
            self.obstacles.append(obstacle(shapeType, startPos))
            # If the obstacle is a rectangle, determine its x-position from the stack
            self.relocate(self.obstacles[i])
            # Change starting position
            startPos += 5
        # Save the remainder of initial obstacle types stack
        self.typeStack = obstacleTypes

    # Moves all obstacles and checks their positions
    def moveAllObs(self, speed):
        # If obstacle list not empty
        if len(self.obstacles) != 0:
            # For each object
            for obs in self.obstacles:
                # Move forward
                obs.moveObstacle(speed)
                # If behind player
                if obs.z < 0:
                    # If stack is empty
                    if len(self.typeStack) == 0:
                        # Remove obstacle
                        self.obstacles.remove(obs)
                    # If not
                    else:
                        # z position based on number of obstacles
                        zpos = len(self.obstacles) * 5
                        # Move back and change shape
                        shapeType = self.typeStack.pop(0)
                        obs.moveBack(shapeType, zpos)
                        # Move the object in x-axis, if shape type changed to or from rectangle
                        self.relocate(obs)
        # If list is empty, game won
        else:
            # Terminate
            print("You win!")
            glutDestroyWindow(glutGetWindow())
            sys.exit()

    # Draw each obstacle
    def drawAllObs(self):
        # For each object
        for obs in self.obstacles:
            # Draw
            obs.drawObstacle()

    # Relocates an obstacle in the x-axis
    def relocate(self, obstacle):
        # It the object is a rectangle, change to xPos
        if obstacle.shapeType == "rectangle":
            # Check if the stack is empty
            if len(self.recXPositions) == 0:
                raise ValueError("Rectangle positions stack does not have the correct amount of positions!")
            else:
                obstacle.x = self.recXPositions.pop(0)
        # Otherwise move to middle
        else:
            obstacle.x = 0

    # Check if obstacle hit player
    def checkHit(self, cameraPos):
        # For each obstacle
        for obs in self.obstacles:
            # If obstacle has same x coordinate as camera at z = 0
            if round(obs.z, 0) == 0:
                # If obstacle is a rectangle, x needs to be checked
                if obs.shapeType == "rectangle":
                    if obs.x == cameraPos['x']:
                        # Terminate
                        print("You lost :(")
                        glutDestroyWindow(glutGetWindow())
                        sys.exit()
                # If obstacle is a bar, y needs to be checked
                # high bar hits when y is 0 or 0.5
                elif obs.shapeType == "highBar":
                    if cameraPos['y'] != -0.5:
                        # Terminate
                        print("You lost :(")
                        glutDestroyWindow(glutGetWindow())
                        sys.exit()
                # low bar hits when y is 0 or -0.5
                elif obs.shapeType == "lowBar":
                    if cameraPos['y'] != 0.5:
                        # Terminate
                        print("You lost :(")
                        glutDestroyWindow(glutGetWindow())
                        sys.exit()

# Draws an OpenGL box
def drawBox(width, height, depth):
    # Start specifying the quadilateral
    glBegin(GL_QUADS)
    # Specify normal for the quadilateral, x, y, z
    glNormal3f(0, 0, 1)
    # Specify four vertices of the rectangle in the front
    glVertex3f(-width/2, -height/2, depth/2)
    glVertex3f(width/2, -height/2, depth/2)
    glVertex3f(width/2, height/2, depth/2)
    glVertex3f(-width/2, height/2, depth/2)
    # The back
    glNormal3f(0, 0, -1)
    glVertex3f(-width/2, -height/2, -depth/2)
    glVertex3f(width/2, -height/2, -depth/2)
    glVertex3f(width/2, height/2, -depth/2)
    glVertex3f(-width/2, height/2, -depth/2)
    # Right side
    glNormal3f(1, 0, 0)
    glVertex3f(width/2, -height/2, -depth/2)
    glVertex3f(width/2, -height/2, depth/2)
    glVertex3f(width/2, height/2, depth/2)
    glVertex3f(width/2, height/2, -depth/2)
    # Left side
    glNormal3f(-1, 0, 0)
    glVertex3f(-width/2, -height/2, -depth/2)
    glVertex3f(-width/2, -height/2, depth/2)
    glVertex3f(-width/2, height/2, depth/2)
    glVertex3f(-width/2, height/2, -depth/2)
    # Top
    glNormal3f(0, 1, 0)
    glVertex3f(-width/2, height/2, -depth/2)
    glVertex3f(width/2, height/2, -depth/2)
    glVertex3f(width/2, height/2, depth/2)
    glVertex3f(-width/2, height/2, depth/2)
    # Bottom
    glNormal3f(0, -1, 0)
    glVertex3f(-width/2, -height/2, -depth/2)
    glVertex3f(width/2, -height/2, -depth/2)
    glVertex3f(width/2, -height/2, depth/2)
    glVertex3f(-width/2, -height/2, depth/2)
    glEnd()