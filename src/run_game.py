from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from game_graphics import graphics_class
import sys

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

def main():
    # Initialize game
    graphics_object = graphics_class(sys.argv[1], sys.argv[2])
    # Initialize GLUT library
    glutInit(sys.argv)
    # Select display channels and buffering. Here 4 channels are used, RGB and depth. Double buffering enabled
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    # Set windowsize
    #glutInitWindowSize(800, 600)
    window = glutCreateWindow(b"Palikkapeli")
    glutSetWindow(window)
    glutFullScreen()
    init()
    # Sets the functions that determine how the display, window reshaping and keyboard callbacks work
    glutDisplayFunc(graphics_object.display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(graphics_object.keyboard)
    glutIdleFunc(graphics_object.idle)
    # Starts the main loop for the window. This is exited once the program is termintated
    glutMainLoop()

# Start game
if __name__ == "__main__":
    main()