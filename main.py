import getopt
import sys
import time
import neighborhood
from sirs import *
from seirs import *
from sihrd import *


# Default settings
size = 75 # The size of the square grid
alpha = 0.05 # Re-Susceptibility rate R->S
beta = 0.2 # Infection rate S->I | S->E
gamma = 0.25 # Recovery rate I->R | H->R
delta = 0.2 # Infection rate after Exposure E->I
epsilon = 0.2 * gamma # Hospitalization rate I->H
maxbeds = 0.05 * size ** 2
batches = 2 # How many intermediate graphs are generated
stepsPerBatch = 10 # How many steps are simulated per batch
runToEnd = False # Whether to automatically stop running when the pandemic ends
save = False # Whether to save the result plot as an image
show = False # Whether to display the result plot on screen


# Input handling
args = sys.argv[1:]
options = ''
longOptions = ['size=', 'alpha=', 'beta=', 'gamma=', 'delta=', 'epsilon=', 'maxbeds=', 'batches=', 'steps=', 'runToEnd', 'save', 'show']

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
        elif currentArgument in ('--maxbeds'):
            maxbeds = float(currentValue)
        elif currentArgument in ('--batches'):
            batches = int(currentValue)
        elif currentArgument in ('--steps'):
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
settings = {
    'size': size,
    'alpha': alpha,
    'beta': beta,
    'gamma': gamma,
    'delta': delta,
    'epsilon': epsilon,
    'maxbeds': maxbeds,
}
model = SIHRD(neighborhood.Strategy.NEUMANN, 1, **settings)
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
model.plotSummary(save, show)
model.plotGrid(save, show)
print(f'Finished simulation')
