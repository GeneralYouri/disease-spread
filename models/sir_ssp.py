import numpy as np
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
        self.neighborDeltas2 = getattr(neighborhood, self.neighborhood2)(2)
        
        # Generate Super Spreaders
        self.isSSP = np.full(self.grid.shape, False, dtype=bool)
        
        # Turn a fraction of cells into Super Spreaders
        cellCount = round(self.superspreaders * self.size ** 2)
        for _ in range(0, cellCount):
            x = self.rng.integers(0, self.size)
            y = self.rng.integers(0, self.size)
            while (self.grid[x, y] == self.State.INFECTIOUS):
                x = self.rng.integers(0, self.size)
                y = self.rng.integers(0, self.size)
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
