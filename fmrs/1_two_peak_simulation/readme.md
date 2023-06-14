# Two Peak fMRS Simulation

This section numerically replicates the theoretical findings of Tal [The future is 2D: spectral-temporal fitting of dynamic MRS data provides exponential gains in precision over conventional approaches](https://doi.org/10.1002/mrm.29456), using FSL-MRS tools. Tal finds 2D (joint spectral-temporal) fitting decreases uncertainty in parameters relating to the magnitude of metabolite concentration changes. This is shown in a simple two-peak toy case, and the decrease is dependent on the separation of the peaks (i.e. the correlation between peak fitting parameters).

This work replicates that finding using the FSL-MRS fitting framework. Additionally, simulation is extended to the case where the 'nuisance parameters' linewidth and global peak shift are jointly estimated (replicating the likely in vivo case.)

## Contents
- `prototyping.ipynb` contains the initial exploration of the simulation and prototyping of the scripted python code. Supporting figures S2 and S3 are generated here.
- `run_mc.py` runs a single case of the monte-carlo simulation (i.e. N repetitions of one separation, delta, and noise level)
- `run_full_mc.py` repeatedly calls `run_mc.py` to generate the full simultion results. I.e. across multiple separations and noise levels.
- `sim_results` and `sim_results_fixed` contain the numerical results of the simulation for the two cases (per-peak lw/shift and fixed lw/shift).
- `generate_results_and_figures.ipynb` contains the analysis and figure generation code. Part A & B of Figure 2 are generated in this section.

## Running the simulation
Having installed FSL, FSL-MRS and its dependencies (see top level readme), run the simulation using:
```
python run_full_mc.py
```
Append `--parallel` if hardware capable of exploiting `fsl_sub` is available.

Generate figures by running the python notebook `generate_results_and_figures.ipynb` e.g. using Jupyter.