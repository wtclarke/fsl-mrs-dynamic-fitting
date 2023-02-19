'''Run the second level analysis steps for each case

Use paired t-test higher-level design
'''

from subprocess import run
from pathlib import Path

misc = Path('misc')


def run_fmrs_stats(results_list, output, paired_ttest=False):
    cmd = [
        'fmrs_stats',
        '--data', results_list,
        '--output', output,
        '--fl-contrasts', misc / 'fl_contrasts.json',
        '--combine', 'NAA', 'NAAG',
        '--combine', 'Cr', 'PCr',
        '--combine', 'PCho', 'GPC',
        '--combine', 'Glu', 'Gln',
        '--overwrite']
    if paired_ttest:
        cmd += [
            '--hl-design', misc / 'design.mat',
            '--hl-contrasts', misc / 'design.con',
            '--hl-contrast-names', "STIM>CTRL", "CTRL>STIM"]
    else:
        cmd += [
            '--hl-design', misc / 'design_ga.mat',
            '--hl-contrasts', misc / 'design_ga.con',
            '--hl-contrast-names',
            "open +ve", "open -ve", "closed +ve", "closed -ve"]
    run(cmd, check=True)


results_list_fixed = Path('first_level_fit_fixed') / 'first_level_results.txt'
results_list_var = Path('first_level_fit_var') / 'first_level_results.txt'

output = Path('group_results')
output.mkdir(exist_ok=True)

run_fmrs_stats(
    results_list_fixed,
    output / 'fixed_paired',
    paired_ttest=True)
run_fmrs_stats(
    results_list_var,
    output / 'var_paired',
    paired_ttest=True)

run_fmrs_stats(
    results_list_fixed,
    output / 'fixed_group_mean',
    paired_ttest=False)
run_fmrs_stats(
    results_list_var,
    output / 'var_group_mean',
    paired_ttest=False)
