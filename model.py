import numpy as np
import random
from enum import Enum
from numba import njit


# Specify how to add Sand to the model
class SandStrategy(Enum):
    RANDOM = 'Random',
    CENTER = 'Center',
    EDGES = 'Edges',

# Create a method for adding Sand depending on the given strategy
class AddSandFactory:
    def Create(strategy):
        if strategy == SandStrategy.RANDOM:
            return AddSandFactory.Random
        if strategy == SandStrategy.CENTER:
            return AddSandFactory.Center
        if strategy == SandStrategy.EDGES:
            return AddSandFactory.Edges
    
    @staticmethod
    def Random(self):
        x = random.randint(1, self.size - 2)
        y = random.randint(1, self.size - 2)
        self.grid[x, y] += 1

    @staticmethod
    def Center(self):
        self.grid[self.center, self.center] += 1
    
    @staticmethod
    def Edges(self):
        a = random.randint(0, 1) # Orientation (horizontal or vertical)
        b = 1 + (self.size - 2) * random.randint(0, 1) # Side (up/down or left/right)
        c = random.randint(1, self.size - 2) # Offset (position on the side)
        [x, y] = [b, c] if a == 0 else [c, b]
        self.grid[x, y] += 1


# njit methods must be defined outside the class environment
# Advance the model one step forwards and update all cells
@njit
def step(K, size, grid):
    nextGrid = np.copy(grid)
    stable = True
    topples = 0
    
    for y in range(1, size - 1):
        for x in range(1, size - 1):
            if grid[x, y] > K:
                #Topple
                stable = False
                topples += 1
                nextGrid[x, y] -= 4
                nextGrid[x - 1, y] += 1
                nextGrid[x + 1, y] += 1
                nextGrid[x, y - 1] += 1
                nextGrid[x, y + 1] += 1
    
    return (nextGrid, stable, topples)

class Model:
    K = 3
    
    grid = np.empty(0)
    size = 0
    center = 0
    stable = False
    time = 0
    topples = 0
    
    def __init__(self, size, sandStrategy = SandStrategy.RANDOM):
        self.setSandStrategy(sandStrategy)
        self.size = size
        self.center = round(self.size / 2)
        self.grid = np.full([size, size], 7)
        self.clearEdges()
    
    def setSandStrategy(self, sandStrategy):
        self.addSandMethod = AddSandFactory.Create(sandStrategy)
    
    # Shorthand to avoid class/self confusion
    def addSand(self):
        self.addSandMethod(self)
    
    # Set edge cells to 0
    def clearEdges(self):
        for i in range(0, self.size):
            self.grid[i, 0] = 0
            self.grid[0, i] = 0
            self.grid[i, self.size - 1] = 0
            self.grid[self.size - 1, i] = 0
    
    # Advance the model one step forwards and update all cells
    def step(self):
        (grid, stable, topples) = step(self.K, self.size, self.grid)
        self.grid = grid
        self.stable = stable
        self.topples += topples
        self.time += 1
    
    # Advance the model forwards until a stable state is reached
    def runToStable(self):
        self.stable = False
        while not self.stable:
            self.step()
        self.time -= 1 # Discount the final iteration which by definition does not change state
    
    # Add sand and advance to stable; counting the number of topples for the resulting avalanche size
    def avalanche(self):
        self.topples = 0
        self.addSand()
        self.runToStable()
        return self.topples
