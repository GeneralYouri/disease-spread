from .si_e import *


class SIS_E(SI_E):
    alpha = 0
    
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
            # Re-susceptibility
            if self.rng.random() < self.alpha:
                return self.State.SUSCEPTIBLE
        return cell
