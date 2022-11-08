import numpy as np
import fsl_mrs.utils.synthetic as synth
from fsl_mrs import dynamic as dyn
from nilearn.glm.first_level import make_first_level_design_matrix
import pandas as pd
import warnings
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(
    description='Run a single metabolite of the dynamic fMRS MC sim.')
parser.add_argument('metabolite', type=str,
                    help='Metabolite name')
parser.add_argument('noise_level', type=float,
                    help='Noise level')
parser.add_argument('lw', type=float,
                    help='Linewidth parameter')
parser.add_argument('delta', type=float,
                    help='fMRS delta')
parser.add_argument('mc_reps', type=int,
                    help='Number of MC reps')
parser.add_argument('--output', type=Path,
                    help='Output location')
args = parser.parse_args()


# Spectral model

baseline_concs = {
    'Ala': 0.6,
    'Asc': 1.2,
    'Asp': 2.4,
    'Cr': 4.87,
    'GABA': 1.2,
    'GPC': 0.74,
    'GSH': 1.2,
    'Glc': 1.2,
    'Gln': 3.37,
    'Glu': 12.41,
    'Gly': 1.2,
    'Ins': 7.72,
    'Lac': 0.6,
    'Mac': 5,
    'NAA': 13.8,
    'NAAG': 1.2,
    'PCho': 0.85,
    'PCr': 4.87,
    'PE': 1.8,
    'Tau': 1.8,
    'sIns': 0.3}


def single_spectrum(concs_in, noise=200, lw=(14.0, 0.0)):
    synth_spec, mrs, _ = synth.syntheticFromBasisFile(
        'challenge_basis',
        points=1024,
        bandwidth=2000,
        broadening=lw,
        noisecovariance=[[noise]],
        concentrations=concs_in)
    mrs.FID = synth_spec
    return mrs


# Temporal model
tr = 2
ta = 120
stim_duration = 60
stim_start = 30

nt = int(ta / tr)
stim_steps = int(stim_duration / tr)
stim_start_step = int(stim_start / tr)


def boxcar(delta):
    response = np.ones(nt)
    response[stim_start_step:(stim_start_step+stim_steps)] += delta
    return response


# Combined temporal + spectral
def gen_timeseries(metabolite, delta, base_concs, **kwargs):
    mrs_list = []
    design = boxcar(delta)
    concs_in = base_concs.copy()
    for factor in design:
        concs_in[metabolite] = base_concs[metabolite] * factor
        mrs_list.append(single_spectrum(concs_in, **kwargs))
    return mrs_list


# Fitting
frame_times = np.arange(60) * tr
conditions = ['STIM', ]
duration = [stim_duration, ]
onsets = [stim_start, ]  # Start time of each stimulation block.
events = pd.DataFrame({'trial_type': conditions,
                       'onset': onsets,
                       'duration': duration})

design_matrix = make_first_level_design_matrix(
    frame_times,
    events,
    drift_model='polynomial',
    drift_order=0,
    hrf_model='fir'
)

Fitargs = {
    'baseline_order': 0,
    'ppmlim': (0.2, 4.2),
    'model': 'lorentzian'}


def one_rep(metabolite, delta, base_concs, noise, lw):
    obj = dyn.dynMRS(
        gen_timeseries(metabolite, delta, base_concs, noise=noise, lw=(lw, 0)),
        design_matrix.to_numpy(),
        'dyn_model.py',
        rescale=False,
        **Fitargs)

    init = obj.initialise(verbose=False)
    dyn_fit = obj.fit(init=init)
    return dyn_fit.init_free_dataframe, dyn_fit.mean_free


# Run MC sim
dyn_df = []
init_df = []
for rep in range(args.mc_reps):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        out = one_rep(
            args.metabolite,
            args.delta,
            baseline_concs,
            args.noise_level,
            args.lw)
    dyn_df.append(out[1])
    init_df.append(out[0])

all_dyn = pd.concat(dyn_df, axis=1).T
all_init = pd.concat(init_df, axis=1).T

all_dyn.to_csv(
    args.output /
    f'dynamic_{args.metabolite}_{args.noise_level}_{args.lw}_{args.delta}.csv')
all_init.to_csv(
    args.output /
    f'init_{args.metabolite}_{args.noise_level}_{args.lw}_{args.delta}.csv')
