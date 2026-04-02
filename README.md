# Agent-Based Model: WhereWeMove Policy Analysis and Household Adaptation under Wealth and Flood Experience

## Project Description
This agent-based model (ABM) is developed to analyse how flood risk management policies influence household adaptation behaviour and perceived satisfaction in a Western European context. The model is explicitly designed to address the following research question:

> **What is the effect of variations in flood policies (base case, subsidies and insurance schemes) on household flood adaptation behaviour and satisfaction in a Western European context?**

The model examines how different policy settings affect the adoption of flood mitigation measures and relocation decisions at the household level. Three policy regimes are analysed: a baseline scenario without policy intervention, a subsidy scheme targeting a specific mitigation measure, and an insurance scheme offering financial compensation for flood damages.

Homeowners are modelled as heterogeneous agents who differ in financial resources, flood experience, housing characteristics and exposure to pluvial and fluvial flood risk. Policy interventions influence agent decision-making by modifying the costs, availability and attractiveness of mitigation measures and insurance options.

The serious game *WhereWeMove* (Arevalo et al., 2024) provides the conceptual foundation for this model. Game mechanics and decision rules are translated into computational rules, allowing the behavioural logic of the game to be **scaled up** and systematically analysed across many simulation runs and policy scenarios.

Building upon this original model, this repository includes an extended version that shifts the focus from policy analysis to the role of household characteristics, specifically wealth and prior flood experience, in shaping adaptation behaviour. This extension addresses the following research question: What is the effect of wealth and prior flood experience on the adoption of preventive flood measures among households? To enable this, a structured scenario framework was implemented in which 27 scenarios are systematically simulated, combining three wealth levels, three experience levels and three population sizes.

In addition, the model was expanded with dedicated analysis scripts to evaluate simulation outcomes. This includes a sensitivity analysis and a one-way ANOVA to statistically assess the influence of key model parameters such as measure thresholds, damage costs and experience weights on adaptation behaviour.

---

## Objective
The primary objective of this agent-based model is **policy analysis** rather than prediction. The model is used to:

- Compare the behavioural effects of different flood policy regimes  
- Analyse substitution, crowding-out and moral hazard effects  
- Examine whether policy-induced behavioural changes translate into differences in satisfaction and inequality  
- Explore how household-level decision-making aggregates into system-level outcomes  

By translating the serious game into an ABM, the model enables **upscaling** from individual gameplay experiences to population-level patterns, providing a controlled environment for testing policy designs before implementation in participatory or real-world settings.

(extendend by Juliette)  
The primary objective of this extended model shifts from policy analysis to understanding household adaptation behaviour under flood risk. The model is used to:

- Analyse how wealth differences influence the adoption of preventive flood measures  
- Examine how prior flood experience affects threat appraisal and adaptation decisions  
- Compare behavioural outcomes across different combinations of wealth and experience scenarios  
- Identify how financial constraints shape not only whether measures are adopted, but also which measures are chosen  
- Evaluate how individual decision-making processes translate into aggregate patterns of measure adoption  
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

- **/figures_N_effect and /figures_experience_effect and /figures_wealth_effect and make_experience_plots.py and plot_wealth_effect.py**
  Contain figures showing the effects of population size (N), flood experience and wealth on model outcomes, such as the average number of adopted measures per agent.

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

- **anova_analysis.py and anova_ervaring.py and anova_results.py and anova_welvaart.py**
  Perform statistical analyses on the simulation results, including one-way ANOVA and Tukey post-hoc tests, to evaluate differences between wealth and experience groups.

- **run_scenarios.py**
  Runs all simulation scenarios by varying wealth, flood experience and population size, and aggregates the results for analysis and export.

- **sensitivity.py**
  Performs sensitivity analysis by varying key model parameters and evaluating their effect on the average number of adopted measures per agent.

- **convergence.py**
  Tests model convergence by running multiple simulations and tracking the running average of outcomes to assess stability.

- **validation_excel.py**
  Validates the model by comparing simulation outputs with data from WhereWeMove game sessions, focusing on the distribution of satisfaction over time.

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

For the extended model, plots related to scenario experiments (wealth, experience and population size effects) are generated separately and stored in dedicated folders ( /figures_wealth_effect, /figures_experience_effect, /figures_N_effect).  

## Reproducibility
To reproduce results from scratch, clear the /results and /plots directories and rerun experiment.py.

## Use of AI

ChatGPT was used exclusively to support the coding process of this agent-based model. Its use was limited to improving code quality and development efficiency and did not influence the conceptual model design, behavioural assumptions, or interpretation of results.

ChatGPT was used for:

- Improving code readability and structure
- Adding and standardising comments and docstrings
- Supporting debugging and identifying implementation errors
- Discussing implementation details to verify that code reflected intended modelling logic

All substantive modelling decisions, simulation results, and analyses were produced by the authors. ChatGPT functioned as a supportive development tool comparable to advanced code editors or peer discussion, and full responsibility for the model and its outcomes remains with the authors.

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

**Thesis title:**  
*From Game to Protection Against Damage: An Agent-Based Model of Flood Adaptation Behaviour*  

**Author:**  
Juliette Folkers  

**Programme:**  
BSc Technology, Policy and Management, Delft University of Technology  

**Year:**  
2026  

The model implements a scenario-based experimental design focusing on variations in household wealth and prior flood experience. It includes additional analyses, such as sensitivity analysis and statistical testing, to systematically evaluate how these factors influence the adoption of preventive flood measures and overall model outcomes.
