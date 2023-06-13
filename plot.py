import matplotlib.colors as mc
import matplotlib.pyplot as plt
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

# Plot average summary/history data across multiple simulations
def averageSummary(models, settings, marker):
    states = [s.name for s in models[0].State]
    lengths = [len(model.history) for model in models]
    times = range(0, min(lengths))
    counts = {s: [sum([m.history[t][s] for m in models]) / len(models) for t in times] for s in states}
    
    for s in states:
        plt.plot(times, counts[s], label=s, color=Colors[s].value)
    
    # Show Intervention timing
    if models[0].interventionFactor != 1.0 and len(times) > models[0].interventionDelay:
        plt.axvline(models[0].interventionDelay, linestyle='--', label='INTERVENTION')
    
    if settings.logPlot:
        plt.yscale('log', base=10)
    
    plt.xlabel('Time')
    plt.ylabel('Amount')
    plt.title(f'{models[0].__class__.__name__} Model')
    plt.legend()
    plt.grid(True)
    
    if settings.save:
        plt.savefig(f'plots/averageSummary_{marker}')
    if settings.show:
        plt.show()

# Plot summary/history data of the simulation so far
def summary(model, settings, marker):
    states = [s.name for s in model.State]
    length = len(model.history)
    times = range(0, length)
    counts = {s: [model.history[t][s] for t in times] for s in states}
    
    for s in states:
        plt.plot(times, counts[s], label=s, color=Colors[s].value)
    
    # Show Intervention timing
    if model.interventionFactor != 1.0 and len(times) > model.interventionDelay:
        plt.axvline(model.interventionDelay, linestyle='--', label='INTERVENTION')
    
    if settings.logPlot:
        plt.yscale('log', base=10)
    
    plt.xlabel('Time')
    plt.ylabel('Amount')
    plt.title(f'{model.__class__.__name__} Model')
    plt.legend()
    plt.grid(True)
    
    if settings.save:
        plt.savefig(f'plots/summary_{marker}')
    if settings.show:
        plt.show(block=False)

# Plot the current grid State in the simulation
def grid(model, settings, marker):
    colors = [Colors[s.name].value for s in model.State]
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
    
    if settings.save:
        plt.savefig(f'plots/grid_{marker}')
    if settings.show:
        plt.show()
    plt.close('all')
