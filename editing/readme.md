# Edited MRS

This directory contains the code for the `Edited-MRS – Simulation` methods and results section.

Briefly, a Monte Carlo simulation is run to generate and fit synthetic spectra pertaining to the on-resonance saturation (ON), control saturation (OFF) conditions. The difference spectrum (DIFF) is formed from each instance of this data. The fitting accuracy (measured to the ground truth) is assessed for different metabolites across three fitting approaches:
1. Just using the control saturation condition.
2. Using the difference spectrum.
3. Dynamically fitting the ON and OFF conditions. 

This simulation is run across different noise levels and linewidhts (simulating different quality spectra).

To run the simulation run `run_all_sim.sh` which makes calls to `run_mc_editing.py`. Results are generated in the notebook `analyse_sim_results.ipynb`.

The explanatory figure for this section (Figure 3) is created in the prototyping notebook `editing_mc_sim_prototype.ipynb` and compiled in `publication/figure_creation/abstract_figures_dynmrs.drawio`.

The file `additional_explanatory_simulation.ipynb` was created in the revision process to explore performance as a function of creatine concentration. The results are not presented in the manuscript.