import numpy as np
from enum import IntEnum
import neighborhood


# Abstract Base Class for the various CA Models for disease spread
class Base:
    size = 0
    center = 0
    neighborDeltas = np.empty(0)
    
    hasEnded = False
    time = 0
    grid = np.empty((0, 0))
    history = np.empty(0)
    
    # Available Cell States for this Model
    class State(IntEnum):
        INFECTIOUS = 0

    def __init__(self, settings):
        for name, value in settings.__dict__.items():
            setattr(self, name, value)
        
        ## Post-processing
        self.center = round(self.size / 2)
        # Compute neighborhood
        self.neighborDeltas = getattr(neighborhood, self.neighborhood)(1)
        # Adjust beta to account for neighborhood
        self.beta = 1 - (1 - self.beta) ** (1 / len(self.neighborDeltas))
        # Apply the maxBeds fraction to the model size and get a flat amount
        self.maxBeds = self.maxBeds * self.size ** 2
        # Apply the maxVaccines fraction to the model size and get a flat amount
        self.maxVaccines = self.maxVaccines * self.size ** 2
        
        self.initialize()
        self.history = np.append(self.history, self.getCounts())
    
    # Create the initial grid state
    def initialize(self):
        self.grid = np.full((self.size, self.size), self.State.INFECTIOUS)
    
    # Continuously advance the simulation until the pandemic ends (0 Infectious)
    def runToEnd(self, maxSteps = 1):
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
        self.history = np.append(self.history, self.getCounts())
        self.time += 1
        
        # Apply Intervention
        if self.time == self.interventionDelay:
            self.beta = 1 - (1 - self.beta) ** len(self.neighborDeltas)
            self.beta *= self.interventionFactor
            self.beta = 1 - (1 - self.beta) ** (1 / len(self.neighborDeltas))
    
    # Calculate the new state for the cell at the given coordinates
    def updateCell(self, x, y):
        return self.grid[x, y]
    
    # Count the number of infected cells in the cell's specified neighborhood
    def countInfectedNeighbors(self, x, y):
        count = 0
        for dx, dy in self.neighborDeltas:
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
