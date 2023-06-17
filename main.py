import time
from tabulate import tabulate
from input import settings, modelSettings
import models
import plot


def simulate():
    # Model creation
    startTimeGlobal = time.perf_counter()
    model = getattr(models, settings.type)(modelSettings)
    print(f'Init state: {model.history[-1]}')

    # Model execution
    for i in range(0, settings.batches):
        startTime = time.perf_counter()
        for _ in range(0, settings.stepsPerBatch):
            if settings.runToEnd and model.hasEnded:
                break
            model.step()
            if settings.shuffle:
                model.shuffle()
        endTime = time.perf_counter()
        print(f'Batch {i + 1}: Simulated {model.time - i * settings.stepsPerBatch} steps in {endTime - startTime:.2f} seconds')
        print(f'Grid state: {model.history[-1]}')
        if settings.runToEnd and model.hasEnded:
            break

    # Model output
    endTimeGlobal = time.perf_counter()
    print(f'Simulation finished after {model.time} steps and {endTimeGlobal - startTimeGlobal:.2f} seconds')
    return model


marker = int(time.time()) % (10 ** 6)
if settings.simulations == 1:
    model = simulate()
    print(f'\n{model.__class__.__name__} Model Settings used:')
    print(tabulate(modelSettings.__dict__.items()))
    plot.summary(model, settings, marker, plot.Type.NORMAL)
    if settings.save:
        plot.summary(model, settings, marker, plot.Type.LOG)
        plot.summary(model, settings, marker, plot.Type.LOGLOG)
        plot.grid(model, settings, marker)
    
else:
    usedModels = []
    for _ in range(0, settings.simulations):
        model = simulate()
        usedModels.append(model)
    print(f'\n{model.__class__.__name__} Model Settings used:')
    print(tabulate(modelSettings.__dict__.items()))
    plot.averageSummary(model, settings, marker, plot.Type.NORMAL)
    if settings.save:
        plot.averageSummary(model, settings, marker, plot.Type.LOG)
        plot.averageSummary(model, settings, marker, plot.Type.LOGLOG)
