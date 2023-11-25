class obstacle:
	def __init__(self, beginX: int, beginY: int, endX: int, endY: int, balls: list) -> None:
		self.beginX = beginX
		self.beginY = beginY
		self.endX = endX
		self.endY = endY

		self.balls = balls

	def calcBearing(self, oldBearing, side):
		return 180 - oldBearing

	
	def checkCollided(self):
		for subBall in balls:
			if beginX >= subBall.x >= endX and beginY >= subBall.y >= endY:
				subBall.changeAngle(calcBearing(subBall.angle))

		