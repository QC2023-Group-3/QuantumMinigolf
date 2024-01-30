import pygame  # Game Engine
import json  # For styles
import math  # certain math functions
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
	with open('style.json') as stylesFile:
		styles = json.load(stylesFile)

	# Get properly scaled/calculated sizing and resolution
	sizing = customScale()
	sizing = customResolution(sizing)

	# Get fonts
	

	# Define Variables
	# Turn presets into obstacle objects
	presetObstacles = [[obstacle(*a) for a in i]
					   for i in styles["obstaclePresets"]]
	presetNum = 0  # Which preset we are currently on

	try:
		# Set to first preset (Error out if it doesn't exist)
		obstacles = presetObstacles[presetNum]
	except IndexError:  # Nothing in preset list
		raise IndexError("Please add a preset in style.json")

	WIDTH = sizing["width"]
	HEIGHT = sizing["height"]

	PARTICLEWIDTH = sizing["particleWidth"]

	screen = pygame.display.set_mode((WIDTH, HEIGHT))  # main screen
	# surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) #surface to
	# draw transparent object

	def scale(var):
		var = var * PARTICLEWIDTH - (PARTICLEWIDTH / 2)
		return var

	while True:
		# Initial selecting of obstacle preset
		selectionComplete = False  # If user has made selection yet

		while not selectionComplete:  # Wait for user to make obstacle selection
			screen.fill((0, 0, 0))  # Reset screen
			# Set obstacles to desired preset
			obstacles = presetObstacles[presetNum]
			drawObstacle(screen, obstacles)  # Draw obstacles

			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:  # Allow user to quit
					exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:  # Finished selection
						selectionComplete = True  # Stop while loop after finishing everything
					elif event.key == pygame.K_LEFT:  # Select previous preset
						presetNum = (presetNum - 1) % len(presetObstacles)
					elif event.key == pygame.K_RIGHT:  # Select next preset
						presetNum = (presetNum + 1) % len(presetObstacles)

			pygame.display.flip()  # Refresh frame

		# Create ball with desired obstacles
		gameBall = ball(obstacles, 0, Dt=sizing["Dt"], sigma=sizing["sigma"])
		hit = False
		dragging = False
		ballX = (HEIGHT / 5)
		ballY = (WIDTH / 2)
		# Game loop
		currRound = True

		while not hit:
			screen.fill((0, 0, 0))  # Reset screen
			drawBall(screen, gameBall, PARTICLEWIDTH)
			drawObstacle(screen, obstacles)  # Draw obstacles
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
				if event.type == pygame.QUIT:  # Allow user to quit
					exit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if inside:
						dragging = True

				elif event.type == pygame.MOUSEBUTTONUP:
					if dragging:
						dragging = False
						hit = True  # end while loop
						angle = calcAngle((ballX, ballY), (mouseX, mouseY))
						gameBall = ball(
							obstacles,
							angle[0],
							Dt=sizing["Dt"],
							sigma=sizing["sigma"])

			if dragging:
				# so that animation continues when no mouse movement is
				# detected
				drawPullBack(screen, mouseX, mouseY, ballX, ballY)

			pygame.display.flip()

		while currRound:
			screen.fill((0, 0, 0))  # Reset screen
			drawBall(screen, gameBall, PARTICLEWIDTH)
			drawObstacle(screen, obstacles)  # Draw obstacles
			drawGoal(screen, WIDTH, HEIGHT)

			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:  # Allow user to quit
					exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:  # Finished selection
						currRound = False  # Stop while loop after user says stop

			gameBall.propagate()

			pygame.display.flip()  # display frame

		gameBall.setGoalCoords((WIDTH * 4 / 5, HEIGHT / 2), 50)
		result, winX, winY = gameBall.measure(gameBall.takeMod(
			gameBall.psi))  # unsure what to pass into mod_end

		finX = scale(winX)
		finY = scale(winY)

		endscreen = True
		while endscreen:
			pygame.draw.circle(screen, (0, 255, 0), (finX, finY), 7)
			drawGoal(screen, WIDTH, HEIGHT)
			drawResult(screen, result)

			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:  # Allow user to quit
					exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						screen.fill((0, 0, 0))  # Reset screen
						endscreen = False

			pygame.display.flip()
