import random
from enum import IntEnum
from si import *


class SEI(SI):
    delta = 0
    
    class State(IntEnum):
        SUSCEPTIBLE = 0
        EXPOSED = 1
        INFECTIOUS = 0
    
    def updateCell(self, x, y):
        if self.grid[x, y] == self.State.SUSCEPTIBLE:
            # Expose
            infectedCount = self.countInfectedNeighbors(x, y)
            compounded = 1 - (1 - self.beta) ** infectedCount # TODO: Can be precalculated
            if random.random() < compounded:
                return self.State.EXPOSED
        elif self.grid[x, y] == self.State.EXPOSED:
            # Sicken
            if random.random() < self.delta:
                return self.State.INFECTIOUS
        elif self.grid[x, y] == self.State.INFECTIOUS:
            pass
        return self.grid[x, y]
