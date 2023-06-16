from .sir_ssp import *


class SIRS_SSP(SIR_SSP):
    def updateCell(self, x, y):
        cell = self.grid[x, y]
        if cell == self.State.SUSCEPTIBLE:
            # Sicken
            infectedCount = self.countInfectedNeighbors(x, y)
            compounded = 1 - (1 - self.beta) ** infectedCount # TODO: Can be precalculated
            if self.rng.random() < compounded:
                return self.State.INFECTIOUS
        elif cell == self.State.INFECTIOUS:
            # Recover
            if self.rng.random() < self.gamma:
                return self.State.RECOVERED
        elif cell == self.State.RECOVERED:
            # Re-susceptibility
            if self.rng.random() < self.alpha:
                return self.State.SUSCEPTIBLE
        return cell
