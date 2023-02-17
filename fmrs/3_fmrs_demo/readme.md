# Simulated fMRS

Code mostly relies upon the fMRS demo that accompanies FSL-MRS, and that was original generated for the ISMRM 2022 meeting.

Here we expand the analysis to compare with GLM fitting of the independently fitted spectra (used for dynamic fitting initialisation), and generate figures for this publication.

## Retrieving the fMRS demo code
The majority of the code for this component resides in the [FSL-MRS fMRS fitting demo repository](https://github.com/wtclarke/fsl_mrs_fmrs_demo), separately hosted on GitHub. This repository has been added as a [submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) to this repository. To receive a version fo the submodule repository when you clone this repository add `--recurse-submodules` to the `git clone` call.