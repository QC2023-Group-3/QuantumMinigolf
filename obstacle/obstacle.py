class obstacle:
	def __init__(self, beginX: float, beginY: float, endX: int, endY: int, balls: list) -> None:
		self.beginX = beginX
		self.beginY = beginY
		self.endX = endX
		self.endY = endY

		self.balls = balls

	def calcSide(self, ballX, ballY) -> str:
		if self.beginX <= ballX <= self.endX and ballY == self.endY:
			return 'N'
		if self.beginY <= ballY <= self.endY and ballX == self.endX:
			return 'E'
		if self.beginX <= ballX <= self.endX and ballY == self.beginY:
			return 'S'
		if self.beginY <= ballY <= self.endY and ballX == self.endX:
			return 'W'

	def calcBearing(self, oldBearing, side):
		match side:
			case 'N': #value entered must be 0 < x < 360
				if oldBearing <= 90:
					return 360 - oldBearing
				else:
					return 180 - oldBearing
			case 'E': #value entered must be 0 < x < 180
				return 180 - oldBearing
			case 'S': #value entered must be 90 < x < 360
				return 360 - oldBearing
			case 'W': #value entered must be 180 < x < 360
				if oldBearing <= 270:
					return 540 - oldBearing
				else:
					return 540 - oldBearing
	
	def checkCollided(self):
		for subBall in self.balls:
			if self.beginX >= subBall.x >= self.endX and self.beginY >= subBall.y >= self.endY:
				subBall.changeAngle(self.calcBearing(subBall.angle, self.calcSide(subBall.x, subBall.y)))

		