"""This script optimises the basis set based on group average data
(using fsl-mrs commandline tools).

It then runs a single fit on all datasets to produce and overview of the
data and its quality."""

from subprocess import run
from pathlib import Path

processed = Path('processed')
output = Path('averaged_fits')
output.mkdir(exist_ok=True)
basis = 'original_basis'
mg = 'mm'

# 0. basis conversion
run([
    'basis_tools', 'convert',
    '--remove_reference', '--hlsvd',
    '7T_slaser36ms_2013_oxford_tdcslb1_ivan.BASIS',
    'tmp_basis'])

run([
    'basis_tools', 'conj',
    'tmp_basis', basis])

run(['rm', '-rf', 'tmp_basis'])

# 1. Run fit on group average with free_shift selected
run([
    'fsl_mrs',
    '--data', str(processed / 'group_avg' / 'group_average.nii.gz'),
    '--basis', basis,
    '--output', str(output / 'group'),
    '--metab_groups', mg,
    '--free_shift',
    '--report',
    '--overwrite'])

# 2. Run basis tools to optimise basis set
run([
    'basis_tools',
    'shift_all',
    basis,
    str(output / 'group'),
    'basis'])

# 3. Run averaged fits
for file in processed.rglob('averaged.nii.gz'):
    curr_name = file.parent.name + '_' + file.parent.parent.name
    run([
        'fsl_mrs',
        '--data', str(file),
        '--h2o', str(file.parent / 'wref.nii.gz'),
        '--output', str(output / curr_name),
        '--config', 'misc/sub_avg_fit_config.txt'])
