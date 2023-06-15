import numpy as np
import random
from .sir import *


class SIR_SSH(SIR):
    supershedders = 0
    isSSH = np.empty(0)
    
    def __init__(self, settings):
        super().__init__(settings)
        
        # Generate Super Spreaders
        self.isSSH = np.full(self.grid.shape, False, dtype=bool)
        
        # Turn a fraction of cells into Super Shedders
        cellCount = round(self.supershedders * self.size ** 2)
        for _ in range(0, cellCount):
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            while (self.grid[x, y] == self.State.INFECTIOUS):
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
            self.isSSH[x, y] = True
    
    # Count the number of infected cells in the cell's specified neighborhood
    def countInfectedNeighbors(self, x, y):
        count = 0
        for dx, dy in self.neighborDeltas:
            nx = (x + dx) % self.size
            ny = (y + dy) % self.size
            if self.grid[nx, ny] == self.State.INFECTIOUS:
                count += 1 + 2 * int(self.isSSH[nx, ny])
        return count
