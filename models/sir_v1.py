import random
from enum import IntEnum
from .sir import *


class SIR_V1(SIR):
    zeta = 0
    vaccinationFactor = 0
    vaccinationDelay = 0

    class State(IntEnum):
        SUSCEPTIBLE = 0
        INFECTIOUS = 1
        RECOVERED = 2
        VACCINATED = 3
    
    def __init__(self, settings):
        super().__init__(settings)
        beta = 1 - (1 - self.beta) ** len(self.neighborhood)
        beta2 = beta * self.vaccinationFactor
        self.beta2 = 1 - (1 - beta2) ** (1 / len(self.neighborhood))
    
    def updateCell(self, x, y):
        cell = self.grid[x, y]
        if cell == self.State.SUSCEPTIBLE:
            # Vaccinate
            if self.time >= self.vaccinationDelay and random.random() < self.zeta:
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
            pass
        elif cell == self.State.VACCINATED:
            # Sicken
            infectedCount = self.countInfectedNeighbors(x, y)
            compounded = 1 - (1 - self.beta2) ** infectedCount # TODO: Can be precalculated
            if random.random() < compounded:
                return self.State.INFECTIOUS
        return cell
