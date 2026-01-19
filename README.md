# Agent Based Model WhereWeMove

## Project Description
This project implements an Agent-Based Model (ABM) to simulate interactions between heterogeneous agents in a dynamic environment. The model is inspired by and builds upon the WhereWeMove game developed by Arévalo et al.(2024). The model is used to explore how individual decisions, spatial dynamics and local interactions give rise to emergent system-level outcomes under different scenarios and assumptions.

## Objective
This Agent-Based Model simulates the behavior and interactions of individual agents to analyse how emergent system-level outcomes arise. The model is used to explore scenarios, compare interventions, and understand complex system dynamics.

### Model Overview
The model is structured as follows:

  - **/classes**: Contains the class definitions used in the model, including the different agent types and supporting classes that define their behavior and interactions.
  - **/data**: Contains the input data used to initialise the model, including the initial set of houses and their attributes.
  - **/plots**: Empty directory reserved for future visualisations and plots generated from simulation outputs.
  - **/results**: Empty directory reserved for future simulation results, stored as CSV files.
  - **experiment.py**: Script used to configure and run experiments, including scenario definitions, parameter settings and multiple simulation runs.
  - **export.py**: Handles the exporting of simulation results, such as writing model outputs and summary statistics to CSV files.
  - **model.py**: Contains the core model logic, including the simulation loop, agent scheduling and environment updates.

### How to Run

## Run the model
The core model logic is implemented in model.py.
Agents, the environment, and the simulation loop are defined there.

To run all experiments and generate simulation data, execute:

```
python experiment.py
```
This runs all scenarios defined in SCENARIOS and stores the results as CSV files in the /results directory.

## Generate plots
Plots are generated from the saved CSV files and can be reproduced without rerunning the model.
Enable the desired plot functions in the __main__ section of experiment.py, for example:

```
plot_policy_comparison_adoption_bars("results", "plots")
plot_satisfaction_regime_with_uncertainty("results", "plots")
```
All figures are saved to the /plots directory.

## Reproducibility
To reproduce results from scratch, clear the /results and /plots directories and rerun experiment.py.


## Authors
- Gerben van Diggelen
- Juliette Folkers
