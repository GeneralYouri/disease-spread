import numpy as np
import time
from model import *
from visualize import *


# For point B
size = 200
sandStrategy = SandStrategy.RANDOM
model = Model(size, sandStrategy) # model with Random sand dropping as strategy
print(f'Created model with size {size} and {sandStrategy}')

# For point C
startTime = time.perf_counter()
model.runToStable()
endTime = time.perf_counter()
print(f'Settled into initial stable state in {endTime - startTime:.2f} seconds')

# For point D
avalanche1 = model.avalanche()
model.clearEdges()
#plot2dGrid(model.grid, key = 'd1')
avalanche2 = model.avalanche()
model.clearEdges()
#plot2dGrid(model.grid, key = 'd2')
print(f'Plotted two stable states after random avalanches')

# For point E
batches = 1 # How many intermediate graphs are generated
avalanchesPerBatch = 1000 # How many avalanches are simulated per batch
frequenciesRandom = {} # Track how often an avalanche of size i occurs with sandStrategy Random
frequenciesCenter = {} # Track how often an avalanche of size i occurs with sandStrategy Random
frequenciesEdge = {} # Track how often an avalanche of size i occurs with sandStrategy Random
avalanches = 1 # Tracks how many avalanches occured in total 
# Is now a dictionary for performance; the array was ginormous and extremely sparse

# Preperation for point F
centerModel = Model(size, SandStrategy.CENTER)
centerModel.runToStable()
edgeModel = Model(size, SandStrategy.EDGES)
edgeModel.runToStable()


def batchAvalanches():
    avalanches = 0
    for _ in range(0, avalanchesPerBatch):
        avalanches += updateDictionary(frequenciesRandom, model)
        
    return(avalanches)

def batchThreeKindsOfAvalanche():
    avalanches = 0
    for _ in range(0, avalanchesPerBatch):
        avalanches += updateDictionary(frequenciesRandom, model)
        avalanches += updateDictionary(frequenciesCenter, centerModel)
        avalanches += updateDictionary(frequenciesEdge, edgeModel)
        
    return(avalanches)

def updateDictionary(frequency, sModel):
    size = sModel.avalanche()
    frequency[size] = frequency.get(size, 0) + 1
    if size != 0: return (1)
    else: return(0)

for i in range(0, batches):
    startTime = time.perf_counter()
    avalanches += batchAvalanches()
    #avalanches += batchThreeKindsOfAvalanche()
    endTime = time.perf_counter()
    print(f'Batch {i}: Generated {avalanchesPerBatch} avalanches in {endTime - startTime:.2f} seconds')
    
    #plotAvalancheSizes(frequenciesRandom, sandStrategy, avalanches)
    #plotThreeSandStrategies(frequenciesRandom, frequenciesCenter,frequenciesEdge, avalanches)
