import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve
import random

class ball:
	def __init__(self, obstacles, L = 5,  Dy = 0.05, Dt = 0.005, sigma = 0.5):
		"""
		L = Well of width L. Shafts from 0 to +L.
		Dy = Spatial step size.
		Dt = Temporal step size.
		Nx = Number of points on the x axis. #window size (qqa)
		Ny = Number of points on the y axis. #window size (qqa)
		rx = Constant to simplify expressions.
		ry = Constant to simplify expressions.
		"""

		# Initialize Parameters
		self.L = L
		self.Dy = Dy
		self.Dt = Dt

		self.Nx = int(L/Dy) + 1
		self.Ny = int(L/Dy) + 1
		self.rx = -Dt/(2j*Dy**2)
		self.ry = -Dt/(2j*Dy**2)

		self.sigma = sigma
		
		# Initial position of the center of the Gaussian wave function.
		self.x0=L/5
		self.y0=L/2

		# Goal variables
		self.in_goal_coords = []
		self.outside_goal_coords = []

		# Obstacles
		self.obstacles = obstacles

		self.v = np.zeros((self.Ny,self.Ny), complex) # Potential.  (Here at all positions v=0, use function to apply interactions.    wxy)
		self.Ni = (self.Nx-2)*(self.Ny-2)  # Number of unknown factors v[i,j], i = 1,...,Nx-2, j = 1,...,Ny-2

		# Matrices for the Crank-Nicolson calculus. The problem A·x[n+1] = b = M·x[n] will be solved at each time step.
		self.A = np.zeros((self.Ni,self.Ni), complex)              # 159*159 (wxy)
		self.M = np.zeros((self.Ni,self.Ni), complex)              # 159*159 (wxy)

		# We fill the A and M matrices.
		for k in range(self.Ni):

			i = 1 + k//(self.Ny-2)
			j = 1 + k%(self.Ny-2)

			# Main central diagonal.
			self.A[k,k] = 1 + 2*self.rx + 2*self.ry + 1j*self.Dt/2*self.v[i,j]
			self.M[k,k] = 1 - 2*self.rx - 2*self.ry - 1j*self.Dt/2*self.v[i,j]

			if i != 1: # Lower lone diagonal.
				self.A[k,(i-2)*(self.Ny-2)+j-1] = -self.ry
				self.M[k,(i-2)*(self.Ny-2)+j-1] = self.ry

			if i != self.Nx-2: # Upper lone diagonal.
				self.A[k,i*(self.Ny-2)+j-1] = -self.ry
				self.M[k,i*(self.Ny-2)+j-1] = self.ry

			if j != 1: # Lower main diagonal.
				self.A[k,k-1] = -self.rx
				self.M[k,k-1] = self.rx

			if j != self.Ny-2: # Upper main diagonal.
				self.A[k,k+1] = -self.rx
				self.M[k,k+1] = self.rx

		self.Asp = csc_matrix(self.A) # sparse matrix, use csc_matrix() to store the non-zero elements in the matrix (wxy)

		self.x = np.linspace(0, L, self.Ny-2) # Array of spatial points. (0,8,159?  wxy)
		self.y = np.linspace(0, L, self.Ny-2) # Array of spatial points.
		self.x, self.y = np.meshgrid(self.x, self.y)

		self.psi = self.psi0(self.x, self.y, self.x0, self.y0) # We initialise the wave function with the Gaussian.   (159*159? wxy)
		self.psi[0,:] = self.psi[-1,:] = self.psi[:,0] = self.psi[:,-1] = 0 # The wave function equals 0 at the edges of the simulation box (infinite potential well). (-1=last) (boundary conditions qqa)

		self.initialisePsi()
		self.propagate()
		self.takeMod()

	def psi0(self, x, y, x0, y0, k=15*np.pi):
		return np.exp(-1/2*((x-x0)**2 + (y-y0)**2)/self.sigma**2)*np.exp(1j*k*(x-x0))

	def propagate(self):
		psi_vect = self.psi.reshape((self.Ni)) # We adjust the shape of the array to generate the matrix b of independent terms.
		b = np.matmul(self.M,psi_vect) # We calculate the array of independent terms.
		psi_vect = spsolve(self.Asp,b) # Resolvemos el sistema para este paso temporal.   (Asp x = b, solve x, which equals to psi_vect.   wxy)	
		self.psi = psi_vect.reshape((self.Nx-2,self.Ny-2)) # Recuperamos la forma del array de la función de onda.
		for i in range (len(self.obstacles)):
			self.psi = self.obstacles[i].checkCollided(self.psi) # We retrieve the shape of the wave function array. (??? wxy)

	# We calculate the modulus of the wave function at each time step.
	def takeMod(self):
		re = np.real(self.psi) # Real part.
		im = np.imag(self.psi) # Imaginary part.
		self.mod = np.sqrt(re**2 + im**2)

		return self.mod

	def setGoalCoords(self, coords):
		self.in_goal_coords=coords #in the form of (i,j)

	def measure(self,Nx,Ny,mod_end):
		mod_total = 0 # to record the total amplitude in the whole space, for normalization later.
		mod_goal = 0 # calculate the total module of psi in the target area (your goal).
		win=True

		in_goal_prob_density=[]
		outside_goal_prob_density=[]
		for i in range(Nx-2):
			for j in range(Ny-2):
				modulus=mod_end[i,j]
				mod_total = mod_total + modulus
				if ((i,j) in self.in_goal_coords):
					mod_goal=mod_goal+modulus
					in_goal_prob_density.append(modulus)
				else:
					self.outside_goal_coords.append((i,j))
					outside_goal_prob_density.apend(modulus)

		probability = mod_goal / mod_total          # The probability to win the game (?)
		random_number = random.random()

		if probability - random_number > 0:
			win=True
			selected_index = np.random.choice(len(in_goal_prob_density), p=in_goal_prob_density)
		else:
			win=False
			selected_index = np.random.choice(len(outside_goal_prob_density), p=outside_goal_prob_density)
		
		i=selected_index[0] # x-coordinate of selected point
		j=selected_index[1] # y-coordinate of selected point
		return (win,i,j)
	
	def initialisePsi(self):
		self.psi = self.psi0(self.x, self.y, self.x0, self.y0) # We initialise the wave function with the Gaussian.   (159*159? wxy)
		self.psi[0,:] = self.psi[-1,:] = self.psi[:,0] = self.psi[:,-1] = 0 # The wave function equals 0 at the edges of the simulation box (infinite potential well). (-1=last) (boundary conditions qqa)
