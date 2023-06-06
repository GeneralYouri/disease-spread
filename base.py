import matplotlib.colors as mc
import matplotlib.pyplot as plt
import numpy as np
import time
from enum import Enum, IntEnum
import neighborhood


# Plot line colors for visualisation purposes
# TODO: Better tie these to States
class Colors(Enum):
    SUSCEPTIBLE = 'purple'
    INFECTIOUS = 'red'
    RECOVERED = 'olivedrab'
    SUPERSPREADER = 'maroon'
    SUPERSHEDDER = 'coral'
    HOSPITALIZED = 'dodgerblue'
    VACCINATED = 'greenyellow'
    EXPOSED = 'orange'
    DEAD = 'black'


# Abstract Base Class for the various CA Models for disease spread
class Base:
    size = 0
    center = 0
    
    hasEnded = False
    time = 0
    grid = np.empty(0)
    history = np.empty(0)
    
    # Define the available States in this model
    class State(IntEnum):
        INFECTIOUS = 0

    def __init__(self, strategy, r, **settings):
        for name, value in settings.items():
            setattr(self, name, value)
        self.center = round(self.size / 2)
        self.neighborhood = getattr(neighborhood, strategy.value)(r)

        self.initialize()
        self.history = np.append(self.history, self.getCounts())
    
    # Create the initial grid state
    def initialize(self):
        self.grid = np.full([self.size, self.size], self.State.INFECTIOUS)
    
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
    def plotSummary(self, save, show):
        times = range(0, len(self.history))
        counts = {state: [t[state] for t in self.history] for state in self.history[0]}
        
        for state in self.history[0]:
            plt.plot(times, counts[state], label=state, color=Colors[state].value)
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
        plt.close()

    def plotGrid(self, save, show):
        colors = [Colors[state.name].value for state in self.State]
        cmap = mc.ListedColormap(colors)
        # plt.imshow(self.grid, cmap = cmap, vmax = len(self.State))
        
        # Customize colorbar to include State names
        fig, ax = plt.subplots()
        heatmap = ax.pcolor(self.grid, cmap = cmap, vmax = len(self.State))
        cbar = plt.colorbar(heatmap)
        cbar.ax.get_yaxis().set_ticks([])
        for i, lab in enumerate(self.State):
            cbar.ax.text(1.5, i + 0.5, lab.name, ha = 'left', va='center')
        
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(f'{self.__class__.__name__} Model')
        plt.grid(True)

        timestamp = int(time.time())
        if save:
            plt.savefig(f'plots/plot_grid_{timestamp}')
        if show:
            plt.show()
        plt.close()
