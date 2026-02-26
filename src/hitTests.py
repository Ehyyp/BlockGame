from gameGraphics import gameStateObject
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pytest

# Initialize test game
speed = 0.05
gameState = gameStateObject(speed, test=True)
# Load test stage
gameState.load_stage("test")

print(gameState.camY)
print(gameState.jumpTime)
gameState.keyboard(b'w')

print(gameState.camY)
print(gameState.jumpTime)
gameState.idle()

print(gameState.camY)
print(gameState.jumpTime)