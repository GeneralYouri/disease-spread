import random
from enum import IntEnum
from si import *


class SIR(SI):
    gamma = 0

    class State(IntEnum):
        SUSCEPTIBLE = 0,
        INFECTIOUS = 1,
        RECOVERED = 2,
    
    def updateCell(self, x, y):
        neighbours = self.getNeighbours(x, y)
        if self.grid[x, y] == self.State.SUSCEPTIBLE:
            # Sicken
            infectedCount = neighbours.count(self.State.INFECTIOUS)
            compounded = 1 - (1 - self.beta) ** infectedCount # TODO: Can be precalculated
            if random.random() < compounded:
                return self.State.INFECTIOUS
        elif self.grid[x, y] == self.State.INFECTIOUS:
            # Recover
            if random.random() < self.gamma:
                return self.State.RECOVERED
        elif self.grid[x, y] == self.State.RECOVERED:
            pass
        return self.grid[x, y]
