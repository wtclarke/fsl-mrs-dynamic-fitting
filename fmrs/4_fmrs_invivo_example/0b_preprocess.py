'''Preprocess converted (nifti) data.

Output for each subject, and each condition:
1. The unaveraged, but otherwise preprocessed metabolite data
2. A processed water reference scan.
3. The averaged data for each subject.

Also output:
4. The all-subject average
'''

from pathlib import Path
import subprocess

import numpy as np
import argparse

from fsl_mrs.utils import mrs_io
from fsl_mrs.core.nifti_mrs import tools as ntools
from fsl_mrs.core.nifti_mrs import NIFTI_MRS
from fsl_mrs.utils.preproc import nifti_mrs_proc as nproc

parser = argparse.ArgumentParser(description='Preprocess the fMRS NIfTI files')
parser.add_argument('input', type=Path,
                    help='Location of ptXX folders containing NIfTI files')
parser.add_argument('output', type=Path,
                    help='Location to output the proccessed files')
args = parser.parse_args()

# Generate output directories
open_out_dir = args.output / 'open'
open_out_dir.mkdir(exist_ok=True, parents=True)
closed_out_dir = args.output / 'closed'
closed_out_dir.mkdir(exist_ok=True)
overall_dir = args.output / 'group_avg'
overall_dir.mkdir(exist_ok=True)


# Apply fsl_mrs_preproc with --fmrs option
def run_preproc_single_subject(data, ref1, ref3, output):
    subprocess.run([
        'fsl_mrs_preproc',
        '--data', str(data),
        '--quant', str(ref3),
        '--reference', str(ref1),
        '--output', str(output),
        '--leftshift', '2',
        '--hlsvd',
        '--fmrs',
        '--report',
        '--overwrite'],
        check=True)


def average_data(data_in, data_out):
    subprocess.run([
        'fsl_mrs_proc', 'average',
        '--file', str(data_in),
        '--output', str(data_out),
        '--dim', 'DIM_DYN',
        '--filename', 'averaged'],
        check=True)


# Loop over subjects
all_averaged = []
for idx, pt in enumerate(args.input.glob('P0*')):
    print(f'Running {idx + 1}/13')
    curr_met_open = pt / 'metab_open.nii.gz'
    curr_met_closed = pt / 'metab_closed.nii.gz'
    curr_wref1 = pt / 'wref1.nii.gz'
    curr_wref3 = pt / 'wref3.nii.gz'

    # run_preproc_single_subject(
    #     curr_met_open,
    #     curr_wref1,
    #     curr_wref3,
    #     open_out_dir / pt.name)

    # run_preproc_single_subject(
    #     curr_met_closed,
    #     curr_wref1,
    #     curr_wref3,
    #     closed_out_dir / pt.name)

    # Create averaged data for each subject
    # average_data(
    #     open_out_dir / pt.name / 'metab.nii.gz',
    #     open_out_dir / pt.name)
    # average_data(
    #     closed_out_dir / pt.name / 'metab.nii.gz',
    #     closed_out_dir / pt.name)

    all_averaged.append(open_out_dir / pt.name / 'averaged.nii.gz')
    all_averaged.append(closed_out_dir / pt.name / 'averaged.nii.gz')


# Create group average.
def rescale(nmrsimg):
    scale = np.linalg.norm(nmrsimg.mrs().get_spec(ppmlim=(0.2, 4.2)))
    return NIFTI_MRS(nmrsimg[:] * 1 / scale, header=nmrsimg.header)


all_averaged = [mrs_io.read_FID(file) for file in all_averaged]
all_rescaled = [rescale(fid) for fid in all_averaged]
all_reordered = [
    ntools.reorder(fid, ['DIM_DYN', None, None]) for fid in all_rescaled]
avg_all = ntools.merge(all_reordered, 'DIM_DYN')
avg_all = nproc.align(avg_all, 'DIM_DYN', ppmlim=(0.2, 4.2))
avg_all = nproc.average(avg_all, 'DIM_DYN')
avg_all.save(overall_dir / 'group_average.nii.gz')
