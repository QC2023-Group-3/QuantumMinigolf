import pygame # Game Engine
import json # For styles
import math #certain math functions
import numpy as np

# Import mathematical logic behind game
from assets.logic.ball import ball
from assets.logic.obstacle import obstacle

# Import Assets
from assets.scripts.draw import *
from assets.scripts.preferences import *
from assets.scripts.angle import *


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

	screen = pygame.display.set_mode((WIDTH,HEIGHT)) #main screen
	#surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) #surface to draw transparent object

	while True:
		obstacles = presetObstacles[1]
		# Create ball with desired obstacles
		gameBall = ball(obstacles, 0, Dt=sizing["Dt"], sigma=sizing["sigma"])
		hit = False
		dragging = False
		ballX = (HEIGHT/5)
		ballY = (WIDTH/2)
		# Game loop
		currRound = True

		while not hit:
			screen.fill((0,0,0)) # Reset screen
			drawBall(screen, gameBall, PARTICLEWIDTH)
			drawGoal(screen, WIDTH, HEIGHT)

			mouseX = pygame.mouse.get_pos()[0]
			mouseY = pygame.mouse.get_pos()[1]
			sqx = (mouseX - ballX)**2
			sqy = (mouseY - ballY)**2
			
			if math.sqrt(sqx + sqy) < 100:
				inside = True
			else:
				inside = False

			for event in pygame.event.get():
				if event.type == pygame.QUIT: # Allow user to quit
					exit()
				elif event.type == pygame.MOUSEBUTTONDOWN:           
					if inside:
						dragging = True

				elif event.type == pygame.MOUSEBUTTONUP:
					if dragging:
						dragging = False
						hit = True #end while loop
						angle = calcAngle((ballX, ballY), (mouseX, mouseY)) #get angle of ball to mouse
						print(angle)
						gameBall = ball(obstacles, angle[0], Dt=sizing["Dt"], sigma=sizing["sigma"])
			
			if dragging:
				drawPullBack(screen, mouseX, mouseY, ballX, ballY) #so that animation continues when no mouse movement is detected

			pygame.display.flip()
		
		while currRound:
			screen.fill((0,0,0)) # Reset screen
			drawBall(screen, gameBall, PARTICLEWIDTH)
			drawGoal(screen, WIDTH, HEIGHT)
			
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT: # Allow user to quit
					exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN: # Finished selection
						currRound = False # Stop while loop after user says stop

			gameBall.propagate()
			gameBall.takeMod()

			pygame.display.flip() # display frame
		
