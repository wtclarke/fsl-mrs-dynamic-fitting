import numpy as np
import fsl_mrs.utils.synthetic as syn
from fsl_mrs.core import MRS, basis
from fsl_mrs import dynamic as dyn
from nilearn.glm.first_level import make_first_level_design_matrix
import pandas as pd
import warnings
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(
    description='Run a single rep of the dynamic fMRS MC sim.')
parser.add_argument('separation', type=float,
                    help='Separation d value')
parser.add_argument('noise_level', type=float,
                    help='Separation d value')
parser.add_argument('delta', type=float,
                    help='fMRS delta')
parser.add_argument('mc_reps', type=int,
                    help='Number of MC reps')
parser.add_argument('--output', type=Path,
                    help='Output location')
args = parser.parse_args()


# Spectral model
spectral_width = 64
points = 64
fwhm = 8
delta = fwhm / 2.355


def separations(d):
    separation = d * np.sqrt(2) * 8
    return (-separation/2, separation/2)


def spectrum_complex(amplitude, frequency, damping, noise=0.0, sw_factor=1.0):
    fid, hdrs = syn.syntheticFID(
                 noisecovariance=[[noise]],
                 bandwidth=spectral_width * sw_factor,
                 points=int(points * sw_factor),
                 chemicalshift=[frequency[0] / 123.2, frequency[1] / 123.2],
                 amplitude=[amplitude[0], amplitude[1]],
                 linewidth=[damping[0], damping[1]],
                 g=[0.0, 0.0])

    # Construct basis simultaneously
    fid_basis_1, hdrs1 = syn.syntheticFID(
                 noisecovariance=[[0]],
                 bandwidth=spectral_width * sw_factor,
                 points=int(points * sw_factor),
                 chemicalshift=[frequency[0] / 123.2, frequency[1] / 123.2],
                 amplitude=[1.0, 0.0],
                 linewidth=[1, 1],
                 g=[0.0, 0.0])
    fid_basis_2, hdrs2 = syn.syntheticFID(
                 noisecovariance=[[0]],
                 bandwidth=spectral_width * sw_factor,
                 points=int(points * sw_factor),
                 chemicalshift=[frequency[0] / 123.2, frequency[1] / 123.2],
                 amplitude=[0.0, 1.0],
                 linewidth=[1, 1],
                 g=[0.0, 0.0])
    basis_fid = np.stack((fid_basis_1[0], fid_basis_2[0]))
    hdrs1['fwhm'] = 1.0
    hdrs2['fwhm'] = 1.0
    fitting_basis = basis.Basis(
        basis_fid,
        names=['A', 'B'],
        headers=[hdrs1, hdrs2])
    return MRS(fid[0], header=hdrs, basis=fitting_basis)


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
def gen_timeseries(delta_b, d, noise=0):
    amp_a = boxcar(0)
    amp_b = boxcar(delta_b)

    mrs_list = []
    for aa, ab in zip(amp_a, amp_b):
        mrs_list.append(
            spectrum_complex(
                (aa, ab),
                separations(d),
                (fwhm, fwhm),
                noise=noise,
                sw_factor=2.0))
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
    'metab_groups': [0, 1],
    'baseline_order': 0,
    'ppmlim': (4.1, 5.2),
    'model': 'lorentzian'}


def one_rep(delta, sep, noise):
    obj = dyn.dynMRS(
        gen_timeseries(delta, sep, noise=noise),
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
            args.delta,
            args.separation,
            args.noise_level)
    dyn_df.append(out[1])
    init_df.append(out[0])

all_dyn = pd.concat(dyn_df, axis=1).T
all_init = pd.concat(init_df, axis=1).T

all_dyn.to_csv(
    args.output /
    f'dynamic_{args.separation}_{args.noise_level}_{args.delta}.csv')
all_init.to_csv(
    args.output /
    f'init_{args.separation}_{args.noise_level}_{args.delta}.csv')
