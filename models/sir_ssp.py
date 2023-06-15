import numpy as np
import random
import neighborhood
from .sir import *


class SIR_SSP(SIR):
    neighborDeltas2 = np.empty(0)
    superspreaders = 0
    isSSP = np.empty(0)
    
    def __init__(self, settings):
        super().__init__(settings)
        
        # Compute Super Spreader neighborhood
        self.neighborhood2 = self.neighborhood
        self.range2 = self.range + 1
        self.neighborDeltas2 = getattr(neighborhood, self.neighborhood2)(self.range2)
        
        # Generate Super Spreaders
        self.isSSP = np.full(self.grid.shape, False, dtype=bool)
        
        # Turn a fraction of cells into Super Spreaders
        cellCount = round(self.superspreaders * self.size ** 2)
        for _ in range(0, cellCount):
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            while (self.grid[x, y] == self.State.INFECTIOUS):
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
            self.isSSP[x, y] = True
    
    # Count the number of infected cells in the cell's specified neighborhood
    def countInfectedNeighbors(self, x, y):
        count = 0
        for dx, dy in self.neighborDeltas:
            nx = (x + dx) % self.size
            ny = (y + dy) % self.size
            if self.grid[nx, ny] == self.State.INFECTIOUS and not self.isSSP[nx, ny]:
                count += 1
        for dx, dy in self.neighborDeltas2:
            nx = (x + dx) % self.size
            ny = (y + dy) % self.size
            if self.grid[nx, ny] == self.State.INFECTIOUS and self.isSSP[nx, ny]:
                count += 1
        return count
