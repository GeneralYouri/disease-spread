from .sir_h import *


class SIRS_H(SIR_H):
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
                return self.State.HOSPITALIZED
            # Recover
            if self.rng.random() < self.gamma:
                return self.State.RECOVERED
        elif cell == self.State.HOSPITALIZED:
            # Recover
            if self.rng.random() < self.gamma / 2:
                return self.State.RECOVERED
        elif cell == self.State.RECOVERED:
            # Re-susceptibility
            if self.rng.random() < self.alpha:
                return self.State.SUSCEPTIBLE
        return cell
