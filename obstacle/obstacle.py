class obstacle:
	def __init__(self, beginX: float, beginY: float, endX: int, endY: int, balls: list) -> None:
		self.beginX = beginX
		self.beginY = beginY
		self.endX = endX
		self.endY = endY

		self.balls = balls

	def calcBearing(self, oldBearing, side):
		return 180 - oldBearing

	
	def checkCollided(self):
		for subBall in self.balls:
			if self.beginX >= subBall.x >= self.endX and self.beginY >= subBall.y >= self.endY:
				subBall.changeAngle(self.calcBearing(subBall.angle))

		