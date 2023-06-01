import getopt
import sys
import time
from model import *
from visualize import *


# Default settings
beta = 0.6 # Infection Rate
gamma = 0.25 # Recovery Rate
size = 75 # The size of the square grid
batches = 1 # How many intermediate graphs are generated
stepsPerBatch = 100 # How many steps are simulated per batch


# Input handling
args = sys.argv[1:]
options = ''
longOptions = ['size=', 'beta=', 'gamma=', 'b=', 'batches=', 's=', 'steps=']

try:
    arguments, values = getopt.getopt(args, options, longOptions)
    for currentArgument, currentValue in arguments:
        if currentArgument in ('--size'):
            size = int(currentValue)
        elif currentArgument in ('--beta'):
            beta = int(currentValue)
        elif currentArgument in ('--gamma'):
            gamma = int(currentValue)
        elif currentArgument in ('--b', '--batches'):
            batches = int(currentValue)
        elif currentArgument in ('--s', '--steps'):
            stepsPerBatch = int(currentValue)

except getopt.error as err:
    print(str(err))
    exit()

# Model execution
model = Model(size, beta, gamma, NeighborStrategy.NEUMANN)
print(f'Created model with size {size} and infection rate {beta} and recovery rate {gamma}')
print(f'Grid state: {model.getSummary()}')

for i in range(1, batches + 1):
    startTime = time.perf_counter()
    for j in range(0, stepsPerBatch):
        model.step()
    endTime = time.perf_counter()
    print(f'Batch {i}: Simulated {stepsPerBatch} steps in {endTime - startTime:.2f} seconds')
    print(f'Grid state: {model.getSummary()}')
