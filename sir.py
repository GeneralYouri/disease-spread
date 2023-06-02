import numpy as np
import random
from enum import IntEnum
from model import *


class SIR(Model):
    class State(IntEnum):
        SUSCEPTIBLE = 0,
        INFECTED = 1,
        RECOVERED = 2,

    def __init__(self, size, beta = 0, gamma = 0, neighborStrategy = NeighborStrategy.NEUMANN):
        super().__init__(size, beta, gamma, neighborStrategy)
        
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
        
        # Start by infecting 10% of cells
        initial = round(self.size * self.size / 10)
        for i in range(0, initial):
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            while (self.grid[x, y] == self.State.INFECTED):
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
            self.grid[x, y] = self.State.INFECTED
        self.history.append({
            self.State.SUSCEPTIBLE.name: self.size * self.size - initial,
            self.State.INFECTED.name: initial,
            self.State.RECOVERED.name: 0,
        })
    
    # Calculate the new state for the cell at the given coordinates
    def updateCell(self, x, y):
        neighbours = self.getNeighbours(x, y)
        if self.grid[x, y] == self.State.SUSCEPTIBLE:
            # Be infected
            infected = neighbours.count(self.State.INFECTED)
            compounded = 1 - (1 - self.beta) ** infected # TODO: Can be precalculated
            if random.random() < compounded:
                return self.State.INFECTED
        elif self.grid[x, y] == self.State.INFECTED:
            # Recover
            if random.random() < self.gamma:
                return self.State.RECOVERED
        return self.grid[x, y]
