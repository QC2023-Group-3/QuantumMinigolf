class subBall:
	def __init__(self, x: int, y: int, bearing: int) -> None:
		# Note that angle is a bearing, degrees
		self.x = x
		self.y = y

		self.bearing = bearing

	def move(self) -> None:
		# move the ball towards the direction of the angle (self.bearing)	
		""

	def changeBearing(self, newBearing) -> None:
		self.bearing = newBearing