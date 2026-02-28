from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from gameState import gameStateClass
import sys

# Defines all of the graphics functionality
class graphicsClass:
    # Defines the game functionality
    gameState = None

    # Initialize graphics and game state
    def __init__(self, speed, stage):
        self.gameState = gameStateClass(speed, stage)

    # Sets up the display
    def display(self):
        # Clear buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
    
        # Set camera position
        # eyex, eyey, eyez, centerx, centery, centerz, upx, upy, upz
        gluLookAt(self.gameState.camX, self.gameState.camY, self.gameState.camZ, self.gameState.camX, self.gameState.camY, self.gameState.camZ + 1, 0, 1, 0)

        # Draw the world
        self.drawWorld()
        # Draw obstacles
        self.drawAllObs()
    
        # Double buffering displays one buffer and draws on another. Swapping them changes which one is displayed and which one is not
        # After swapping, the buffer that is no longer displayed is cleared
        glutSwapBuffers()

    # Defines keyboard input
    # WASD controls
    # The x and y parameters determine the mouse location when key is pressed and are required by the glutKeyboardFunc
    def keyboard(self, key, x=0, y=0):
        # Can't move in the air or when sliding
        self.gameState.keyboard(key)
        glutPostRedisplay()

    # Defines what happens at idle, i.e. update obstacles and refresh display
    def idle(self):
        self.gameState.idle()
        # Check if game is over
        if self.gameState.gameLost == True:
            print("You lost :(")
            glutDestroyWindow(glutGetWindow())
            sys.exit()
        elif self.gameState.gameWon == True:
            print("You won! :D")
            glutDestroyWindow(glutGetWindow())
            sys.exit()

        # Update display
        glutPostRedisplay()

    # Draw all obstacles
    def drawAllObs(self):
        # For each obstacle
        for obs in self.gameState.stage.obstacles:
            self.drawObstacle(obs)

    # Uses OpenGL to draw a single obstacle
    def drawObstacle(self, obstacle):
        # Push new matrix
        glPushMatrix()
        # Move to obstacle start
        glTranslatef(obstacle.x, obstacle.y, obstacle.z)
        # Set color to red
        glColor3f(255, 0, 0)
        # Draw with dimensions
        self.drawBox(obstacle.dx, obstacle.dy, obstacle.dz)
        # Set color back to white
        glColor3f(1, 1, 1)
        # Pop matrix
        glPopMatrix()

    # Draws an OpenGL box
    def drawBox(self, width, height, depth):
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

    # Defines the world box as ground and sky boxes
    def drawWorld(self):
        # Ground matrix
        glPushMatrix()
        # Translate to below camera
        glTranslatef(0, -1, 35)
        # Green
        glColor3f(0, 255, 0)
        # Draw ground
        self.drawBox(70, 0.1, 70)
        # Change color back to white
        glColor3f(1, 1, 1)
        # Move out of ground matrix
        glPopMatrix()

        # Sky matrix
        glPushMatrix()
        # Translate to end of ground
        glTranslatef(0, 30, 30)
        # Blue sky
        glColor3f(0, 0, 255)
        # Draw sky
        self.drawBox(100, 100, 0.1)
        # Change color back to white
        glColor3f(1, 1, 1)
        # Move out of sky matrix
        glPopMatrix()