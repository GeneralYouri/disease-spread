import numpy as np
from enum import IntEnum
from base import *


class SI(Base):
    initial = 0
    beta = 0
    
    class State(IntEnum):
        SUSCEPTIBLE = 0
        INFECTIOUS = 1
    
    # TODO: Add different starting strategies
    def initialize(self):
        self.grid = np.full((self.size, self.size), self.State.SUSCEPTIBLE)
        
        if self.initial == 0 or self.initial > 1:
            # Start by infecting the center cell
            self.grid[self.center - 1 : self.center + 2, self.center - 1 : self.center + 2] = self.State.INFECTIOUS
        else:
            # Start by infecting a fraction of cells randomly
            cellCount = round(self.initial * self.size ** 2)
            for _ in range(0, cellCount):
                x = self.rng.integers(0, self.size)
                y = self.rng.integers(0, self.size)
                while (self.grid[x, y] == self.State.INFECTIOUS):
                    x = self.rng.integers(0, self.size)
                    y = self.rng.integers(0, self.size)
                self.grid[x, y] = self.State.INFECTIOUS
    
    # Calculate the new state for the cell at the given coordinates
    def updateCell(self, x, y):
        cell = self.grid[x, y]
        if cell == self.State.SUSCEPTIBLE:
            # Sicken
            infectedCount = self.countInfectedNeighbors(x, y)
            compounded = 1 - (1 - self.beta) ** infectedCount # TODO: Can be precalculated
            if self.rng.random() < compounded:
                return self.State.INFECTIOUS
        elif cell == self.State.INFECTIOUS:
            pass
        return cell
