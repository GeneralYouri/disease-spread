import matplotlib.pyplot as plt
import numpy as np
import time
from enum import IntEnum
import neighborhood


# Plot line colors for visualisation purposes
# TODO: Better tie these to States
colors = ['purple', 'red', 'orange', 'yellow', 'green']


# Abstract Base Class for the various CA Models for disease spread
class Base:
    size = 0
    center = 0
    
    hasEnded = False
    time = 0
    grid = np.empty(0)
    history = []
    
    # Define the available States in this model
    class State(IntEnum):
        INFECTIOUS = 0,

    def __init__(self, strategy, r, **settings):
        for name, value in settings.items():
            setattr(self, name, value)
        self.center = round(self.size / 2)
        self.setNeighborhood(strategy, r)

        self.initialize()
        self.history.append(self.getCounts())
    
    # Define the model's cell neighborhood, from the given strategy and range
    def setNeighborhood(self, strategy, r):
        if strategy == neighborhood.Strategy.MOORE:
            self.neighborhood = neighborhood.moore(r)
        elif strategy == neighborhood.Strategy.NEUMANN:
            self.neighborhood = neighborhood.neumann(r)
    
    # Create the initial grid state
    def initialize(self):
        self.grid = np.full([self.size, self.size], self.State.INFECTIOUS)
    
    # Continuously advance the simulation until the pandemic ends (0 Infectious)
    def runToEnd(self, maxSteps = 0):
        if self.hasEnded == True:
            return
        for _ in range(0, maxSteps):
            if self.history[-1][self.State.INFECTIOUS.name] == 0:
                self.hasEnded = True
                return
            self.step()
    
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
    
    # Count the number of infected cells in the cell's specified neighborhood
    def countInfectedNeighbors(self, x, y):
        count = 0
        for dx, dy in self.neighborhood:
            if self.grid[(x + dx) % self.size, (y + dy) % self.size] == self.State.INFECTIOUS:
                count += 1
        return count
    
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
    def plotSummary(self, save = True, show = False):
        times = range(0, len(self.history))
        counts = {state: [t[state] for t in self.history] for state in self.history[0]}
        
        for state in self.history[0]:
            plt.plot(times, counts[state], label=state, color=colors[self.State[state]])
        plt.xlabel('Time')
        plt.ylabel('Proportion')
        plt.title(f'{self.__class__.__name__} Model')
        plt.legend()
        plt.grid(True)
        timestamp = int(time.time())
        if save:
            plt.savefig(f'plots/plot_summary_{timestamp}')
        if show:
            plt.show()
