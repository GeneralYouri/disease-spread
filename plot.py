import matplotlib.colors as mc
import matplotlib.pyplot as plt
import time
from enum import Enum


# Plot line colors for visualisation purposes
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

# Plot summary/history data of the simulation so far
def summary(model, save, show):
    times = range(0, len(model.history))
    counts = {state: [t[state] for t in model.history] for state in model.history[0]}
    
    for state in model.history[0]:
        plt.plot(times, counts[state], label=state, color=Colors[state].value)
    plt.yscale('log')
    plt.xlabel('Time')
    plt.ylabel('Amount')
    plt.title(f'{model.__class__.__name__} Model')
    plt.legend()
    plt.grid(True)
    
    timestamp = int(time.time())
    if save:
        plt.savefig(f'plots/summary_{timestamp}')
    if show:
        plt.show(block=False)

# Plot the current grid State in the simulation
def grid(model, save, show):
    colors = [Colors[state.name].value for state in model.State]
    cmap = mc.ListedColormap(colors)
    
    # Customize colorbar to include State names
    fig, ax = plt.subplots()
    heatmap = ax.pcolorfast(model.grid, cmap = cmap, vmin = 0, vmax = len(model.State))
    cbar = plt.colorbar(heatmap)
    cbar.ax.get_yaxis().set_ticks([])
    for i, state in enumerate(model.State):
        cbar.ax.text(1.5, i + 0.5, state.name, ha = 'left', va='center')
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'{model.__class__.__name__} Model')
    plt.grid(True)
    
    timestamp = int(time.time())
    if save:
        plt.savefig(f'plots/grid_{timestamp}')
    if show:
        plt.show()
    plt.close('all')
