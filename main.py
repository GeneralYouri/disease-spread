import getopt
import numpy as np
import sys
import time
from model import *
from visualize import *


# Default settings
a = 0.6 # Infection Rate
p = 0.25 # Recovery Rate
size = 75 # The size of the square grid
batches = 1 # How many intermediate graphs are generated
stepsPerBatch = 100 # How many steps are simulated per batch


# Input handling
argumentList = sys.argv[1:]
options = ''
long_options = ['size=', 'a=', 'p=', 'b=', 'batches=', 's=', 'steps=']

try:
    arguments, values = getopt.getopt(argumentList, options, long_options)
    for currentArgument, currentValue in arguments:
        if currentArgument in ('--size'):
            size = int(currentValue)
        elif currentArgument in ('--a'):
            a = int(currentValue)
        elif currentArgument in ('--p'):
            p = int(currentValue)
        elif currentArgument in ('--b', '--batches'):
            batches = int(currentValue)
        elif currentArgument in ('--s', '--steps'):
            stepsPerBatch = int(currentValue)

except getopt.error as err:
    print(str(err))
    exit()


# Model execution
model = Model(size, a, p, NeighborStrategy.NEUMANN)
print(f'Created model with size {size} and infection rate {a} and recovery rate {p}')

for i in range(1, batches + 1):
    startTime = time.perf_counter()
    for j in range(0, stepsPerBatch):
        model.step()
    endTime = time.perf_counter()
    print(f'Batch {i}: Simulated {stepsPerBatch} steps in {endTime - startTime:.2f} seconds')
