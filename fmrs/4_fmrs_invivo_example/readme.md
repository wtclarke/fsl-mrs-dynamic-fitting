# fMRS #4: In vivo example

This section runs GLM constrained fitting of a previously published visual stimulation fMRS study. It compares this fitting when using a fixed linewidth constraint and one that anticipates a BOLD effect on the linewidth.

## Data
The data is taken from:
Ip IB, Berrington A, Hess AT, Parker AJ, Emir UE, Bridge H. _Combined fMRI-MRS acquires simultaneous glutamate and BOLD-fMRI signals in the human brain._ Neuroimage 2017;155:113–119  
doi: [10.1016/j.neuroimage.2017.04.030](https://doi.org/10.1016/j.neuroimage.2017.04.030).

The raw data is hosted and available from [Zenodo](https://doi.org/10.5281/zenodo.7950984).

The preprocessed data is packaged with this git repository. The preprocessed data can be recreated by running the first two (optional) steps listed below.

## Installation & requirements
FSL-MRS version >= 2.1.0. Please see the [FSL-MRS documentation](http://www.fsl-mrs.com/) for instructions on [installing and setting up a Conda environment](https://open.win.ox.ac.uk/pages/fsl/fsl_mrs/conda.html#conda) and subsequently installing [FSL-MRS](https://open.win.ox.ac.uk/pages/fsl/fsl_mrs/install.html#option-1-using-conda)

To use the packaged script `run_all.sh` you will require an FSL installation. Please see the [online instructions](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation) on how to install for your system.

## How to run the analysis & generate figures

All steps (1-6 below) can be run using the `run_all.sh` script. Note the dynamic fitting (step 6 below) will take a long time, and it is recommended to run this on a suitable computing cluster.

__Optionally__
1. Download the unprocessed NIfTI-MRS data from [Zenodo](https://doi.org/10.5281/zenodo.7950984). This data was converted from DICOM scanner outputs using `0a_convert.py`, which calls `spec2nii` (use `python 0a_convert.py path_to_data_dir nifti/`). The raw (unconverted) DICOM data is available on request.
2. Run `0b_preprocess.py` to preprocess the unprocessed NIfTI-MRS data. This includes forming the average data.
```
python 0b_preprocess.py nifti/ processed
```
3. Run `0c_avg_fit_qc_and_basis.py` to perform the fit to the average data (for QC) and to convert and optimise the basis set. The LCModel-formatted basis `7T_slaser36ms_2013_oxford_tdcslb1_ivan.BASIS` used in the original study is available from [Zenodo](). After running this stage the averaged data can be visualised using `fsl_mrs_summarise dir averaged_fits`. 

```
python 0c_avg_fit_qc_and_basis.py
```

4. Run `0d_generate_design_matrix.py` to generate the design matrix for the first-level GLM fitting. The command-line interface accepts inputs for number of transients (128), number of OFF-ON blocks (4), number of transients per ON block (16), TR (4.0 s) and output location.
```
python 0d_generate_design_matrix.py 128 4 16 4.0 ./design_matrix.csv
```
5. Run `0e_generate_hl_designs.py` to create the higher-level GLM (group analysis) design and contrast matrices.
```
python 0e_generate_hl_designs.py
```

_All files generated in the above steps  and required for subsequent steps are included pre-generated in the repository._

__Run the main steps__

7. Run `1_first_level_dynamic_fit.py` with and without the linewidth model. This is repeated twice times for with and without the linewidth model. Append `--parallel` to exploit any hardware capable of using the `fsl_sub` interface.
```
    python 1_first_level_dynamic_fit.py processed/ first_level_fit_fixed
    python 1_first_level_dynamic_fit.py processed/ first_level_fit_var --model_lw
```
8. Run `2_second_level_glm.py` to perform the higher-level, group statistics.
```
python 2_second_level_glm.py
```

__Run the plotting scripts__

9. Run `figures.ipynb` to generate the output tables and results figures.
