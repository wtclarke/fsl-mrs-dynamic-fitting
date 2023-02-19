"""This script carries out the first level single-subject fMRS fits.
The script iterates over each of the 13 subjects, either in series
(warning slow!) or in parrallel using a cluster queue submission syntax.
Fits are carried out for both the eyes-open and eyes-closed data identically.

W T Clarke, University of Oxford, April 2022.
"""

import argparse
from subprocess import check_call
from pathlib import Path

parser = argparse.ArgumentParser(
    description='Run first-level dynamic fMRS fitting.')
parser.add_argument('input', type=Path,
                    help='Location of processed data')
parser.add_argument('output', type=Path,
                    help='base output location')
parser.add_argument('--parallel', action='store_true',
                    help='Run in cluster job submission mode')
parser.add_argument('--model_lw', action='store_true',
                    help='Add variable LW to fit')
args = parser.parse_args()

if not args.parallel:
    print('This will take a long time run like this!')

if args.model_lw:
    config_file = Path('misc') / 'fmrs_lw_model.py'
else:
    config_file = Path('misc') / 'fmrs_model.py'


def cmd_series(path, output):
    return ['fsl_dynmrs',
            '--data', str(path),
            '--basis', 'basis',
            '--dyn_config', str(config_file),
            '--time_variables', 'design_matrix.csv',
            '--baseline_order', '1',
            '--metab_groups', 'mm',
            '--output', str(output),
            '--report',
            '--overwrite']


def cmd_parallel(pathin, output):
    return ['fsl_sub', '-q', 'short.q'] + cmd_series(pathin, output)


out_dir = Path(args.output)
(out_dir / 'open').mkdir(exist_ok=True, parents=True)
(out_dir / 'closed').mkdir(exist_ok=True)

all_stim = []
all_ctrl = []
for idx in range(1, 14):
    sub_str = f'P{idx:03.0f}'
    path_stim = args.input / 'open' / sub_str / 'metab.nii.gz'
    path_ctrl = args.input / 'closed' / sub_str / 'metab.nii.gz'

    out_stim = out_dir / 'open' / sub_str
    out_ctrl = out_dir / 'closed' / sub_str

    if args.parallel:
        check_call(
            cmd_parallel(path_stim, out_stim))
        check_call(
            cmd_parallel(path_ctrl, out_ctrl))
    else:
        check_call(
            cmd_series(path_stim, out_stim))
        print(f'Subject {sub_str}: stim done.')
        check_call(
            cmd_series(path_ctrl, out_ctrl))
        print(f'Subject {sub_str}: ctrl done.')
        print(f'Subject {idx+1}/13 done.')

    all_stim.append(out_stim)
    all_ctrl.append(out_ctrl)

to_write = [str(x) + '\n' for x in (all_stim + all_ctrl)]
with open(out_dir / 'first_level_results.txt', 'w') as fp:
    fp.writelines(to_write)
