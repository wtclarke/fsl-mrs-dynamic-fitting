# Two Peak fMRS Simulation

This section extends the analysis of the previous two-peak simulation to simulation of a full 3 tesla 1H-MRS spectrum containing 21 metabolites. In turn, for each metabolite, 500 fMRS series (of 60 spectra with a 30 spectra 'stimulation' period) are simulated. The selected metabolite experiences a 20% increase during the stimulation period. No BOLD effect (line-narrowing) is simulated. Fitting of all spectral series is performed independently and using FSL-MRS dynamic tools supplied with the correct fitting model. Noise is calibrated to give a matched-filter NAA SNR of 25-35, and line-broadening to give a FWHM of NAA of either 5.9 (excellent FWHM) or 9.7 Hz (adequate FWHM).

The ratio of uncertainty of fMRS parameters (delta concentration) of independent and spatio-temporal fitting was calculated for each metabolite changing in that particular simulation, and plotted as a function of mean parameter correlation.

## Contents
- `prototyping_and_analysis.ipynb` contains the initial exploration of the simulation and prototyping of the scripted python code. Also contains the analysis and figure generation code. Part C & D of Figure 2 are generated in this section. Supporting figure S5 is also generated here.
- `run_mc.py` runs a single case of the monte-carlo simulation (i.e. N repetitions of one separation, delta, and noise level)
- `run_full_mc.py` repeatedly calls `run_mc.py` to generate the full simultion results.
- `sim_results` contains the numerical results of the simulation.
- `basisset_JMRUI` and `challenge_basis` contain the basis spectra distributed by the MRS fitting challenge team in original jMRUI text format and fsl-mrs format respectively.
- `dyn_model.py` contains the temporal (GLM) fitting model.

## Running the simulation
Having installed FSL, FSL-MRS and its dependencies (see top level readme), run the simulation using:
```
python run_full_mc.py
```
Append `--parallel` if hardware capable of exploiting `fsl_sub` is available.

Generate figures by running the python notebook `prototyping_and_analysis.ipynb` e.g. using Jupyter.