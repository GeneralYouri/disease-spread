import getopt
import sys
import time
import neighborhood
from sirs import *
from seirs import *
from sihrd import *


# Default settings
type = 'SIHRD' # The model type to simulate
size = 100 # The size of the square grid
alpha = 0.05 # Re-Susceptibility rate R->S
beta = 0.2 # Infection rate S->I | S->E
gamma = 0.25 # Recovery rate I->R | H->R
delta = 0.2 # Infection rate after Exposure E->I
epsilon = 0.3 * gamma # Hospitalization rate I->H
maxBeds = 0.05 * size ** 2 # The maximum allowed number of Hospitalized cells 
batches = 5 # How many intermediate results are generated
stepsPerBatch = 10 # How many steps are simulated per batch
runToEnd = False # Whether to automatically stop running when the pandemic ends
save = False # Whether to save the result plots as images
show = False # Whether to display the result plots on screen


# Input handling
args = sys.argv[1:]
options = ''
longOptions = ['type=', 'size=', 'alpha=', 'beta=', 'gamma=', 'delta=', 'epsilon=', 'maxBeds=', 'batches=', 'stepsPerBatch=', 'runToEnd', 'save', 'show']

try:
    arguments, values = getopt.getopt(args, options, longOptions)
    for currentArgument, currentValue in arguments:
        if currentArgument in ('--type'):
            type = str(currentValue)
        elif currentArgument in ('--size'):
            size = float(currentValue)
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
        elif currentArgument in ('--maxBeds'):
            maxBeds = float(currentValue)
        elif currentArgument in ('--batches'):
            batches = int(currentValue)
        elif currentArgument in ('--stepsPerBatch'):
            stepsPerBatch = int(currentValue)
        elif currentArgument in ('--runToEnd'):
            runToEnd = True
        elif currentArgument in ('--save'):
            save = True
        elif currentArgument in ('--show'):
            show = True
except getopt.error as err:
    print(str(err))
    exit()


# Model creation
startTimeGlobal = time.perf_counter()
settings = {
    'size': size,
    'alpha': alpha,
    'beta': beta,
    'gamma': gamma,
    'delta': delta,
    'epsilon': epsilon,
    'maxBeds': maxBeds,
}
model = globals()[type](neighborhood.Strategy.NEUMANN, 1, **settings)
print(f'Created {model.__class__.__name__} model with size {size} and infection rate {beta} and recovery rate {gamma}')
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
endTimeGlobal = time.perf_counter()
model.plotSummary(save, show)
model.plotGrid(save, show)
print(f'Simulation finished after {model.time} steps and {endTimeGlobal - startTimeGlobal:.2f} seconds')
