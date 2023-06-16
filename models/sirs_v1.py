from .sir_v1 import *


class SIRS_V1(SIR_V1):
    def updateCell(self, x, y):
        cell = self.grid[x, y]
        if cell == self.State.SUSCEPTIBLE:
            # Vaccinate
            if self.time >= self.vaccinationDelay and self.rng.random() < self.zeta:
                return self.State.VACCINATED
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
        elif cell == self.State.VACCINATED:
            # Sicken
            infectedCount = self.countInfectedNeighbors(x, y)
            compounded = 1 - (1 - self.beta2) ** infectedCount # TODO: Can be precalculated
            if self.rng.random() < compounded:
                return self.State.INFECTIOUS
        return cell
