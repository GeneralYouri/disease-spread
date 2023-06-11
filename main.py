import time
from tabulate import tabulate
from input import settings, modelSettings
from sirs import *
from seirs import *
from sihrds import *
from sivrs import *
import plot


# Model creation
startTimeGlobal = time.perf_counter()
model = globals()[settings.type](modelSettings)
print(f'Init state: {model.history[-1]}')

# Model execution
for i in range(0, settings.batches):
    startTime = time.perf_counter()
    if settings.runToEnd:
        if model.hasEnded:
            break
        model.runToEnd(settings.stepsPerBatch)
    else:
        for _ in range(0, settings.stepsPerBatch):
            model.step()
    endTime = time.perf_counter()
    print(f'Batch {i + 1}: Simulated {model.time - i * settings.stepsPerBatch} steps in {endTime - startTime:.2f} seconds')
    print(f'Grid state: {model.history[-1]}')

# Model output
endTimeGlobal = time.perf_counter()
print(f'{model.__class__.__name__} Model Settings used:')
print(tabulate(modelSettings.__dict__.items()))
print(f'Simulation finished after {model.time} steps and {endTimeGlobal - startTimeGlobal:.2f} seconds')
plot.summary(model, settings.save, settings.show)
plot.grid(model, settings.save, settings.show)
