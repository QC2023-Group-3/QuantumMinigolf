import numpy as np
import math
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve
import random


class ball:
    def __init__(self, obstacles, angle, L=5, Dy=0.05, Dt=0.005, sigma=0.5):
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

        self.Nx = int(L / Dy) + 1
        self.Ny = int(L / Dy) + 1
        self.rx = -Dt / (2j * Dy**2)
        self.ry = -Dt / (2j * Dy**2)

        self.sigma = sigma
        self.angle = angle

        # Initial position of the center of the Gaussian wave function.
        self.x0 = L / 5
        self.y0 = L / 2

        # Goal variables
        self.in_goal_coords = []
        self.outside_goal_coords = []

        # Obstacles
        self.obstacles = obstacles

        # Potential.  (Here at all positions v=0, use function to apply
        # interactions.    wxy)
        self.v = np.zeros((self.Ny, self.Ny), complex)
        # Number of unknown factors v[i,j], i = 1,...,Nx-2, j = 1,...,Ny-2
        self.Ni = (self.Nx - 2) * (self.Ny - 2)

        # Matrices for the Crank-Nicolson calculus. The problem A·x[n+1] = b =
        # M·x[n] will be solved at each time step.
        # 159*159 (wxy)
        self.A = np.zeros((self.Ni, self.Ni), complex)
        # 159*159 (wxy)
        self.M = np.zeros((self.Ni, self.Ni), complex)

        # We fill the A and M matrices.
        for k in range(self.Ni):

            i = 1 + k // (self.Ny - 2)
            j = 1 + k % (self.Ny - 2)

            # Main central diagonal.
            self.A[k, k] = 1 + 2 * self.rx + 2 * \
                self.ry + 1j * self.Dt / 2 * self.v[i, j]
            self.M[k, k] = 1 - 2 * self.rx - 2 * \
                self.ry - 1j * self.Dt / 2 * self.v[i, j]

            if i != 1:  # Lower lone diagonal.
                self.A[k, (i - 2) * (self.Ny - 2) + j - 1] = -self.ry
                self.M[k, (i - 2) * (self.Ny - 2) + j - 1] = self.ry

            if i != self.Nx - 2:  # Upper lone diagonal.
                self.A[k, i * (self.Ny - 2) + j - 1] = -self.ry
                self.M[k, i * (self.Ny - 2) + j - 1] = self.ry

            if j != 1:  # Lower main diagonal.
                self.A[k, k - 1] = -self.rx
                self.M[k, k - 1] = self.rx

            if j != self.Ny - 2:  # Upper main diagonal.
                self.A[k, k + 1] = -self.rx
                self.M[k, k + 1] = self.rx

        # sparse matrix, use csc_matrix() to store the non-zero elements in the
        # matrix (wxy)
        self.Asp = csc_matrix(self.A)

        # Array of spatial points. (0,8,159?  wxy)
        self.x = np.linspace(0, L, self.Ny - 2)
        self.y = np.linspace(0, L, self.Ny - 2)  # Array of spatial points.
        self.x, self.y = np.meshgrid(self.x, self.y)

        # We initialise the wave function with the Gaussian.   (159*159? wxy)
        self.psi = self.psi0()
        # The wave function equals 0 at the edges of the simulation box
        # (infinite potential well). (-1=last) (boundary conditions qqa)
        self.psi[0, :] = self.psi[-1, :] = self.psi[:, 0] = self.psi[:, -1] = 0

        self.initialisePsi()
        self.propagate()

    # angle = angle between direction of propagation to the vertical position
    # in degree
    def psi0(self, k=15 * np.pi):
        # theta=-np.pi/180*self.angle #convert to radians
        theta = self.angle
        return np.exp(-1 / 2 * ((self.x - self.x0)**2 + (self.y - self.y0)**2) / self.sigma**2) * \
            np.exp(-1j * k * ((self.y - self.y0) * np.cos(theta) + (self.x - self.x0) * np.sin(theta)))

    def propagate(self):
        # We adjust the shape of the array to generate the matrix b of
        # independent terms.
        psi_vect = self.psi.reshape((self.Ni))
        # We calculate the array of independent terms.
        b = np.matmul(self.M, psi_vect)
        # Solve for time step.   (Asp x = b, solve x, which equals to psi_vect.
        # wxy)
        psi_vect = spsolve(self.Asp, b)
        # Recover array from wave function.
        self.psi = psi_vect.reshape((self.Nx - 2, self.Ny - 2))
        for i in range(len(self.obstacles)):
            # We retrieve the shape of the wave function array. (??? wxy)
            self.psi = self.obstacles[i].checkCollided(self.psi)

    # We calculate the modulus of the wave function at each time step.
    def takeMod(self, wavefunc):
        re = np.real(wavefunc)  # Real part.
        im = np.imag(wavefunc)  # Imaginary part.
        mod = np.sqrt(re**2 + im**2)

        return mod

    def setGoalCoords(self, coords, rad):
        self.goalCoords = coords[0], coords[1]
        self.goalRad = rad

    def checkInGoal(self, x, y):
        x2, y2 = self.goalCoords
        pointX = x * 6 - 3
        pointY = y * 6 - 3
        distance = math.hypot(pointX - x2, pointY - y2)
        if distance <= self.goalRad:
            return True
        else:
            return False

    def measure(self, mod_end):
        # to record the total amplitude in the whole space, for normalization
        # later.
        prob_density=mod_end.flatten()
        prob_density/=sum(prob_density)
        selected_index = np.random.choice(
                len(prob_density),
                p=prob_density)
        
        i = 1 + selected_index % (self.Ny - 2) # transform to x-coordinate of selected point
        j = 1 + selected_index // (self.Ny - 2) # transform to y-coordinate of selected point
        
        win = self.checkInGoal(i,j)
        '''
        in_goal_prob_density = []
        outside_goal_prob_density = []
        for i in range(self.Nx - 2):
            for j in range(self.Ny - 2):
                modulus = mod_end[i, j]
                mod_total = mod_total + modulus
                if (self.checkInGoal(i, j)):
                    mod_goal = mod_goal + modulus
                    in_goal_prob_density.append(modulus)
                else:
                    self.outside_goal_coords.append((i, j))
                    outside_goal_prob_density.append(modulus)
        j = 1 + selected_index // (self.Ny - 2)
        # x-coordinate of selected point
        i = 1 + selected_index % (self.Ny - 2)

        # The probability to win the game (?)
        probability = mod_goal / mod_total
        random_number = random.random()

        if probability - random_number > 0:
            win = True
            # selected_index=np.where(in_goal_prob_density==np.amax(in_goal_prob_density))[0][0]
            # #(for testing)
            selected_index = np.random.choice(
                len(in_goal_prob_density),
                p=in_goal_prob_density /
                sum(in_goal_prob_density))
        else:
            win = False
            # selected_index=np.where(outside_goal_prob_density==np.amax(outside_goal_prob_density))[0][0]
            # #(for testing)
            selected_index = np.random.choice(
                len(outside_goal_prob_density),
                p=outside_goal_prob_density /
                sum(outside_goal_prob_density))

        j = 1 + selected_index // (self.Ny - 2)
        # x-coordinate of selected point
        i = 1 + selected_index % (self.Ny - 2)
        print(i, j)'''
    # y-coordinate of selected point

        return (win, i, j)

    def initialisePsi(self):
        # We initialise the wave function with the Gaussian.   (159*159? wxy)
        self.psi = self.psi0()
        # The wave function equals 0 at the edges of the simulation box
        # (infinite potential well). (-1=last) (boundary conditions qqa)
        self.psi[0, :] = self.psi[-1, :] = self.psi[:, 0] = self.psi[:, -1] = 0
