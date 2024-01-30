import json
import pygame
import numpy as np

# Open colors selection
with open('style.json') as styles:
    COLORS = json.load(styles)['colors']
    TEXTFONT = json.load(styles)['textfont']
    TEXTSIZE = json.load(styles)['textsize']
    DEFAULTS = json.load(styles)['defaults']

# Draw obstacles


def drawObstacle(surface, obstacles) -> None:
    for obstacle in obstacles:
        pygame.draw.rect(
            surface,
            COLORS["obstacle"],
            pygame.Rect(
                obstacle.left,
                obstacle.top,
                obstacle.width,
                obstacle.height))

# Draw result

def drawResult(surface, result) -> None:
    font=pygame.font.Font(TEXTFONT,TEXTSIZE)
    if result:
        text=font.render("You Win!", True, COLORS["resultText"])
    else:
        text = font.render("You Lose!", True, COLORS["resultText"])
    text_rect=text.get_rect(center=(DEFAULTS["width"]/2, DEFAULTS["height"]/2))
    surface.blit(text,text_rect)


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
            currColor = int(x * 255)
            # Select which RGB values should be colored
            color = tuple(i * currColor for i in COLORS["ballHeatmap"])

            pygame.draw.rect(surface,
                             color,
                             pygame.Rect(((xPos * particleWidth - (particleWidth / 2)),
                                          (yPos * particleWidth - (particleWidth / 2))),
                                         (particleWidth,
                                          particleWidth)))

# draw line from centre of ball to mouse position


def drawPullBack(surface, mouseX, mouseY, ballX, ballY):
    pygame.draw.line(surface, (255, 255, 255),
                     (ballX, ballY), (mouseX, mouseY), 4)

# draw the goal


def drawGoal(surface, screenWidth, screenHeight):
    centerX = screenWidth * 4 / 5
    centerY = screenHeight / 2
    pygame.draw.circle(surface, (255, 255, 255), (centerX, centerY), 50, 4)
