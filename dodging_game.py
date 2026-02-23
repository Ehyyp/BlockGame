from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math
# Import obstacle class
from obstacleClasses import obstacleCourse
# And box drawing function
from obstacleClasses import drawBox

# Holds the camera position data
cameraPos = {
    'x': 0.0,
    'y': 0.0,
    'z': 0.0
}

# Times the jump
jumpTimer = {
    'time': 0
}

# Holds the game speed data
gameSpeed = {
    'speed': 0.04
}

# If command line arguments were used
if len(sys.argv) == 2:
    gameSpeed['speed'] = float(sys.argv[1])

# Number of obstacles in world
nObs = 3
# Defines the obstacle course
obstacleTypes = ["lowBar", "highBar", "rectangle", "lowBar", "highBar", "rectangle"]

# Sets up the course
stage = obstacleCourse(nObs, obstacleTypes)

def init():
    # Set background color
    #glClearColor(0.0, 0.0, 0.0, 1.0)
    # Enable depth
    glEnable(GL_DEPTH_TEST)
    # Makes color gradients smooth
    glShadeModel(GL_SMOOTH)
    # Enables the use of ligths
    glEnable(GL_LIGHTING)
    # Determines how many ligths can be used. GL_LIGHT0 means one ligth can be enabled. Max is 8
    glEnable(GL_LIGHT0)
   
    # Light properties
    # Default is (0, 0, 1, 0), x, y, z, w. If w = 0.0, it is treated as a directional source
    light_position = [0, 1, -1, 0.0]
    # GL_LIGHT0 here is the light identifier, it determines which light source we wish to alter
    # GL_POSITION sets the ligths position, the argument after it is the position. Takes in four floating point numbers
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
   
    # Specifies material parameters for the already specified lighting model
    # GL_FRONT defines which face of the material is being updated with this function
    # GL_SPECULAR defines the materials specular reflectance, the argument [1.0, 1.0, 1.0, 1.0] defines this reflectance
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    # Same as previous, but defines the shininess for the front
    glMaterialfv(GL_FRONT, GL_SHININESS, [50.0])
    # One or more material parameters track the current color when this is enabled
    glEnable(GL_COLOR_MATERIAL)
    # This causes the material color to track the current color
    # Front face materials should track the current color
    # Second argument specifies which material parameters track the current color. In our case, we want the material to
    # take into account ambient light and diffuse reflection
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)


# Sets up the display
def display():
    # Clear buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
   
    # Set camera position
    # eyex, eyey, eyez, centerx, centery, centerz, upx, upy, upz
    #gluLookAt(3, 2, 5, 0, 0.5, 0, 0, 1, 0)
    #glTranslatef(cameraPos['x'], cameraPos['y'], cameraPos['z'])
    gluLookAt(cameraPos['x'], cameraPos['y'], cameraPos['z'], cameraPos['x'], cameraPos['y'], cameraPos['z'] + 1, 0, 1, 0)

    # Draw the world
    drawWorld()
    # Draw obstacles
    stage.drawAllObs()
   
    # Double buffering displays one buffer and draws on another. Swapping them changes which one is displayed and which one is not
    # After swapping, the buffer that is no longer displayed is cleared
    glutSwapBuffers()

# Reshapes the window
def reshape(w, h):
    # Sets the viewport: x, y, width, height
    glViewport(0, 0, w, h)
    # Specifies which matrix is the current matrix
    # GL_PROJECTION allows subsequent matrix operations to the projection matrix stack
    # Other options for this are subsequent operations to modelview or texture matrix stacks
    glMatrixMode(GL_PROJECTION)
    # Replaces the current matrix with identity matrix
    glLoadIdentity()
    # Sets up a perspective projection matrix: fovy, aspect, zNear, zFar
    # fovy = Field of view angle in degrees, in the y-direction
    # aspect = aspect ratio, which is the ratio x (width) / y (heigth)
    # zNear = The distance from the viewer to the near clipping plane (always positive)
    # zFar = The distance from the viewer to the far clipping plane (always positive)
    gluPerspective(45, w/h, 0.1, 50.0)
    # Changes to model view mode
    glMatrixMode(GL_MODELVIEW)

# Defines the world box as ground and sky boxes
def drawWorld():
    # Ground matrix
    glPushMatrix()
    # Translate to below camera
    glTranslatef(0, -1, 35)
    # Green
    glColor3f(0, 255, 0)
    # Draw ground
    drawBox(70, 0.1, 70)
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
    drawBox(100, 100, 0.1)
    # Change color back to white
    glColor3f(1, 1, 1)
    # Move out of sky matrix
    glPopMatrix()

# Defines keyboard input
# WASD controls
def keyboard(key, x, y):
    # W = up
    if key == b'w':
        if cameraPos['y'] != 0.5:
            cameraPos['y'] += 0.5
    # A = left
    if key == b'a':
        if cameraPos['x'] != 1:
            cameraPos['x'] += 1
    # S = down
    if key == b's':
        if cameraPos['y'] != -0.5:
            cameraPos['y'] -= 0.5
    # D = right
    if key == b'd':
        if cameraPos['x'] != -1:
            cameraPos['x'] -= 1
   
    # Tell GLUT that the display needs to be refreshed
    glutPostRedisplay()

# Defines what happens at idle, i.e. update obstacles and refresh display
def idle():
    # If player in air
    if cameraPos['y'] == 0.5:
        # And jump time ended
        if jumpTimer['time'] == 36:
            # Bring to ground
            cameraPos['y'] = 0
            jumpTimer['time'] = 0
        # If not, increment jump timer
        else:
            jumpTimer['time'] += 1

    # Move obstacles
    #print(stage.obstacles[0][0].z)
    stage.moveAllObs(gameSpeed['speed'])
    stage.checkHit(cameraPos)

    # Refresh display
    glutPostRedisplay()

def main():
    # Initialize GLUT library
    glutInit(sys.argv)
    # Select display channels and buffering. Here 4 channels are used, RGB and depth. Double buffering enabled
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    # Set windowsize
    #glutInitWindowSize(800, 600)
    window = glutCreateWindow(b"Dodging game")
    glutSetWindow(window)
    glutFullScreen()
    init()
    # Sets the functions that determine how the display, window reshaping and keyboard callbacks work
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(idle)
    # Starts the main loop for the window. This is exited once the program is termintated
    glutMainLoop()

# Start game
if __name__ == "__main__":
    main()