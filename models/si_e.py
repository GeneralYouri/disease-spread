import random
from enum import IntEnum
from .si import *


class SI_E(SI):
    delta = 0
    
    class State(IntEnum):
        SUSCEPTIBLE = 0
        EXPOSED = 1
        INFECTIOUS = 2
    
    def updateCell(self, x, y):
        cell = self.grid[x, y]
        if cell == self.State.SUSCEPTIBLE:
            # Expose
            infectedCount = self.countInfectedNeighbors(x, y)
            compounded = 1 - (1 - self.beta) ** infectedCount # TODO: Can be precalculated
            if random.random() < compounded:
                return self.State.EXPOSED
        elif cell == self.State.EXPOSED:
            # Sicken
            if random.random() < self.delta:
                return self.State.INFECTIOUS
        elif cell == self.State.INFECTIOUS:
            pass
        return cell
