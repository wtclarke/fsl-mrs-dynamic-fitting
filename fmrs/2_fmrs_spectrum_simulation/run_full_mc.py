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


def cmd_series(metabolite, noise, lw, delta, reps, output):
    return ['python',
            'run_mc.py',
            metabolite,
            str(noise),
            str(lw),
            str(delta),
            str(reps),
            '--output', str(output)]


def cmd_parallel(*args):
    return ['fsl_sub', '-q', 'short.q'] + cmd_series(*args)


out_dir = Path('sim_results')
out_dir.mkdir(exist_ok=True)

reps = 500
delta = 0.2
noise_vec = (200, )
lw_vec = (11.0, 23.0)
metabolites = [
    'Ala',
    'Asc',
    'Asp',
    'Cr',
    'GABA',
    'GPC',
    'GSH',
    'Glc',
    'Gln',
    'Glu',
    'Gly',
    'Ins',
    'Lac',
    'Mac',
    'NAA',
    'NAAG',
    'PCho',
    'PCr',
    'PE',
    'Tau',
    'sIns']
for nv in noise_vec:
    for lw in lw_vec:
        for met in metabolites:
            if args.parallel:
                cmd = cmd_parallel(met, nv, lw, delta, reps, out_dir)
            else:
                cmd = cmd_series(met, nv, lw, delta, reps, out_dir)
            run(cmd)
