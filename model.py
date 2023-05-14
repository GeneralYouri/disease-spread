import numpy as np
import random
from enum import Enum, IntEnum
from numba import njit


# SIR
class State(IntEnum):
    SUSCEPTIBLE = 0,
    INFECTED = 1,
    RECOVERED = 2,


# Specify the neighborhood type for the model
class NeighborStrategy(Enum):
    NEUMANN = 'Neumann',
    MOORE = 'Moore',

# Create a method for getting cell neighbors depending on the given strategy
# TODO: Make iterable?
# TODO: Add range
class GetNeighborsFactory:
    def Create(strategy):
        if strategy == NeighborStrategy.NEUMANN:
            return GetNeighborsFactory.Neumann
        if strategy == NeighborStrategy.MOORE:
            return GetNeighborsFactory.Moore
    
    @staticmethod
    def Moore(self, x, y):
        return [
            *GetNeighborsFactory.Neumann(self, x, y),
            self.grid[x - 1, y - 1],
            self.grid[x + 1, y - 1],
            self.grid[x - 1, y + 1],
            self.grid[x + 1, y + 1],
        ]
        
    @staticmethod
    def Neumann(self, x, y):
        return [
            self.grid[x, y - 1],
            self.grid[x - 1, y],
            self.grid[x + 1, y],
            self.grid[x, y + 1],
        ]


# njit methods must be defined outside the class environment
# Advance the model one step forwards and update all cells
@njit
def step(a, p, size, grid):
    nextGrid = np.copy(grid)
    
    for y in range(0, size):
        for x in range(0, size):
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
    
    def __init__(self, size, a = 0, p = 0, neighborStrategy = NeighborStrategy.NEUMANN):
        self.size = size
        self.center = round(self.size / 2)
        self.a = a
        self.p = p
        self.setNeighborStrategy(neighborStrategy)
        
        self.grid = np.full([size, size], State.SUSCEPTIBLE)
        self.grid[self.center, self.center] = State.INFECTED
    
    def setNeighborStrategy(self, neighborStrategy):
        self.getNeighborMethod = GetNeighborsFactory.Create(neighborStrategy)
    
    # Advance the model one step forwards and update all cells
    def step(self):
        grid = step(self.a, self.p, self.size, self.grid)
        self.grid = grid
        self.time += 1
    
    # Get neighborhood cells for a given grid coordinate, using the Model's Neighborhood Strategy
    def getNeighbours(self, x, y):
        return self.getNeighborMethod(self, x, y)
