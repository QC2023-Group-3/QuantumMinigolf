import pygame # Game Engine
import json # For styles

# Import mathematical logic behind game
from QuantumAPI.ball import ball
from QuantumAPI.obstacle import obstacle

# Import Assets
from assets.scripts.draw import *


# MAIN
if __name__ == "__main__":
	pygame.init()
	
	obstacles = []

	# Get styles
	with open('../style.json') as stylesFile: styles = json.load(stylesFile)

	# Define Variables
	gameBall = ball(obstacles)

	WIDTH = styles["width"]
	HEIGHT = styles["height"]

	PARTICLEWIDTH = styles["particleWidth"]

	surface = pygame.display.set_mode((WIDTH,HEIGHT))

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
		drawBall(surface, gameBall, PARTICLEWIDTH)

		gameBall.propagate()
		gameBall.takeMod()

		pygame.display.flip() # Refresh frame
		frame += 1
	
	result, winX, winY = gameBall.measure()

