# Disease Spread
A CA model for researching pandemic disease spread and the factors that affect it

A command line interface allows simulating a variety of different models with different features, with settings to further customize the simulation.
#

## Usage
Using Python, run simulations during development.
```
python main.py [settings]
```
Using PyInstaller, compile the development version into a new executable:
```
pyinstaller CA.spec
```
Run simulations via the compiled executable (no prerequisites required):
```
CA.exe [settings]
```
**Note: Output plot images are saved in a subfolder called `plots`. This subfolder must be manually created.**
#

## Examples 
Run the SIRS Model with adjusted alpha/beta/gamma values (this one is very infectious).
```
CA.exe --type=SIRS --alpha=0.1 --beta=0.8 --gamma=0.2 --show
```
Run the SIR_HD Model with adjusted gamma/epsilon values and a maximum fraction of beds.\
Note it’s usually smart to set epsilon relative to gamma and to specify both settings together.
```
CA.exe --type=SIR_HD --alpha=0.05, --beta=0.7, --gamma=0.1 --epsilon=0.04 --maxBeds=0.05 --show
```
The same as above, because not specifying a setting uses its default value.\
Because of this all settings are always optional, even if they are specific to this Model type.\
It is also fine if you happen to specify settings that are not used by the specified Model type.
```
CA.exe --type=SIR_HD --gamma=0.2 --epsilon=0.06 --delta=0.5 --show
```
Run the S_EIR Model for up to 100 time steps and show the result on screen.\
The simulation can stop early if the pandemic dies before 100 time steps.
```
CA.exe --type=SIR_E --batches=10 --stepsPerBatch=10 --runToEnd --show
```
&nbsp;

You probably want to specify at least these settings whenever you’re generating definitive images.\
Note: To --save a graph, make a new folder called "Plots" in the same directory as the CA.exe file.
```
CA.exe --type=SIRS --runToEnd --save
```
Alternatively, instead of letting the simulation run to its end you can run a set number of time steps.\
Both options have their benefits, it depends on the use case.
```
CA.exe --type=SIRS --batches=10 --stepsPerBatch=10 --save
```
#

## Settings 
All settings are optional and settings can be specified in any order.\
Note: default values are very likely to change over time.

`--type=SIR`\
The model type to simulate.\
Valid options: SI, SIS, SIR, SIRS, SI_E, SIS_E, SIR_E, SIRS_E, SIR_H, SIRS_H, SIR_HD, SIRS_HD, SIR_V1, SIRS_V1, SIR_V2, SIRS_V2.

`--size=100`\
The one-dimensional size of the square grid; creates a 100x100 cells large grid.

`--neighborhood=Neumann`\
The neighborhood type to use for Infection.

`--range=1`\
The range applied on the neighborhood type.

`--initial=0`\
The initial fraction of cells to randomly Infect.\
Note: the value 0 instead Infects the center 3x3 of cells.

`--alpha=0.05`\
Re-Susceptibility rate for R->S.

`--beta=0.7`\
Infection rate for S->I and S->E.\
The Infection rate has been updated to auto-adjust for neighborhood size.\
You can therefore use the same beta values as used in the ODE.

`--gamma=0.25`\
Recovery rate for I->R and H->R.

`--delta=0.2`\
Infection rate after Exposure for E->I.

`--epsilon=0.03`\
Hospitalization rate for I->H.\
Note it’s usually smart to set this relative to gamma and to specify both settings together.

`--zeta=0.005`\
Vaccination rate for S->V.

`--interventionFactor=1.0`\
The factor of change that's applied to beta due to Intervention.\
Example: if beta=0.8 and interventionFactor=0.75, after Intervention beta=0.6.\
Note: Intervention is considered to be disabled when this value is 1.0.

`--interventionDelay=100`\
How long to run the simulation normally before applying Intervention.

`--vaccinationFactor=1.0`\
The factor of change that's applied to beta when Infecting Vaccinated cells.\
Example: if beta=0.8 and vaccinationFactor=0.75, for Vaccinated cells beta=0.6.

`--vaccinationDelay=50`\
How long to run the simulation normally before enabling Vaccination.

`--maxVaccines=1.0`\
The maximum allowed fraction of Vaccinated cells.

`--maxBeds=0.05`\
The maximum allowed fraction of Hospitalized cells.

&nbsp;

`--simulations=1`\
How many times to run the entire simulation in a row.\
For values above 1 only the summary plot is used, using average data across all simulations.\
The runtime of the shortest simulation is used; other data is discarded.

`--batches=10`\
How many intermediate results are generated (ie. text output on the screen).\
Note: the value 0 is treated as infinity, effectively disabling the setting (use for runToEnd).

`--stepsPerBatch=10`\
How many time steps are simulated per batch.\
The total number of time steps is batches * stepsPerBatch = 5 * 10 = 50.

`--runToEnd`\
Whether to automatically stop running when the pandemic ends.\
The simulation runs until there are 0 Infectious cells, or until the total number of time steps.

`--save`\
Whether to save the result plots as images.\
Note: To --save a graph, make a new folder called "Plots" in the same directory as the CA.exe file.

`--show`\
Whether to display the result plots on screen.
#

## TODO List

### Must Have
- Add a way to compare and prove exponential growth factors across models.
Perhaps by calculating the R value?
- Add more Model types to support these features:
  - Superspreader: A variant Infected cell with a larger neighborhood.
  - Supershedder: A variant Infected cell with a higher Infection rate beta.
- Figure out a way to use different neighborhoods within a single Model, ie only some cells use an extended neighborhood. This messes up the current calculation because it happens on the receiving cell. See Superspreader.

### Should have
- Find a way to apply inheritance to the State Machine itself.
Goal is to be able to compose State Transitions from different features.
A feature would be "Recovery" which adds the State Recovered and the Transition I->R.

### Want to have
- Add a way to randomise the location of all cells in the grid. Use it to randomise the full grid every time step, while retaining total counts for each State. Could be useful for comparing to the ODE model.
- Create a way to export grid data for visualisations.
- Create a way to import grid data for usage across experiments.
