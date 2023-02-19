'''Generate a block stimulus design matrix.
Block order is [STIM - CTRL -] * n blocks
Blocks are equal length
'''
import argparse
from pathlib import Path

import pandas as pd
import numpy as np
from nilearn.glm.first_level import make_first_level_design_matrix


parser = argparse.ArgumentParser(
    description='Generate a block-wise design matrix')
parser.add_argument('n_transients', type=int,
                    help='Number of transients in data')
parser.add_argument('n_blocks', type=int,
                    help='Number of ON/OFF blocks to use')
parser.add_argument('block_length', type=int,
                    help='Number of transients per ON block')
parser.add_argument(
    'tr',
    metavar='TR',
    type=float,
    help='Duration of each transient (repetition time) in seconds.')
parser.add_argument(
    'output',
    type=Path,
    help='Location and name to output the matrix in csv format')
parser.add_argument(
    '--drift_order',
    type=int,
    default=1,
    help='Polynomial order for drift regressors.')
parser.add_argument(
    '--plot',
    action='store_true',
    help='Plot design matrix.')
args = parser.parse_args()

# Define design matrix for correct number of blocks
# The number of stimulation regressors matches the number of stim blocks
frame_times = np.arange(args.n_transients) * args.tr
conditions = [f'STIM{i}' for i in range(args.n_blocks)]
duration = [args.block_length * args.tr] * args.n_blocks

# onset times
on_off_duration = args.block_length * 2 * args.tr
offset_duration = args.tr * (args.block_length - 1)
onsets = [
    offset_duration + on_off_duration * k for k in np.arange(0, args.n_blocks)]
events = pd.DataFrame({'trial_type': conditions,
                       'onset': onsets,
                       'duration': duration})

design_matrix = make_first_level_design_matrix(
    frame_times,
    events,
    drift_model='polynomial',
    drift_order=args.drift_order,
    hrf_model='glover')

assert design_matrix.shape == (
    args.n_transients,
    args.drift_order + 1 + args.n_blocks)

design_matrix.to_csv(args.output, index=False, header=False)

if args.plot:
    from nilearn.plotting import plot_design_matrix
    from matplotlib import pyplot as plt
    _ = plot_design_matrix(design_matrix)
    plt.show()
