# Simulation of dwMRS multi-direction models
This simulation explores the ability of the dynamic fitting tools to simultaneously fit spectral and diffusion models across multiple diffusion gradient directions. Here we make and fit synthetic data using a [ball and two sticks model](http://www.ncbi.nlm.nih.gov/pubmed/22334356). The simulation implements three metabolite signals representative of metabolites thought to have different compartmentalisation: NAA in neurons, myo-inositol in glia, and creatine in both. The simulation explores the ability to use the model fitting few (six) direction data and many (sixty) direction data. The code demonstrates one way to initialise such models which contain degeneracies by calling existing FSL tools for water imaging (`FSL xfibres`).

The code in this subdirectory corresponds to `Diffusion-weighted MRS – Simulation` in the paper.

## Contents
- `ball_and_sticks_simulation.ipynb` contains the simulation and figure generation code.
- `model_ball2sticks.py` is the ball and two sticks dynamic fitting configuration file.
- `basis` contains the simulated spectral basis set. This basis set was taken from data distributed for the workshop "Best practices and tools for Diffusion MR Spectroscopy” workshop, which took place at the Lorentz center in Leiden (NL) in September 2021. The original basis set is available [online](https://github.com/dwmrshub/pregame-workshop-2021)
- `create_siemens_directions.py` is the python script used to create the direction files.
- `b_1000_3000_{N}dir` contains the specified b values and gradient directions created by `create_siemens_directions.py`.

## Running the simulation
After generating the direction files using `create_siemens_directions.py`, this simulation is run entirely within the `ball_and_sticks_simulation.ipynb`  notebook. This notebook generates the `ig9_ball_and_sticks_sim.png` figure (Figure 9).

The specific direction files can be generated using the following commands.

```
python create_siemens_directions.py -b 1000 3000 -n 6 -z 1 --save_bfiles --out b_1000_3000_6dir
python create_siemens_directions.py -b 1000 3000 -n 60 -z 10 --save_bfiles --out b_1000_3000_60dir
```