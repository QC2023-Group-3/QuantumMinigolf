import pygame # Game Engine

# Import mathematical logic behind game
from QuantumAPI.ball import ball
from QuantumAPI.obstacle import obstacle

# Import Assets
from assets.scripts.draw import *


# MAIN
if __name__ == "__main__":
	pygame.init()
	
	obstacles = []

	# Define Variables
	gameBall = ball(obstacles)

	surface = pygame.display.set_mode((400,300))

	DURATION = 100 # Time duration of project

	# Initial selecting direction/paddle of ball
	selectionComplete = False # If user has made paddle selection yet

	while not selectionComplete: # Wait for user to make paddle direction selection
		drawObstacle(surface, obstacles) # Draw obstacles

		pygame.display.flip() # Refresh frame

	# Game loop
	frame = 1
	while frame < DURATION:
		drawObstacle(surface, obstacles) # Draw obstacles

		pygame.display.flip() # Refresh frame
		frame += 1

