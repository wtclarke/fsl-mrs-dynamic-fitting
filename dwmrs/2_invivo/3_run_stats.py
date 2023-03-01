from subprocess import run
import tempfile
from pathlib import Path
import numpy as np


fit_path = Path('fits_scaled')
group_dir = Path('group_results')
group_dir.mkdir(exist_ok=True)

# 1. Create list of results
all_wt = sorted(list((fit_path / 'wt').rglob('dyn_results.csv')))
all_cntf = sorted(list((fit_path / 'cntf').rglob('dyn_results.csv')))

all_dir = [str(x.parent) for x in all_wt] + [str(x.parent) for x in all_cntf]

with open(group_dir / 'results_list', 'w') as rl:
    rl.write('\n'.join(all_dir))

# 2. Create design and contrast matrices
design_mat = np.zeros((len(all_dir), 2))
design_mat[:len(all_wt), 0] = 1.0
design_mat[len(all_wt):, 1] = 1.0
# print(design_mat)

contrast_mat = np.array([[1, 0], [0, 1], [1, -1], [-1, 1]])
# contrast_mat = np.array([[1, -1], [-1, 1]])
# print(contrast_mat)

with tempfile.TemporaryDirectory() as tmpdirname:
    temp_dir = Path(tmpdirname)
    np.savetxt(temp_dir / 'desmat', design_mat)
    np.savetxt(temp_dir / 'conmat', contrast_mat)

    run(['Text2Vest', temp_dir / 'desmat', group_dir / 'design.mat'])
    run(['Text2Vest', temp_dir / 'conmat', group_dir / 'design.con'])

# 3. Run stats
run([
    'fmrs_stats',
    '--data', group_dir / 'results_list',
    '--output', group_dir / 'unparied_ttest',
    '--hl-design', group_dir / 'design.mat',
    '--hl-contrasts', group_dir / 'design.con',
    '--hl-contrast-names', "WT", "CNTF", "WT>CNTF", "CNTF>WT", 
    '--overwrite',
    '--verbose'])
