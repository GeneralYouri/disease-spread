import numpy as np
import random
from enum import IntEnum
from si import *


class SIR(SI):
    class State(IntEnum):
        SUSCEPTIBLE = 0,
        INFECTIOUS = 1,
        RECOVERED = 2,
    
    # TODO: Add different starting strategies
    def initialize(self):
        self.grid = np.full([self.size, self.size], self.State.SUSCEPTIBLE)
        
        # Start by infecting the center cell
        # self.grid[self.center, self.center] = self.State.INFECTED
        # self.history.append({
        #     self.State.SUSCEPTIBLE.name: size * size - 1,
        #     self.State.INFECTED.name: 1,
        #     self.State.RECOVERED.name: 0,
        # })
        
        # Start by infecting 10% of cells randomly
        initial = round(self.size * self.size / 10)
        for _ in range(0, initial):
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            while (self.grid[x, y] == self.State.INFECTIOUS):
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
            self.grid[x, y] = self.State.INFECTIOUS
        self.history.append({
            self.State.SUSCEPTIBLE.name: self.size * self.size - initial,
            self.State.INFECTIOUS.name: initial,
            self.State.RECOVERED.name: 0,
        })
    
    # Calculate the new state for the cell at the given coordinates
    def updateCell(self, x, y):
        neighbours = self.getNeighbours(x, y)
        if self.grid[x, y] == self.State.SUSCEPTIBLE:
            # Sicken
            infectedCount = neighbours.count(self.State.INFECTIOUS)
            compounded = 1 - (1 - self.beta) ** infectedCount # TODO: Can be precalculated
            if random.random() < compounded:
                return self.State.INFECTIOUS
        elif self.grid[x, y] == self.State.INFECTIOUS:
            # Recover
            if random.random() < self.gamma:
                return self.State.RECOVERED
        elif self.grid[x, y] == self.State.RECOVERED:
            pass
        return self.grid[x, y]
