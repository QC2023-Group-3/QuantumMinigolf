import json
import pygame

# Open colors selection
with open('../style.json') as styles: COLORS = json.load(styles)['colors']

# Draw obstacles
def drawObstacle(surface, obstacles) -> None:
	for obstacle in obstacles:
		left = obstacle.beginX
		top = obstacle.beginY
		width = abs(obstacle.beginX-obstacle.beginY)
		height = abs(obstacle.beginY-obstacle.endY)

		pygame.draw.rect(surface, COLORS["obstacle"], pygame.Rect(left, top, width, height))
