import numpy as np
import random
from enum import IntEnum
from base import *


class SI(Base):
    beta = 0
    
    class State(IntEnum):
        SUSCEPTIBLE = 0
        INFECTIOUS = 1
    
    # TODO: Add different starting strategies
    def initialize(self):
        self.grid = np.full([self.size, self.size], self.State.SUSCEPTIBLE)
        
        # Start by infecting the center cell
        # self.grid[self.center, self.center] = self.State.INFECTED
        
        # Start by infecting 10% of cells randomly
        initial = round(self.size * self.size / 10)
        for _ in range(0, initial):
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            while (self.grid[x, y] == self.State.INFECTIOUS):
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
            self.grid[x, y] = self.State.INFECTIOUS
    
    # Calculate the new state for the cell at the given coordinates
    def updateCell(self, x, y):
        if self.grid[x, y] == self.State.SUSCEPTIBLE:
            # Sicken
            infectedCount = self.countInfectedNeighbors(x, y)
            compounded = 1 - (1 - self.beta) ** infectedCount # TODO: Can be precalculated
            if random.random() < compounded:
                return self.State.INFECTIOUS
        elif self.grid[x, y] == self.State.INFECTIOUS:
            pass
        return self.grid[x, y]
