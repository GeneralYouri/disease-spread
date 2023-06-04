# Disease Spread
A CA model for researching epidemic disease spread and the factors that affect it

## TODO:
- Add more and better ways of specifying the initial State.
- Add more Model types to support features like Superspreader, Hospitalization, Vaccination, Intervention.
- Create graph visualization for displaying the grid itself.
- Find a way to apply inheritance to the State Machine itself.
Goal is to be able to compose State Transitions from different features.
A feature would be "Recovery" which adds the State Recovered and the Transition I->R.

- ? Create a way to export grid data for visualisations.
- ? Create a way to import grid data for usage across experiments.
- X Look into njit for performance improvements.
- X Can't use PyPy because it doesn't support matplotlib.
