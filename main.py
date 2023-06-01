import numpy as np
import time
from model import *
from visualize import *


size = 75
a = 0.6 # Infection rate
p = 0.25 # Recovery rate
model = Model(size, a, p, NeighborStrategy.NEUMANN)
print(f'Created model with size {size} and infection rate {a} and recovery rate {p}')

batches = 1 # How many intermediate graphs are generated
stepsPerBatch = 100 # How many steps are simulated per batch


for i in range(1, batches + 1):
    startTime = time.perf_counter()
    for j in range(0, stepsPerBatch):
        model.step()
    endTime = time.perf_counter()
    print(f'Batch {i}: Simulated {stepsPerBatch} steps in {endTime - startTime:.2f} seconds')
