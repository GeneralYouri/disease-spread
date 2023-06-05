import getopt
import sys
import time
import neighborhood
from sirs import *
from seirs import *


# Default settings
size = 75 # The size of the square grid
alpha = 0.05 # Re-Susceptibility rate R->S
beta = 0.2 # Infection rate S->I | S->E
gamma = 0.25 # Recovery rate I->R
delta = 0.2 # Infection rate after Exposure E->I
epsilon = 0 # Nothing yet
batches = 2 # How many intermediate graphs are generated
stepsPerBatch = 10 # How many steps are simulated per batch
save = False # Whether to save the result plot as an image
show = False # Whether to display the result plot on screen
runToEnd = False # Whether to automatically stop running when the pandemic ends


# Input handling
args = sys.argv[1:]
options = ''
longOptions = ['size=', 'alpha=', 'beta=', 'gamma=', 'delta=', 'epsilon', 'b=', 'batches=', 's=', 'steps=', 'save', 'show', 'runToEnd']

try:
    arguments, values = getopt.getopt(args, options, longOptions)
    for currentArgument, currentValue in arguments:
        if currentArgument in ('--size'):
            size = int(currentValue)
        elif currentArgument in ('--alpha'):
            gamma = float(currentValue)
        elif currentArgument in ('--beta'):
            beta = float(currentValue)
        elif currentArgument in ('--gamma'):
            gamma = float(currentValue)
        elif currentArgument in ('--delta'):
            delta = float(currentValue)
        elif currentArgument in ('--epsilon'):
            epsilon = float(currentValue)
        elif currentArgument in ('--b', '--batches'):
            batches = int(currentValue)
        elif currentArgument in ('--s', '--steps'):
            stepsPerBatch = int(currentValue)
        elif currentArgument in ('--save'):
            save = True
        elif currentArgument in ('--show'):
            show = True
        elif currentArgument in ('--runToEnd'):
            runToEnd = True
except getopt.error as err:
    print(str(err))
    exit()


# Model creation
settings = {
    'size': size,
    'alpha': alpha,
    'beta': beta,
    'gamma': gamma,
    'delta': delta,
    'epsilon': epsilon,
}
model = SEIRS(neighborhood.Strategy.NEUMANN, 1, **settings)
print(f'Created model with size {size} and infection rate {beta} and recovery rate {gamma}')
print(f'Grid state: {model.history[-1]}')

# Model execution
for i in range(0, batches):
    startTime = time.perf_counter()
    if runToEnd:
        if model.hasEnded:
            break
        model.runToEnd(stepsPerBatch)
    else:
        for _ in range(0, stepsPerBatch):
            model.step()
    endTime = time.perf_counter()
    print(f'Batch {i + 1}: Simulated {model.time - i * stepsPerBatch} steps in {endTime - startTime:.2f} seconds')
    print(f'Grid state: {model.history[-1]}')

# Model output
model.plotSummary(save, show)
model.plotGrid(save, show)
print(f'Finished simulation')
