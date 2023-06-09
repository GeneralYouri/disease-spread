from .sir_h import *


class SIR_HD(SIR_H):
    epsilon = 0
    beds = 0
    maxBeds = 0

    class State(IntEnum):
        SUSCEPTIBLE = 0
        INFECTIOUS = 1
        HOSPITALIZED = 2
        RECOVERED = 3
        DEAD = 4
    
    def updateCell(self, x, y):
        cell = self.grid[x, y]
        if cell == self.State.SUSCEPTIBLE:
            # Sicken
            infectedCount = self.countInfectedNeighbors(x, y)
            compounded = 1 - (1 - self.beta) ** infectedCount # TODO: Can be precalculated
            if self.rng.random() < compounded:
                return self.State.INFECTIOUS
        elif cell == self.State.INFECTIOUS:
            # Hospitalize
            if self.rng.random() < self.epsilon:
                if self.beds < self.maxBeds:
                    self.beds += 1
                    return self.State.HOSPITALIZED
                else:
                    return self.State.DEAD
            # Recover
            elif self.rng.random() < self.gamma:
                return self.State.RECOVERED
        elif cell == self.State.HOSPITALIZED:
            # Recover
            if self.rng.random() < self.epsilon:
                self.beds -= 1
                return self.State.RECOVERED
        elif cell == self.State.RECOVERED:
            pass
        elif cell == self.State.DEAD:
            pass
        return cell
