import random
from .sir_v1 import *


class SIR_V2(SIR_V1):
    maxVaccines = 0 # K
    vaccines = 0

    def updateCell(self, x, y):
        cell = self.grid[x, y]
        if cell == self.State.SUSCEPTIBLE:
            # Vaccinate
            adjustedZeta = self.zeta * (1 - self.vaccines / self.maxVaccines)
            if self.time >= self.vaccinationDelay and random.random() < adjustedZeta:
                self.vaccines += 1
                return self.State.VACCINATED
            # Sicken
            infectedCount = self.countInfectedNeighbors(x, y)
            compounded = 1 - (1 - self.beta) ** infectedCount # TODO: Can be precalculated
            if random.random() < compounded:
                return self.State.INFECTIOUS
        elif cell == self.State.INFECTIOUS:
            # Recover
            if random.random() < self.gamma:
                return self.State.RECOVERED
        elif cell == self.State.RECOVERED:
            # Vaccinate
            adjustedZeta = self.zeta * (1 - self.vaccines / self.maxVaccines)
            if self.time >= self.vaccinationDelay and random.random() < adjustedZeta:
                self.vaccines += 1
                return self.State.VACCINATED
        elif cell == self.State.VACCINATED:
            pass
        return cell
