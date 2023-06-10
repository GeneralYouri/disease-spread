import getopt
import sys
from enum import Enum
from neighborhood import Strategy


# Allowed Model types
class Type(Enum):
    SI = 'SI'
    SIS = 'SIS'
    SIR = 'SIR'
    SIRS = 'SIRS'
    SEI = 'SEI'
    SEIS = 'SEIS'
    SEIR = 'SEIR'
    SEIRS = 'SEIRS'
    SIHR = 'SIHR'
    SIHRD = 'SIHRD'


# Default settings
type = Type.SIR.value # The model type to simulate
size = 100 # The size of the square grid
neighborhood = Strategy.NEUMANN.value # The name of the neighborhood type
range = 1 # The range applied to the neighborhood
alpha = 0.05 # Re-Susceptibility rate R->S
beta = 0.7 # Infection rate S->I | S->E
gamma = 0.25 # Recovery rate I->R | H->R
delta = 0.2 # Infection rate after Exposure E->I
epsilon = 0.3 * gamma # Hospitalization rate I->H
maxBeds = 0.05 # The maximum allowed number of Hospitalized cells 
batches = 0 # How many intermediate results are generated
stepsPerBatch = 10 # How many steps are simulated per batch
runToEnd = False # Whether to automatically stop running when the pandemic ends
save = False # Whether to save the result plots as images
show = False # Whether to display the result plots on screen


# Input handling
args = sys.argv[1:]
options = ''
longOptions = ['type=', 'size=', 'neighborhood=', 'range=', 'alpha=', 'beta=', 'gamma=', 'delta=', 'epsilon=', 'maxBeds=', 'batches=', 'stepsPerBatch=', 'runToEnd', 'save', 'show']

try:
    arguments, values = getopt.getopt(args, options, longOptions)
    for currentArgument, currentValue in arguments:
        if currentArgument in ('--type'):
            type = Type(currentValue).value
        elif currentArgument in ('--size'):
            size = float(currentValue)
        elif currentArgument in ('--neighborhood'):
            neighborhood = Strategy(currentValue).value
        elif currentArgument in ('--range'):
            range = int(currentValue)
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
# Infinite batches
if batches == 0:
    batches = 1 << 31


# Output Settings
class Settings:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
modelSettings = Settings(
    size=size, neighborhood=neighborhood, range=range,
    alpha=alpha, beta=beta, gamma=gamma, delta=delta, epsilon=epsilon,
    maxBeds=maxBeds,
)
settings = Settings(
    type=type,
    batches=batches, stepsPerBatch=stepsPerBatch, runToEnd=runToEnd,
    save=save, show=show,
)
