# Dynamic fitting of functional MRS (fMRS) data.

This section contains four subsections:

1. `two_peak_simulation` replicates the theoretical findings of Tal's work [The future is 2D: spectral-temporal fitting of dynamic MRS data provides exponential gains in precision over conventional approaches](https://doi.org/10.1002/mrm.29456), numerically, using FSL-MRS tools.
2. `fmrs_spectrum_simulation` extends the simulations done in #1 to a simulations of realistic in vivo 1H-MRS spectra.
3. `fmrs_demo` demonstrates the full fMRS toolset in FSL-MRS on a simulated multi-subject, two-condition dataset, created using reported values. The tool's implementation is validated using this simulation.
4. `fmrs_invivo_example` uses the fsl-mrs dynamic fitting tools to replicates the results of [published work](https://doi.org/10.1016/j.neuroimage.2017.04.030) performing human in vivo visual stimulation.

The first two subsections correspond to `Functional MRS – Simulation`, the third subsection to `Functional MRS – Demo`, and the fourth subsection to `Functional MRS – In vivo` in the paper's _Methods_ and _Results_.