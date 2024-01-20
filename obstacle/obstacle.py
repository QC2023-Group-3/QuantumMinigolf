class obstacle:
	def __init__(self, beginX: int, beginY: int, endX: int, endY: int, scale: int = 6) -> None:
		self.beginX = int(beginX/scale)
		self.beginY = int(beginY/scale)
		self.endX = int(endX/scale)
		self.endY = int(endY/scale)

		# For drawing
		self.left = beginX
		self.top = beginY
		self.width = abs(beginX-endX)
		self.height = abs(beginY-endY)
	
	def checkCollided(self, psi):
		for y in range(self.beginY, self.endY):
			for x in range(self.beginX, self.endX):
				psi[y][x] = 0

		return psi
		