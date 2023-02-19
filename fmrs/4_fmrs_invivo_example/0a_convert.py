'''Convert raw fMRS data in DICOM format to NIfTI-MRS format'''

from pathlib import Path
from subprocess import run
import argparse

parser = argparse.ArgumentParser(
    description='Convert the fMRS DICOM files to NIfTI-MRS')
parser.add_argument(
    'input',
    type=Path,
    help='Location of ptXX folders containing DICOM files')
parser.add_argument(
    'output',
    type=Path,
    help='Location to output ptXX folders containing NIfTI files')
args = parser.parse_args()

orig_data_dir = args.input
nifti_data_dir = args.output
nifti_data_dir.mkdir(exist_ok=True)

for pt in orig_data_dir.glob('P0*'):
    pt_number = pt.stem
    curr_out = nifti_data_dir / pt_number
    curr_out.mkdir(exist_ok=True)
    out = run(['spec2nii', 'dicom',
               '-o', str(curr_out),
               '-f', 'metab_open',
               '-t', 'DIM_DYN',
               str(pt / 'OCC_fmrs_BothEyesOpen')])
    out = run(['spec2nii', 'dicom',
               '-o', str(curr_out),
               '-f', 'metab_closed',
               '-t', 'DIM_DYN',
               str(pt / 'OCC_fmrs_BothEyesClosed')])
    out = run(['spec2nii', 'dicom',
               '-o', str(curr_out),
               '-f', 'wref1',
               '-t', 'DIM_DYN',
               str(pt / 'OCC_wref1')])
    out = run(['spec2nii', 'dicom',
               '-o', str(curr_out),
               '-f', 'wref3',
               '-t', 'DIM_DYN',
               str(pt / 'OCC_wref3')])
