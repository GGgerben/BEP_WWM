# Agent-Based Model: WhereWeMove Policy Analysis

## Project Description
This agent-based model (ABM) is developed to analyse how flood risk management policies influence household adaptation behaviour and perceived satisfaction in a Western European context. The model is explicitly designed to address the following research question:

> **What is the effect of variations in flood policies (base case, subsidies and insurance schemes) on household flood adaptation behaviour and satisfaction in a Western European context?**

The model examines how different policy settings affect the adoption of flood mitigation measures and relocation decisions at the household level. Three policy regimes are analysed: a baseline scenario without policy intervention, a subsidy scheme targeting a specific mitigation measure, and an insurance scheme offering financial compensation for flood damages.

Homeowners are modelled as heterogeneous agents who differ in financial resources, flood experience, housing characteristics and exposure to pluvial and fluvial flood risk. Policy interventions influence agent decision-making by modifying the costs, availability and attractiveness of mitigation measures and insurance options.

The serious game *WhereWeMove* (Arevalo et al., 2024) provides the conceptual foundation for this model. Game mechanics and decision rules are translated into computational rules, allowing the behavioural logic of the game to be **scaled up** and systematically analysed across many simulation runs and policy scenarios.

---

## Objective
The primary objective of this agent-based model is **policy analysis** rather than prediction. The model is used to:

- Compare the behavioural effects of different flood policy regimes  
- Analyse substitution, crowding-out and moral hazard effects  
- Examine whether policy-induced behavioural changes translate into differences in satisfaction and inequality  
- Explore how household-level decision-making aggregates into system-level outcomes  

By translating the serious game into an ABM, the model enables **upscaling** from individual gameplay experiences to population-level patterns, providing a controlled environment for testing policy designs before implementation in participatory or real-world settings.

---

## Model Framework
The model is implemented using the **Mesa** framework, a widely used Python library for agent-based modelling.

Mesa provides the core infrastructure for:
- Agent scheduling and activation  
- Model stepping and simulation control  
- Managing agent–environment interactions  

More information about Mesa can be found at:  
https://mesa.readthedocs.io

---

## Model Structure
The project is structured as follows:

- **/classes**  
  Contains class definitions for agents and supporting objects, including household agents, houses, mitigation measures and insurance logic.

- **/data**  
  Contains input data used to initialise the model, such as housing characteristics and flood-related attributes.

- **/plots**  
  Directory for figures generated from simulation outputs.

- **/results**  
  Directory for simulation outputs stored as CSV files.

- **experiment.py**  
  Main script for configuring and running experiments. Defines policy scenarios, parameter settings and the number of simulation runs.

- **export.py**  
  Handles exporting model outputs and summary statistics to CSV files.

- **model.py**  
  Contains the core model logic, including the simulation loop, agent decision-making and environment updates.

---

## How to Run the Model

### Requirements
Make sure Python is installed and required packages (including Mesa) are available in your environment.

### Running the model via the terminal
Navigate to the project root directory and run:

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

## Related Thesis
This agent-based model was developed as part of a bachelors’s thesis at Delft University of Technology.

**Thesis title:**  
*Policy and Behaviour under Flood Risk: A Serious Game into an Agent-Based Model*

**Author:**  
Gerben van Diggelen

**Programme:**  
BSc Technology, Policy and Management, Delft University of Technology

**Year:**  
2025

The model implements the behavioural mechanisms, policy scenarios and experimental design described in the thesis, and is intended to support transparency, reproducibility and further research.
