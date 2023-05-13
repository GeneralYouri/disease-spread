import numpy as np
import random
from enum import IntEnum
from numba import njit


# SIR
class State(IntEnum):
    SUSCEPTIBLE = 0,
    INFECTED = 1,
    RECOVERED = 2,


# njit methods must be defined outside the class environment
# Advance the model one step forwards and update all cells
@njit
def step(a, p, size, grid):
    nextGrid = np.copy(grid)
    
    for y in range(1, size - 1):
        for x in range(1, size - 1):
            if grid[x, y] == State.SUSCEPTIBLE:
                # Be infected
                # TODO: Count Infected neighbours, roll once each
                if random.random() > a:
                    nextGrid[x, y] = State.INFECTED
            elif grid[x, y] == State.INFECTED:
                # Recover
                if random.random() > p:
                    nextGrid[x, y] = State.RECOVERED
    
    return nextGrid

class Model:
    a = 1 # Infection rate
    p = 1 # Recovery rate
    
    grid = np.empty(0)
    size = 0
    center = 0
    time = 0
    
    def __init__(self, size, a = 0, p = 0):
        self.size = size
        self.center = round(self.size / 2)
        self.a = a
        self.p = p
        
        self.grid = np.full([size, size], State.SUSCEPTIBLE)
        self.clearEdges()
        self.grid[self.center, self.center] = State.INFECTED
    
    # Reset edge cells
    def clearEdges(self):
        for i in range(0, self.size):
            self.grid[i, 0] = State.SUSCEPTIBLE
            self.grid[0, i] = State.SUSCEPTIBLE
            self.grid[i, self.size - 1] = State.SUSCEPTIBLE
            self.grid[self.size - 1, i] = State.SUSCEPTIBLE
    
    # Advance the model one step forwards and update all cells
    def step(self):
        grid = step(self.a, self.p, self.size, self.grid)
        self.grid = grid
        self.time += 1
