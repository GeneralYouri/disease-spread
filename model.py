import matplotlib.pyplot as plt
import numpy as np
import random
from enum import Enum, IntEnum
# from numba import njit


# SIR
# TODO: Add more state types
class State(IntEnum):
    SUSCEPTIBLE = 0,
    INFECTED = 1,
    RECOVERED = 2,


# Plot SIR
def plotSummary(history):
    counts = {state: [t[state] for t in history] for state in history[0]}
    
    plt.plot(counts[State.SUSCEPTIBLE.name], 'black', lw = 2.0)
    plt.plot(counts[State.INFECTED.name], 'red', lw = 2.0)
    plt.plot(counts[State.RECOVERED.name], 'blue', lw = 2.0)
    plt.xlabel('Time')
    plt.ylabel('SIR')
    plt.show()


# Specify the neighborhood type for the model
class NeighborStrategy(Enum):
    NEUMANN = 'Neumann',
    MOORE = 'Moore',

# Create a method for getting cell neighbors depending on the given strategy
# TODO: Make iterable?
# TODO: Add a neighborhood range variable
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
            self.grid[(x + 1) % self.size, y - 1],
            self.grid[x - 1, (y + 1) % self.size],
            self.grid[(x + 1) % self.size, (y + 1) % self.size],
        ]
        
    @staticmethod
    def Neumann(self, x, y):
        return [
            self.grid[x, y - 1],
            self.grid[x - 1, y],
            self.grid[(x + 1) % self.size, y],
            self.grid[x, (y + 1) % self.size],
        ]


class Model:
    size = 0
    center = 0
    beta = 1 # Infection rate
    gamma = 1 # Recovery rate
    
    grid = np.empty(0)
    neighbors = np.empty(0)
    
    time = 0
    history = []
    
    def __init__(self, size, beta = 0, gamma = 0, neighborStrategy = NeighborStrategy.NEUMANN):
        self.size = size
        self.center = round(self.size / 2)
        self.beta = beta
        self.gamma = gamma
        self.setNeighborStrategy(neighborStrategy)
        
        self.grid = np.full([size, size], State.SUSCEPTIBLE)
        # Start by infecting the center cell
        # TODO: Add different starting strategies
        self.grid[self.center, self.center] = State.INFECTED
        self.history.append({
            State.SUSCEPTIBLE.name: size * size - 1,
            State.INFECTED.name: 1,
            State.RECOVERED.name: 0,
        })
    
    def setNeighborStrategy(self, neighborStrategy):
        self.getNeighborMethod = GetNeighborsFactory.Create(neighborStrategy)
    
    # Advance the model one step forwards and update all cells
    def step(self):
        nextGrid = np.copy(self.grid)
        counts = {}
        for state in State:
            counts[state.name] = 0
        
        for y in range(0, self.size):
            for x in range(0, self.size):
                newState = self.updateCell(x, y)
                nextGrid[x, y] = newState
                counts[State(newState).name] += 1
        
        self.grid = nextGrid
        self.history.append(counts)
        self.time += 1
    
    # Calculate the new state for the cell at the given coordinates
    def updateCell(self, x, y):
        neighbours = self.getNeighbours(x, y)
        if self.grid[x, y] == State.SUSCEPTIBLE:
            # Be infected
            infected = neighbours.count(State.INFECTED)
            failRate = (1 - self.beta) ** infected # TODO: Can be precalculated
            if random.random() > failRate:
                return State.INFECTED
        elif self.grid[x, y] == State.INFECTED:
            # Recover
            if random.random() > self.gamma:
                return State.RECOVERED
        return self.grid[x, y]
    
    # Get neighborhood cells for a given grid coordinate, using the Model's Neighborhood Strategy
    def getNeighbours(self, x, y):
        return self.getNeighborMethod(self, x, y)
