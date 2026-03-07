"""
obstacle_classes.py module defines Obstacle and ObstacleCourse
classes. Obstacle class handles the data of a single obstacle
and ObstacleCourse handles the data of all obstacles in the
game.
"""

class Obstacle:
    """
    Handles obstacle shape and position data
    """
    # Dimensions
    x = None
    y = None
    z = None
    # Shape
    dx = None
    dy = None
    dz = 0.1
    # shape_type, which is square or bar
    shape_type = None

    # Constructs the obstacle with specified type
    def __init__(self, shape_type, z):
        # y coordinate is based on the type of obstacle
        if shape_type == "rectangle":
            self.y = 0
        elif shape_type == "lowBar":
            self.y = -0.6
        elif shape_type == "highBar":
            self.y = 0.3

        # x position for bars is always 0, for rectangles it is
        # determined in the obstacle_course class
        self.x = 0
        # z start position given
        self.z = z

        # Reshape the obstacle to correct type
        self.shape_type = shape_type
        self.reshape(shape_type)

    def reshape(self, shape):
        """
        Reshapes the object to rectangle, lowBar or highBar.
        Also changes the y position of the obstacle
        """
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

    def move_back(self, shape_type, z_pos):
        """
        Move obstacle to z_pos and reshape it to shape_type
        """
        # Move to start
        self.z = z_pos
        # Update shape type
        self.shape_type = shape_type
        # Change shape
        self.reshape(self.shape_type)

    def move_obstacle(self, speed):
        """
        Move object in z-axis by "speed" amount
        """
        self.z -= speed


# Controls all of the obstacles
class ObstacleCourse:
    """
    Handles the stage related data that includes obstacles, obstacle types
    and rectangle positions.
    Defines methods for moving all obstacles, changing obstacles x-axis location
    and checking if the player was hit by an obstacle.
    """
    # Holds all the obstacle objects and their shape type stacks
    obstacles = []
    # Determines the obstacles shape type through the game
    type_stack = []
    # Holds the rectangle obstacles starting x positions
    rec_x_positions = []

    # Initialize obstacles list with number of obstacles and the obstacle shape types stack
    def __init__(self, num_obstacles, obstacle_types, rec_x_positions):
        self.rec_x_positions = rec_x_positions
        # Defines first obstacles starting position
        start_pos = 5
        # Make sure obstacle list is empty before appending to it
        self.obstacles = []
        # Initialize each obstacle
        for i in range(0, num_obstacles):
            # Get first type of obstacle
            shape_type = obstacle_types.pop(0)
            # Add to list
            self.obstacles.append(Obstacle(shape_type, start_pos))
            # If the obstacle is a rectangle, determine its x-position from the stack
            self.relocate(self.obstacles[i])
            # Change starting position
            start_pos += 5
        # Save the remainder of initial obstacle types stack
        self.type_stack = obstacle_types

    # Moves all obstacles and checks their positions
    def move_all_obs(self, speed):
        """
        Move all obstacles forward by speed amount.
        Moves the obstacle back to start if it passed player
        and game still has more obstacles, otherwise remove
        obstacle from game.
        """
        # If obstacle list not empty
        if len(self.obstacles) != 0:
            # For each object
            for obs in self.obstacles:
                # Move forward
                obs.move_obstacle(speed)
                # If behind player
                if obs.z < 0:
                    # If stack is empty
                    if len(self.type_stack) == 0:
                        # Remove obstacle
                        self.obstacles.remove(obs)
                    # If not
                    else:
                        # z position based on number of obstacles
                        z_pos = len(self.obstacles) * 5
                        # Move back and change shape
                        shape_type = self.type_stack.pop(0)
                        obs.move_back(shape_type, z_pos)
                        # Move the object in x-axis, if shape type changed to or from rectangle
                        self.relocate(obs)
            # Return False for not winning, game kept going
            return False
        # If list is empty, game won
        return True

    # Relocates an obstacle in the x-axis
    def relocate(self, obstacle):
        """
        Relocates the obstacle x-position to shape
        appropriate location.
        """
        # It the object is a rectangle, change to xPos
        if obstacle.shape_type == "rectangle":
            # Check if the stack is empty
            if len(self.rec_x_positions) == 0:
                raise ValueError(
                    "Rectangle positions stack does not havethe correct amount of positions!"
                    )
            # If stack not empty, update position
            obstacle.x = self.rec_x_positions.pop(0)
        # Otherwise move to middle
        else:
            obstacle.x = 0

    # Check if obstacle hit player
    def check_hit(self, cam_x, cam_y):
        """
        Check if position (cam_x, cam_y) was
        hit by an obstacle
        """
        # For each obstacle
        for obs in self.obstacles:
            # If obstacle has same x coordinate as camera at z = 0
            if round(obs.z, 0) == 0:
                # If obstacle is a rectangle, x needs to be checked
                if obs.shape_type == "rectangle":
                    if obs.x == cam_x:
                        # Return True for being hit
                        return True
                # If obstacle is a bar, y needs to be checked
                # high bar hits when y is 0 or 0.5
                elif obs.shape_type == "highBar":
                    if cam_y != -0.5:
                        return True
                # low bar hits when y is 0 or -0.5
                elif obs.shape_type == "lowBar":
                    if cam_y != 0.5:
                        return True
        # Return False for not being hit
        return False
