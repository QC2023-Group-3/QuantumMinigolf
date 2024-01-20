from manim import * # Animation Engine
import pyglet # User Input
from pyglet.window import key as pyglet_key # Keyboard Input

from QuantumAPI.ball import ball
from QuantumAPI.obstacle import obstacle


class QuantumMinigolf(Scene):
	def construct(self):
		# Define Variables
		self.gameBall = ball()
