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
    SI_E = 'SI_E'
    SIS_E = 'SIS_E'
    SIR_E = 'SIR_E'
    SIRS_E = 'SIRS_E'
    SIR_H = 'SIR_H'
    SIRS_H = 'SIRS_H'
    SIR_HD = 'SIR_HD'
    SIRS_HD = 'SIRS_HD'
    SIR_V1 = 'SIR_V1'
    SIRS_V1 = 'SIRS_V1'
    SIR_V2 = 'SIR_V2'
    SIRS_V2 = 'SIRS_V2'


# Default settings
type = Type.SIR.value # The model type to simulate
size = 100 # The size of the square grid
neighborhood = Strategy.NEUMANN.value # The name of the neighborhood type
range = 1 # The range applied to the neighborhood
initial = 0 # The initial fraction of cells to Infect
alpha = 0.05 # Re-Susceptibility rate R->S
beta = 0.7 # Infection rate S->I | S->E
gamma = 0.1 # Recovery rate I->R | H->R
delta = 0.2 # Infection rate after Exposure E->I
epsilon = 0.3 * gamma # Hospitalization rate I->H
zeta = 0.005 # Vaccination rate S->V
interventionFactor = 1.0 # Adjusted infection rate to be applied later during the simulation
interventionDelay = 100 # The time after which beta2 replaces beta as the infection rate
vaccinationFactor = 1.0 # Adjusted infection rate for vaccinated cells
vaccinationDelay = 50 # The time after which the Vaccination State is enabled
maxVaccines = 1.0 # The maximum allowed fraction of Vaccinated cells
maxBeds = 0.05 # The maximum allowed fraction of Hospitalized cells
simulations = 1 # How many times to run the entire simulation in a row (results are averaged)
batches = 10 # How many intermediate results are generated
stepsPerBatch = 10 # How many steps are simulated per batch
runToEnd = False # Whether to automatically stop running when the pandemic ends
save = False # Whether to save the result plots as images
show = False # Whether to display the result plots on screen
logPlot = False # Whether to use a log scale for the summary plot


# Input handling
args = sys.argv[1:]
options = ''
longOptions = [
    'type=', 'size=', 'neighborhood=', 'range=', 'initial=',
    'alpha=', 'beta=', 'gamma=', 'delta=', 'epsilon=', 'zeta=',
    'interventionFactor=', 'interventionDelay=',
    'vaccinationFactor=', 'vaccinationDelay=',
    'maxVaccines=', 'maxBeds=',
    
    'simulations=', 'batches=', 'stepsPerBatch=', 'runToEnd',
    'save', 'show', 'logPlot',
]

try:
    arguments, values = getopt.getopt(args, options, longOptions)
    for currentArgument, currentValue in arguments:
        if currentArgument in ('--type'):
            type = Type(currentValue).value
        elif currentArgument in ('--size'):
            size = int(currentValue)
        elif currentArgument in ('--neighborhood'):
            neighborhood = Strategy(currentValue).value
        elif currentArgument in ('--range'):
            range = int(currentValue)
        elif currentArgument in ('--initial'):
            initial = float(currentValue)
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
        elif currentArgument in ('--zeta'):
            zeta = float(currentValue)
        elif currentArgument in ('--interventionFactor'):
            interventionFactor = float(currentValue)
        elif currentArgument in ('--interventionDelay'):
            interventionDelay = int(currentValue)
        elif currentArgument in ('--vaccinationFactor'):
            vaccinationFactor = float(currentValue)
        elif currentArgument in ('--vaccinationDelay'):
            vaccinationDelay = int(currentValue)
        elif currentArgument in ('--maxVaccines'):
            maxVaccines = float(currentValue)
        elif currentArgument in ('--maxBeds'):
            maxBeds = float(currentValue)
        elif currentArgument in ('--simulations'):
            simulations = int(currentValue)
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
        elif currentArgument in ('--logPlot'):
            logPlot = True
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
    size=size, neighborhood=neighborhood, range=range, initial=initial,
    alpha=alpha, beta=beta, gamma=gamma, delta=delta, epsilon=epsilon, zeta=zeta,
    interventionFactor=interventionFactor, interventionDelay=interventionDelay,
    vaccinationFactor=vaccinationFactor, vaccinationDelay=vaccinationDelay,
    maxVaccines=maxVaccines, maxBeds=maxBeds,
)
settings = Settings(
    type=type,
    simulations=simulations, batches=batches, stepsPerBatch=stepsPerBatch, runToEnd=runToEnd,
    save=save, show=show, logPlot=logPlot,
)
