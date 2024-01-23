import pygame # Game Engine
import json # For styles
import math #certain math functions

# Import mathematical logic behind game
from assets.logic.ball import ball
from assets.logic.obstacle import obstacle

# Import Assets
from assets.scripts.draw import *
from assets.scripts.preferences import *
from assets.scripts.calculation import *


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
	#surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) #surface to draw transparent objects

	fps = 120 #sets speed/frames per second
	time = pygame.time.Clock

	while True:
		# Initial selecting of obstacle preset
		selectionComplete = False # If user has made selection yet

		while not selectionComplete: # Wait for user to make obstacle selection
			screen.fill((0,0,0)) # Reset screen
			obstacles = presetObstacles[presetNum] # Set obstacles to desired preset
			drawObstacle(screen, obstacles) # Draw obstacles

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

		hit = False
		# Game loop
		currRound = True
		while currRound:
			# Create ball with desired obstacles
			gameBall = ball(obstacles, Dt=sizing["Dt"], sigma=sizing["sigma"])

			screen.fill((0,0,0)) # Reset screen
			drawBall(screen, gameBall, PARTICLEWIDTH)
			drawObstacle(screen, obstacles) # Draw obstacles
			drawGoal(screen, WIDTH, HEIGHT)

			scale = gameBall.Nx/WIDTH
			ballX = gameBall.x0*scale
			ballY = gameBall.y0*scale 
			dragging = False

			pygame.display.set_caption(str(ballX))
			pygame.display.set_caption(str(ballY))

			while not hit:
				screen.fill((0,0,0)) # Reset screen
				drawBall(screen, gameBall, PARTICLEWIDTH)
				drawObstacle(screen, obstacles) # Draw obstacles
				drawGoal(screen, WIDTH, HEIGHT)

				pygame.draw.circle(screen, (255, 255, 255), (ballX, ballY), 10)

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
						if dragging == True:
							dragging = False
							hit = True #end while loop
							angle = calcAnge()
				
				if dragging:
					drawPullBack(screen, mouseX, mouseY, ballX, ballY) #so that animation continues when no mouse movement is detected

				pygame.display.flip()

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
		
		result, winX, winY = gameBall.measure(WIDTH, HEIGHT, )
