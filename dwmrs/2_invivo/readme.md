# In vivo dwMRS example

This section replicates an analysis approach from [published work](https://doi.org/10.1016/j.neuroimage.2019.02.046) (full citation below). The originating study applied multi-b-value dwMRS to study changes in cell microstructure in two pre-clinical cohorts, one undergoing pharmacological modulation (here labelled as CNTF). The original study found moth changes in metabolite concentrations and diffusion properties. In this work we use this data as a demonstration of the dynamic fitting tools for real-world dwMRS by replicating the results of the original study.

## Data
The data is taken from:
Ligneul C, Palombo M, Hernández-Garzón E, et al. _Diffusion-weighted magnetic resonance spectroscopy enables cell-specific monitoring of astrocyte reactivity in vivo_. NeuroImage 2019;191:457–469.
doi: [10.1016/j.neuroimage.2019.02.046](https://doi.org/10.1016/j.neuroimage.2019.02.046).

The original data is hosted and available from [Zenodo]().

The data packaged with this git repository is already preprocessed, as provided by the original study authors. Minor additional preprocessing to align across b-values was applied for this work. The original dat was supplied in .mat format and was converted to NIfTI-MRS for use here. The data can be recreated by running the first (optional) step listed below.

## How to run the analysis & generate the figures

Follow the steps in order below.

Note the dynamic fitting (step 3) can take a long time, and it is recommended to run this on a suitable computing cluster.

__Optionally__
1. Download the original `.mat` formatted data from [Zenodo]() and run `0a_convert_and_process.py`. This applies additional preprocessing to the data provided by the original authors and generates NIfTI-MRS format files.
```
python 0a_convert_and_process.py path_to_data_dir nifti/
```
2. Run `0b_group_avg_optim_basis.py.py` to run optimisation of the basis set for FSL-MRS. The original basis set provided by the authors was formatted for LCModel, FSL-MRS requires a different file format, no TMS (0 ppm) signal and does not allow peaks to shift.
```
python 0b_group_avg_optim_basis.py
```

_All files generated in the above steps and required for subsequent steps are included pre-generated in the repository._

__Run the main steps__

3. Run `1_fit_dwmrs.py`. This runs fitting over all datasets. Append `--parallel` to exploit any hardware capable of using the `fsl_sub` interface.
```
    python 1_fit_dwmrs.py nifti/ fits
```
4. Run `2_scale_amplitudes.py` to perform referencing of metabolite concentrations to total creatine. This generates the `fits_scaled` directory
```
python 2_scale_amplitudes.py 
```

5. Run `3_runs_stats.py` to perform group level stats, genertign the `group_results` directory. This calls the FSL-MRS `fmrs_stats` tool.
```
python 3_runs_stats.py 
```

__Run the plotting scripts__

6. Run `results_and_figures.ipynb` to generate the outputs and results figures.
