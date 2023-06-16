from .sir_hd import *


class SIRS_HD(SIR_HD):
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
            if self.rng.random() < self.epsilon: # alpha
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
            if self.rng.random() < self.epsilon: # xi
                self.beds -= 1
                return self.State.RECOVERED
        elif cell == self.State.RECOVERED:
            # Re-susceptibility
            if self.rng.random() < self.alpha:
                return self.State.SUSCEPTIBLE
        elif cell == self.State.DEAD:
            pass
        return cell
