# Scale all dynamic fit amplitudes to tCr
import re
import pandas as pd
import numpy as np
from pathlib import Path
import shutil


def apply_scaling(dyn_val, dyn_cov):

    indices = dyn_val.index.to_list()
    tcr_index = indices.index('conc_Cr+PCr_c_amp')

    conc_scale = 8.0
    tcr_val = dyn_val.loc['conc_Cr+PCr_c_amp']

    jac = np.eye(dyn_val.shape[0])
    conc_ptrn = re.compile(r'conc_.*_amp')
    for idx, index in enumerate(indices):
        if idx == tcr_index:
            jac[idx, :] = 0.0
        elif conc_ptrn.match(index):
            jac[idx, idx] = conc_scale / tcr_val
            jac[idx, tcr_index] = - conc_scale * dyn_val.loc[index] / (tcr_val**2)

    cov = dyn_cov.to_numpy()
    new_cov = jac @ cov @ jac.T

    dyn_cov_new = pd.DataFrame(new_cov, index=dyn_cov.index, columns=dyn_cov.columns)

    amp_indices = dyn_val.filter(regex='conc_.*_amp').index.to_list()
    dyn_val_new = dyn_val.copy()
    dyn_val_new.loc[amp_indices] *= conc_scale / tcr_val

    dyn_val_new = dyn_val_new.to_frame().T
    dyn_val_new.index.name='Samples'

    return dyn_val_new, dyn_cov_new


data_dir = Path('fits')
out_dir = Path('fits_scaled')

for dv_file in data_dir.rglob('dyn_results.csv'):

    dv_in = pd.read_csv(dv_file, index_col=0).loc[0,:]
    dc_in = pd.read_csv(dv_file.parent / 'dyn_cov.csv', index_col=0)

    dv_out, dc_out = apply_scaling(dv_in, dc_in)

    curr_out = out_dir / dv_file.parent.parent.name / dv_file.parent.name
    curr_out.mkdir(exist_ok=True, parents=True)

    dv_out.to_csv(curr_out / 'dyn_results.csv')
    dc_out.to_csv(curr_out / 'dyn_cov.csv')
    shutil.copy(
        dv_file.parent / 'mapped_parameters.csv',
        curr_out / 'mapped_parameters.csv')

