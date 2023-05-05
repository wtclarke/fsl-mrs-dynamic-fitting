# Simultaneous fitting of spectral and dynamic models to 2D MRS
### Clarke, Ligneul, Cottaar, Ip & Jbabdi. 2023.

This repository contains the source code, data, and analysis results for the publication `Simultaneous fitting of spectral and dynamic models to 2D MRS` published by `Clarke, Ligneul, Cottaar, Ip & Jbabdi`, Wellcome Centre for Integrative Neuroimaging (WIN), University of Oxford, in 2023.

The accompanying paper is **not** yet available. This will be updated once available online as a preprint.

## Contents
This repository contains sections pertaining to each subsection in the methods and results of the accompanying paper. Additionally, the figures generated for the paper and supporting information are contained in the `publication` subdirectory.

### Sections
1. Edited MRS (`editing`)- Contains simulations showing the advantage of fitting two-condition, MEGA-edited data with a dynamic approach, over the traditional differencing approach.
2. Functional MRS (`fmrs`) - Contains four subsections exploring:
- numerical validation of the advantage of dynamic fitting,
- a demonstration and software validation on synthetic data, and,
- a reproduction of published results on human, in vivo data.
3. Diffusion weighted MRS (`dwmrs`) - Contains two subsections:
- a demonstration of fitting a simple (ball and two sticks) diffusion model to synthetic data, and,
- a reproduction of published results on in vivo data.

## Running the code
Each section contains further documentation and breakdown of the subsections, including how to run and generate the results.

To get a local copy of this repository `git clone https://git.fmrib.ox.ac.uk/wclarke/fsl-mrs-dynamic-fitting.git`. Install [Git LFS](https://git-lfs.com/) before cloning as some files are stored using it.

## Requirements
To run the code in this repository you will need to install FSL-MRS. An ipython kernel will be required to run any of the python notebooks. The [Nilearn](https://nilearn.github.io/stable/index.html) package is required for the fMRS components. All requirements are best installed using the package manager _conda_. Briefly, after installing conda:

```
conda install -c conda-forge \
              -c https://fsl.fmrib.ox.ac.uk/fsldownloads/fslconda/public/ \
              fsl_mrs ipython nilearn

```

Full installation instructions (including how to use conda) can be found in FSL-MRS's online help [documentation](https://open.win.ox.ac.uk/pages/fsl/fsl_mrs/install.html)

## Licence
The code in this repository is released under the BSD 3-clause licence (see LICENCE file). The anonymised data, and simulated data in this repository is released into the public domain. Raw data is available via the WIN Open Data route.

Please cite the accompanying paper **[DOI TO DO]** if you use any part of this work.

## Contact & Help
Please contact the corresponding author, [Will Clarke](https://www.win.ox.ac.uk/people/william-clarke) for information about the scientific content. Issues with the code samples can be raised via the GitHub Issues page or via the [FSL JISC mailing list](mailto:FSL@JISCMAIL.AC.UK).

For help with MRS concepts we recommend the [MRSHub discussion boards](https://forum.mrshub.org/).

### Code documentation
Documentation for the underlying FSL-MRS tool is [online](fsl-mrs.com).

### Accompanying talks
Aspects of this work, specifically fMRS, were presented at ISMRM 2022, as abstract #0309 `Dynamic fitting of functional MRS, diffusion weighted MRS, and edited MRS using a single interface`, and as a talk `Using all the Information: Fitting Functional MRS with a GLM` in the member initiated session `Functional MRS: Current Challenges & Cutting-Edge Methods`.