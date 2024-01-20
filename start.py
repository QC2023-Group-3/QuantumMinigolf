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

	# Initial selecting direction/paddle of ball
	while True:
		drawObstacle(surface, obstacles) # Draw obstacles

		pygame.display.flip() # Refresh frame

