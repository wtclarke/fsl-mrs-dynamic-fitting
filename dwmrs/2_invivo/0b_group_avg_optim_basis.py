# Make group average of all low b data

from pathlib import Path
from subprocess import run

from fsl_mrs.utils import mrs_io
from fsl_mrs.core import nifti_mrs as ntools
from fsl_mrs.utils.preproc import nifti_mrs_proc as nproc

data_path = Path('nifti')

data_list = []
for file in data_path.rglob('*.nii.gz'):
    curr_file = mrs_io.read_FID(file)
    low_b, _ = ntools.split(curr_file, dimension='DIM_USER_0', index_or_indicies=0)
    low_b.set_dim_tag('DIM_USER_0', 'DIM_DYN')
    data_list.append(low_b)

merged = ntools.merge(data_list, dimension='DIM_DYN')

aligned = nproc.align(merged, 'DIM_DYN', ppmlim=(0, 4.0), apodize=0)
averaged = nproc.average(aligned, 'DIM_DYN')
averaged.save('group_avg_low_b')

# Create basis with combined peaks
basis = mrs_io.read_basis('basis')
tcr_basis = basis.original_basis_array[:, basis.names.index('Cr')] + basis.original_basis_array[:, basis.names.index('PCr')]
basis.add_fid_to_basis(tcr_basis, 'Cr+PCr')
tcho_basis = basis.original_basis_array[:, basis.names.index('PCho')] + basis.original_basis_array[:, basis.names.index('GPC')]
basis.add_fid_to_basis(tcho_basis, 'PCho+GPC')
basis.remove_fid_from_basis('Cr')
basis.remove_fid_from_basis('PCr')
basis.remove_fid_from_basis('PCho')
basis.remove_fid_from_basis('GPC')
basis.save('basis_combined', overwrite=True)

# Run fitting
run([
    'fsl_mrs',
    '--data', 'group_avg_low_b.nii.gz',
    '--basis', 'basis_combined',
    '--output', 'basis_optim_fit',
    '--free_shift',
    '--metab_groups', 'MM_WT_',
    '--internal_ref', 'Cr+PCr',
    '--report',
    '--overwrite'])

# Optimisation
run([
    'basis_tools',
    'shift_all',
    'basis_combined',
    'basis_optim_fit',
    'basis_optim'])
