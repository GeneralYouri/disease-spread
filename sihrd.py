import random
from sihr import *


class SIHRD(SIHR):
    epsilon = 0
    beds = 0
    maxbeds = 0

    class State(IntEnum):
        SUSCEPTIBLE = 0
        INFECTIOUS = 1
        HOSPITALIZED = 2
        RECOVERED = 3
        DEAD = 4
    
    def updateCell(self, x, y):
        if self.grid[x, y] == self.State.SUSCEPTIBLE:
            # Sicken
            infectedCount = self.countInfectedNeighbors(x, y)
            compounded = 1 - (1 - self.beta) ** infectedCount # TODO: Can be precalculated
            if random.random() < compounded:
                return self.State.INFECTIOUS
        elif self.grid[x, y] == self.State.INFECTIOUS:
            # Hospitalize
            if random.random() < self.epsilon:
                if self.beds < self.maxbeds:
                    self.beds += 1
                    return self.State.HOSPITALIZED
                else:
                    return self.State.DEAD
            # Recover
            elif random.random() < self.gamma:
                return self.State.RECOVERED
        elif self.grid[x, y] == self.State.HOSPITALIZED:
            # Recover
            if random.random() < self.epsilon:
                self.beds -= 1
                return self.State.RECOVERED
        elif self.grid[x, y] == self.State.RECOVERED:
            # Re-susceptibility
            if random.random() < self.alpha:
                return self.State.SUSCEPTIBLE
        elif self.grid[x, y] == self.State.DEAD:
            pass
        return self.grid[x, y]
