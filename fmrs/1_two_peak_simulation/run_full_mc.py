import argparse
from subprocess import run
from pathlib import Path

parser = argparse.ArgumentParser(
    description='Run first-level dynamic fMRS fitting.')
parser.add_argument('--parallel', action='store_true',
                    help='Run in cluster job submission mode')
args = parser.parse_args()

if not args.parallel:
    print('This will take a long time run like this!')


def cmd_series(sep, noise, delta, reps, output):
    return ['python',
            'run_mc.py',
            str(sep),
            str(noise),
            str(delta),
            str(reps),
            '--output', str(output)]


def cmd_parallel(*args):
    return ['fsl_sub', '-q', 'veryshort.q'] + cmd_series(*args)


out_dir = Path('sim_results')
out_dir.mkdir(exist_ok=True)

reps = 100
delta = 0.2
sep_vec = (0.2, 0.4, 0.6, 0.8, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0)
noise_vec = (0.2E-5, 1E-5, 5E-5)
for nv in noise_vec:
    for sep in sep_vec:
        if args.parallel:
            cmd = cmd_parallel(sep, nv, delta, reps, out_dir)
        else:
            cmd = cmd_series(sep, nv, delta, reps, out_dir)
        run(cmd)
