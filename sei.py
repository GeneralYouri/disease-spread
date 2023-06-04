import numpy as np
import random
from enum import IntEnum
from si import *


class SEI(SI):
    theta = 0
    
    class State(IntEnum):
        SUSCEPTIBLE = 0,
        EXPOSED = 1,
        INFECTIOUS = 0,
    
    def initialize(self):
        self.grid = np.full([self.size, self.size], self.State.SUSCEPTIBLE)
        
        # Start by exposing the center cell
        # self.grid[self.center, self.center] = self.State.EXPOSED
        
        # Start by exposing 10% of cells randomly
        initial = round(self.size * self.size / 10)
        for _ in range(0, initial):
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            while (self.grid[x, y] == self.State.EXPOSED):
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
            self.grid[x, y] = self.State.EXPOSED
    
    def updateCell(self, x, y):
        neighbours = self.getNeighbours(x, y)
        if self.grid[x, y] == self.State.SUSCEPTIBLE:
            # Expose
            infectedCount = neighbours.count(self.State.EXPOSED)
            compounded = 1 - (1 - self.beta) ** infectedCount # TODO: Can be precalculated
            if random.random() < compounded:
                return self.State.EXPOSED
        elif self.grid[x, y] == self.State.EXPOSED:
            # Sicken
            if random.random() < self.theta:
                return self.State.INFECTIOUS
        elif self.grid[x, y] == self.State.INFECTIOUS:
            pass
        return self.grid[x, y]
