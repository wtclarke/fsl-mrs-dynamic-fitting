"""

W T Clarke, University of Oxford, April 2022.
"""

import argparse
from subprocess import run
from pathlib import Path

parser = argparse.ArgumentParser(
    description='Run dynamic dwMRS fitting.')
parser.add_argument('dir', type=Path,
                    help='Input directory containing nifti-mrs files.')
parser.add_argument('output', type=Path,
                    help='Output location.')
parser.add_argument('--parallel', action='store_true',
                    help='Run in cluster job submission mode')
args = parser.parse_args()

if not args.parallel:
    print('This will take a long time run like this!')


def cmd_series(path, output):
    return ['fsl_dynmrs',
            '--data', str(path),
            '--basis', 'basis_optim',
            '--dyn_config', 'dmrs_model_biexp_mm_lin.py',
            '--time_variables', 'bvals',
            '--lorentzian',
            '--baseline_order', '1',
            '--metab_groups', 'MM_WT_',
            '--output', str(output),
            '--report',
            '--overwrite']


def cmd_parallel(pathin, output):
    return ['fsl_sub', '-q', 'short.q'] + cmd_series(pathin, output)


our_dir = args.output
our_dir.mkdir(exist_ok=True, parents=True)

n_sub = len(list(args.dir.glob('*.nii.gz')))
for idx, sub in enumerate(args.dir.glob('*.nii.gz')):
    sub_str = sub.with_suffix('').with_suffix('').name
    out_loc = our_dir / sub_str
    if args.parallel:
        run(cmd_parallel(sub, out_loc))
    else:
        run(cmd_series(sub, out_loc))
        print(f'Subject {idx+1}/{n_sub} done.')
