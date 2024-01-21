import pygame # Game Engine
import json # For styles

# Import mathematical logic behind game
from QuantumAPI.ball import ball
from QuantumAPI.obstacle import obstacle

# Import Assets
from assets.scripts.draw import *
from assets.scripts.preferences import *


# MAIN
if __name__ == "__main__":
	pygame.init()
	
	# Get styles
	with open('style.json') as stylesFile: styles = json.load(stylesFile)

	# Get properly scaled/calculated sizing and resolution
	sizing = customScale()
	sizing = customResolution(sizing)

	# Define Variables
	presetObstacles = [[obstacle(*a) for a in i] for i in styles["obstaclePresets"]] # Turn presets into obstacle objects
	presetNum = 0 # Which preset we are currently on

	try:
		obstacles = presetObstacles[presetNum] # Set to first preset (Error out if it doesn't exist)
	except IndexError: # Nothing in preset list
		raise IndexError("Please add a preset in style.json")

	WIDTH = sizing["width"]
	HEIGHT = sizing["height"]

	PARTICLEWIDTH = sizing["particleWidth"]

	surface = pygame.display.set_mode((WIDTH,HEIGHT))

	while True:
		# Initial selecting direction/paddle of ball
		selectionComplete = False # If user has made paddle selection yet

		while not selectionComplete: # Wait for user to make paddle direction selection
			surface.fill((0,0,0)) # Reset screen
			obstacles = presetObstacles[presetNum] # Set obstacles to desired preset
			drawObstacle(surface, obstacles) # Draw obstacles

			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT: # Allow user to quit
					exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN: # Finished selection
						selectionComplete = True # Stop while loop after finishing everything
					elif event.key == pygame.K_LEFT: # Select previous preset
						presetNum = (presetNum - 1) % len(presetObstacles)
					elif event.key == pygame.K_RIGHT: # Select next preset
						presetNum = (presetNum + 1) % len(presetObstacles)

			pygame.display.flip() # Refresh frame

		# Create ball with desired obstacles
		gameBall = ball(obstacles, Dt=sizing["Dt"], sigma=sizing["sigma"])

		# Game loop
		currRound = True
		while currRound:
			surface.fill((0,0,0)) # Reset screen
			drawBall(surface, gameBall, PARTICLEWIDTH)
			drawObstacle(surface, obstacles) # Draw obstacles

			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT: # Allow user to quit
					exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN: # Finished selection
						currRound = False # Stop while loop after user says stop

			gameBall.propagate()
			gameBall.takeMod()

			pygame.display.flip() # Refresh frame
		
		result, winX, winY = gameBall.measure()
