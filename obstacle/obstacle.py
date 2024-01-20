class obstacle:
	def __init__(self, beginX: float, beginY: float, endX: int, endY: int) -> None:
		self.beginX = beginX
		self.beginY = beginY
		self.endX = endX
		self.endY = endY
	
	def checkCollided(self, psi):
		for y in range(len(psi)):
			for x in range(len(y)):
				if self.beginY >= y >= self.endY and self.beginX >= x >= self.endX:
					psi[y][x] = 0

		return psi
		