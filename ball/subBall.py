class subBall:
	def __init__(self, x: int, y: int, prob: float, bearing: int) -> None:
		# Note that angle is a bearing, degrees
		self.x = x
		self.y = y

		self.prob = prob
		self.bearing = bearing

	def move(self) -> None:
		# move the ball towards the direction of the angle (self.angle)	
		""

	def changeBearing(self, newBearing) -> None:
		self.bearing = newBearing