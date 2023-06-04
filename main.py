import getopt
import sys
import time
from sirs import *
from sei import *


# Default settings
alpha = 0.05 # Re-Susceptibility rate R->S
beta = 0.2 # Infection rate S->I | S->E
gamma = 0.25 # Recovery rate I->R
theta = 0.2 # Infection rate after Exposure E->I
size = 75 # The size of the square grid
batches = 1 # How many intermediate graphs are generated
stepsPerBatch = 10 # How many steps are simulated per batch


# Input handling
args = sys.argv[1:]
options = ''
longOptions = ['size=', 'alpha=', 'beta=', 'gamma=', 'theta=', 'b=', 'batches=', 's=', 'steps=']

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
        elif currentArgument in ('--theta'):
            gamma = float(currentValue)
        elif currentArgument in ('--b', '--batches'):
            batches = int(currentValue)
        elif currentArgument in ('--s', '--steps'):
            stepsPerBatch = int(currentValue)

except getopt.error as err:
    print(str(err))
    exit()


# Model execution
settings = { size, alpha, beta, gamma, theta }
model = SIRS(NeighborStrategy.NEUMANN, size=size, alpha=alpha, beta=beta, gamma=gamma)
print(f'Created model with size {size} and infection rate {beta} and recovery rate {gamma}')
print(f'Grid state: {model.history[-1]}')

for i in range(1, batches + 1):
    startTime = time.perf_counter()
    for _ in range(0, stepsPerBatch):
        model.step()
    endTime = time.perf_counter()
    print(f'Batch {i}: Simulated {stepsPerBatch} steps in {endTime - startTime:.2f} seconds')
    print(f'Grid state: {model.history[-1]}')

model.plotSummary()
print(f'Finished simulation')
