class obstacle:
	def __init__(self, beginX: float, beginY: float, endX: int, endY: int, balls: list, psi: list) -> None:
		self.beginX = beginX
		self.beginY = beginY
		self.endX = endX
		self.endY = endY

		self.balls = balls
		self.psi = psi
	
	def newPsi(self, newPsi) -> None:
		self.psi = newPsi
	
	def changedPsi(self) -> list:
		return self.psi
	
	def checkCollided(self):
		for y in range(len(self.psi)):
			for x in range(len(y)):
				if self.beginY >= y >= self.endY and self.beginX >= x >= self.endX:
					self.psi[y][x] = 0

		return self.psi
		