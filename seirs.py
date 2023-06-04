import random
from seir import *
from seis import *


class SEIRS(SEIR, SEIS):
    def updateCell(self, x, y):
        if self.grid[x, y] == self.State.SUSCEPTIBLE:
            # Exposure
            infectedCount = self.countInfectedNeighbors(x, y)
            compounded = 1 - (1 - self.beta) ** infectedCount # TODO: Can be precalculated
            if random.random() < compounded:
                return self.State.EXPOSED
        elif self.grid[x, y] == self.State.EXPOSED:
            # Sicken
            if random.random() < self.theta:
                return self.State.INFECTIOUS
        elif self.grid[x, y] == self.State.INFECTIOUS:
            # Recover
            if random.random() < self.gamma:
                return self.State.RECOVERED
        elif self.grid[x, y] == self.State.RECOVERED:
            # Re-susceptibility
            if random.random() < self.alpha:
                return self.State.SUSCEPTIBLE
        return self.grid[x, y]