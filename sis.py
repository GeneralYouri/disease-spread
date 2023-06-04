import random
from si import *


class SIS(SI):
    alpha = 0
    
    # Calculate the new state for the cell at the given coordinates
    def updateCell(self, x, y):
        neighbours = self.getNeighbours(x, y)
        if self.grid[x, y] == self.State.SUSCEPTIBLE:
            # Sicken
            infectedCount = neighbours.count(self.State.INFECTIOUS)
            compounded = 1 - (1 - self.beta) ** infectedCount # TODO: Can be precalculated
            if random.random() < compounded:
                return self.State.INFECTIOUS
        elif self.grid[x, y] == self.State.INFECTIOUS:
            if random.random() < self.alpha:
                return self.State.SUSCEPTIBLE
        return self.grid[x, y]
