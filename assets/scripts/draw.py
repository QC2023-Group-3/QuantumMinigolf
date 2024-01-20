import json
import pygame
import numpy as np

# Open colors selection 
with open('style.json') as styles: COLORS = json.load(styles)['colors']

# Draw obstacles
def drawObstacle(surface, obstacles) -> None:
	for obstacle in obstacles:
		pygame.draw.rect(surface, COLORS["obstacle"], pygame.Rect(obstacle.left, obstacle.top, obstacle.width, obstacle.height))

# Draw the ball
def drawBall(surface, ball, particleWidth) -> None:
	psi = ball.psi
	npPsi = np.array(psi)

	psiMagnitude = np.abs(npPsi)
	maxPsiMag = np.max(psiMagnitude)
	normalizedMag = psiMagnitude / maxPsiMag

	# Converting psi/matrix to a surface
	for yPos, y in enumerate(normalizedMag):
		for xPos, x in enumerate(y):
			currColor = int(x*255)
			color = tuple(i*currColor for i in COLORS["ballHeatmap"]) # Select which RGB values should be colored

			pygame.draw.rect(surface, color, pygame.Rect(((xPos*particleWidth-(particleWidth/2)), (yPos*particleWidth-(particleWidth/2))), (particleWidth, particleWidth)))