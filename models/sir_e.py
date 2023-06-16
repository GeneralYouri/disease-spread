from enum import IntEnum
from .si_e import *


class SIR_E(SI_E):
    gamma = 0

    class State(IntEnum):
        SUSCEPTIBLE = 0
        EXPOSED = 1
        INFECTIOUS = 2
        RECOVERED = 3
    
    def updateCell(self, x, y):
        cell = self.grid[x, y]
        if cell == self.State.SUSCEPTIBLE:
            # Exposure
            infectedCount = self.countInfectedNeighbors(x, y)
            compounded = 1 - (1 - self.beta) ** infectedCount # TODO: Can be precalculated
            if self.rng.random() < compounded:
                return self.State.EXPOSED
        elif cell == self.State.EXPOSED:
            # Sicken
            if self.rng.random() < self.delta:
                return self.State.INFECTIOUS
        elif cell == self.State.INFECTIOUS:
            # Recover
            if self.rng.random() < self.gamma:
                return self.State.RECOVERED
        elif cell == self.State.RECOVERED:
            pass
        return cell
