import matplotlib.pyplot as plt
import numpy as np
import time
from enum import Enum, IntEnum


# Plot line colors for visualisation purposes
# TODO: Better tie these to States
colors = ['purple', 'red', 'orange']


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


# Abstract Base Class for the various CA Models for disease spread
class Model:
    size = 0
    center = 0
    
    time = 0
    grid = np.empty(0)
    history = []
    
    class State(IntEnum):
        DEFAULT = 0,

    def __init__(self, neighborStrategy = NeighborStrategy.NEUMANN, **settings):
        for name, value in settings.items():
            setattr(self, name, value)
        self.center = round(self.size / 2)
        self.setNeighborStrategy(neighborStrategy)

        self.initialize()
        self.history.append(self.getCounts())
    
    # Create the initial grid state
    def initialize(self):
        self.grid = np.full([self.size, self.size], self.State.DEFAULT)
    
    # Apply the given neighbor strategy to the model
    def setNeighborStrategy(self, neighborStrategy):
        self.getNeighborMethod = GetNeighborsFactory.Create(neighborStrategy)
    
    # Get neighborhood cells for a given grid coordinate, using the Model's Neighborhood Strategy
    def getNeighbours(self, x, y):
        return self.getNeighborMethod(self, x, y)
    
    # Advance the model one step forwards and update all cells
    def step(self):
        nextGrid = np.copy(self.grid)
        
        for y in range(0, self.size):
            for x in range(0, self.size):
                newState = self.updateCell(x, y)
                nextGrid[x, y] = newState
        
        self.grid = nextGrid
        self.history.append(self.getCounts())
        self.time += 1
    
    # Calculate the new state for the cell at the given coordinates
    def updateCell(self, x, y):
        return self.grid[x, y]
    
    # Count the number of cells in each State in the current grid
    def getCounts(self):
        counts = {}
        for state in self.State:
            counts[state.name] = 0
        for y in range(0, self.size):
            for x in range(0, self.size):
                counts[self.State(self.grid[x, y]).name] += 1
        return counts
    
    # Plot summary/history data of the simulation so far
    def plotSummary(self):
        times = range(0, len(self.history))
        counts = {state: [t[state] for t in self.history] for state in self.history[0]}
        
        for state in self.history[0]:
            plt.plot(times, counts[state], label=state, color=colors[self.State[state]])
        plt.xlabel('Time')
        plt.ylabel('Proportion')
        plt.title('SIR Model')
        plt.legend()
        plt.grid(True)
        timestamp = int(time.time() * 1000)
        plt.savefig(f'plots/plot_summary_{timestamp}')
        # plt.show()
