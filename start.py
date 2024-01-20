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
	
	# Get styles
	with open('assets/style.json') as stylesFile: styles = json.load(stylesFile)

	# Define Variables
	presetObstacles = [obstacle(*i) for i in styles["obstaclePresets"]] # Turn presets into obstacle objects
	presetNum = 0 # Which preset we are currently on

	try:
		obstacles = presetObstacles[presetNum] # Set to first preset (Error out if it doesn't exist)
	except IndexError: # Nothing in preset list
		raise IndexError("Please add a preset in style.json")

	gameBall = ball(obstacles)

	WIDTH = styles["width"]
	HEIGHT = styles["height"]

	PARTICLEWIDTH = styles["particleWidth"]

	surface = pygame.display.set_mode((WIDTH,HEIGHT))

	DURATION = 200 # Time duration of project

	# Initial selecting direction/paddle of ball
	selectionComplete = False # If user has made paddle selection yet

	while not selectionComplete: # Wait for user to make paddle direction selection
		obstacles = presetObstacles[presetNum] # Set obstacles to desired preset
		drawObstacle(surface, obstacles) # Draw obstacles

		events = pygame.event.get()
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN: # Finished selection
					selectionComplete = True # Stop while loop after finishing everything
				elif event.key == pygame.K_LEFT: # Select previous preset
					presetNum -= 1 # Reduce preset by 1
					if presetNum < 0:
						presetNum = len(presetObstacles)-1 # Set to last preset, -1 because of index numbers
				elif event.key == pygame.K_RIGHT: # Select next preset
					presetNum += 1
					if presetNum > len(presetObstacles)-1:
						presetNum = 0 # Reset preset number

		pygame.display.flip() # Refresh frame

	# Game loop
	frame = 1
	while frame < DURATION:
		drawBall(surface, gameBall, PARTICLEWIDTH)
		drawObstacle(surface, obstacles) # Draw obstacles

		gameBall.propagate()
		gameBall.takeMod()

		pygame.display.flip() # Refresh frame
		frame += 1
	
	result, winX, winY = gameBall.measure()

