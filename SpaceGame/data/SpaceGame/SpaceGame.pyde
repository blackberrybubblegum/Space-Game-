add_library('minim')  # Import the Minim library for audio functionality
import random  # Import random module for generating random numbers
from math import sqrt, sin, cos, radians, pi # Use lowercase pi for stability

# Define constants for the game
RESOLUTION_W, RESOLUTION_H = 1000, 700 # Width and Height of the game window
R, MOVE_SPEED = 75, 5 # Radius of the planet and speed at which objects move downwards
ASTRO_D, ASTRO_H, STAR_D = 40, 60, 30 # Dimensions for astronaut and star

# Function to calculate three equidistant points on a line segment joining two circles
# x1, y1 and x2, y2 are the coordinates of the centers of the two circles
# r1 and r2 are the radii of the two circles
def get_three_points(x1, y1, x2, y2, r1, r2):
    # Minimum distance offset
    offset = 40 + 15  # 55 pixels
    
    total_distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)
    dx = (x2 - x1) / total_distance
    dy = (y2 - y1) / total_distance

    # Adjust start and end distances to ensure minimum separation from both planets
    start_distance = r1 + offset
    end_distance = total_distance - (r2 + offset)
    valid_distance = end_distance - start_distance
    
    points = []
    for t in [0.25, 0.5, 0.75]:
        distance = start_distance + t * valid_distance
        x = x1 + distance * dx
        y = y1 + distance * dy
        points.append((x, y))

    return points # points is a list of the three points

class Planet:
    def __init__(self, x, y, r, img_list):
        self.x = x  # x-coordinate of the planet's center
        self.y = y  # y-coordinate of the planet's center
        self.r = r  # Radius of the planet
        self.type = random.randint(0, 2)  # Randomly choose the type of the planet
        self.images = img_list # Reference pre-loaded images
        self.angle = 0  # Initial rotation angle of the planet
        self.target_y = self.y  # Target y-position for smooth downward movement

    def display(self):
        imageMode(CENTER)  # Set image mode to center
        self.angle += radians(1.5)  # Increment rotation angle
        if self.y < self.target_y:
            self.y = min(self.y + MOVE_SPEED, self.target_y)  # Move planet downward smoothly
        pushMatrix()  # Save the current transformation matrix
        translate(self.x, self.y)  # Move to the planet's position
        rotate(self.angle)  # Rotate the coordinate system by the planet's angle
        image(self.images[self.type], 0, 0, 2 * R, 2 * R)  # Display the planet's image
        popMatrix()  # Restore the previous transformation matrix
        
class Star:
    def __init__(self, x, y, img, sound):
        self.x = x  # x-coordinate of the star's center
        self.y = y  # y-coordinate of the star's center
        self.img = img  # Use pre-loaded image for the star
        self.coin_sound = sound  # Use pre-loaded sound for collecting a star
        self.targety = self.y  # Target y-position for smooth downward movement

    def display(self):
        image(self.img, self.x, self.y)  # Display the star's image
        if self.y < self.targety:
            self.y = min(self.y + MOVE_SPEED, self.targety)  # Move star downward smoothly

    def check_star_collision(self):
        d = sqrt((self.x - game.astronaut.x)**2 + (self.y - game.astronaut.y)**2)  # Calculate the distance between the star and the astronaut
        
        # if the distance between the center of the astronaut and the center of the star is less than or equal to the radius of the star plus half the width of the astronaut
        if d <= STAR_D / 2 + ASTRO_D / 2:
            self.coin_sound.rewind()  # Rewind the coin sound
            self.coin_sound.play()  # Play the coin sound
            game.stars = [star for star in game.stars if star != self]  # Remove this star from the list of stars
            game.score += 1  # Increment the game score

class Astronaut:
    def __init__(self, x, y, img, j_snd, s_snd):
        self.x = x  # x-coordinate of the astronaut
        self.y = y  # y-coordinate of the astronaut
        self.img = img  # Use pre-loaded image for the astronaut
        self.jump_sound = j_snd  # Use pre-loaded sound for jumping
        self.scream_sound = s_snd  # Use pre-loaded sound for out-of-bounds scream
        self.angle = 0  # astronaut initially begins rotating from the bottom of the planet and then around
        self.move = False  # Whether the astronaut is moving
        self.rot = True  # Whether the astronaut is rotating around the planet
        self.move_initialized = False  # Whether the move has been initialized
        self.allow_astro_coord_change = False  # used to allow a change in the coordinate of astronaut only in the frame right after the launch
        self.jump = -1  # used later in code to determine which planet the astronaut is currently on
        self.scream = 0  # allows scream to only be played once

    def display(self):
        pushMatrix()  # saves the current transformation matrix
        
        if self.rot and self.jump % 2 == 1:  # if rotation is allowed and astronaut is on planet0
            translate(game.planets[0].x, game.planets[0].y)  # moves center of point of rotation to center point of planet0
            rotate(radians(self.angle))  # rotates whatever "angle" is by first converting to radians
            image(self.img, 0, R + 25)  # Display the astronaut's image in top of planet
            self.angle += 1.5  # Increment the angle
            self.move_initialized = False  # once astronaut lands on next planet allow for the next jump
            
        elif self.rot and self.jump % 2 == 0: # if rotation is allowed and astronaut is on planet1. Note when jump is even, it has recently been launched from planet0 and is now on planet1
            self.move_initialized = False   # once astronaut lands on next planet allow for the next jump
            translate(game.planets[1].x, game.planets[1].y)   # moves center of point of rotation to center point of planet)
            rotate(radians(self.angle) + pi)  # rotates the coordinate system by "angle" + pi in order to have the astronaut displayed at the bottom of the planet (instead of top)
            image(self.img, 0, R + 25)  # Display the astronaut's image
            self.angle += 1.5  # Increment the angle
        popMatrix()  # Restore the previous transformation matrix

        if self.move == True: # once the astronaut is launched to new planet
            if self.jump % 2 == 0: # if jump is even then astronaut is launched from planet0 (so we want self.y to be relative to that planet0's coord. system)
                
                if self.allow_astro_coord_change:
                    # updating position of astronaut to its latest coordinate before jump
                    self.x = game.planets[0].x + (R + 25) * cos(radians(self.angle) + pi / 2)  # Adjust astronaut's x-coordinate
                    self.y = game.planets[0].y + (R + 25) * sin(radians(self.angle) + pi / 2)  # Adjust astronaut's y-coordinate
                    self.allow_astro_coord_change = False
                    
                for star in game.stars: # for every star check collision
                    star.check_star_collision()
                
                # increment position of center of the astronaut according to angle of launch
                self.y += 5 * sin(radians(self.angle) + pi / 2)  # the +pi/2 in the argument of sign ensures that sin is negative when astronaut is launched upwards
                self.x += 5 * cos(radians(self.angle) + pi / 2)  # Update x-coordinate
                
                pushMatrix()
                # then rotate the astronaut about itself
                translate(self.x, self.y)  # trasnslates the rotation axis to center of astronaut
                rotate(radians(self.angle))  # reminds code of the latest angle of the coordinate system
                image(self.img, 0, 0)  # display the image starting at edge of planet
                popMatrix()
                d = sqrt((self.x - game.planets[1].x)**2 + (self.y - game.planets[1].y)**2)  # Calculate distance of center of astronaut to to the planet1
                
            elif self.jump % 2 == 1: # if jump is odd then astronaut is launched from planet1 (so we want self.y to be relative to that planet1's coord. system)
                if self.allow_astro_coord_change:
                    self.x = game.planets[1].x + (R + 25) * sin(radians(self.angle))  # Adjust astronaut's x-coordinate
                    self.y = game.planets[1].y + (R + 25) * cos(radians(self.angle) + pi)  # Adjust astronaut's y-coordinate
                    self.allow_astro_coord_change = False
                    
                for star in game.stars:
                    star.check_star_collision()  # Check for collision with stars
                    
                # Note here that 5 determines the translational velocity of the astronaut
                self.y += 5 * cos(radians(self.angle) + pi) # the +pi in the argument of sign ensures that sin is negative when astronaut is launched upwards
                self.x += 5 * sin(radians(self.
