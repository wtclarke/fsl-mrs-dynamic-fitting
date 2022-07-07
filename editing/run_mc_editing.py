import argparse
import numpy as np
import pandas as pd

from fsl_mrs.utils import mrs_io
from fsl_mrs.utils import synthetic as syn
from fsl_mrs.utils.fitting import fit_FSLModel
from fsl_mrs.core import MRS
from fsl_mrs import dynamic as dyn
from pathlib import Path

parser = argparse.ArgumentParser(
    description='Run montecarlo editing simulation.')
parser.add_argument('mc_reps', metavar='N', type=int,
                    help='Number of montecarlo reps')
parser.add_argument('noise_lvl', type=float,
                    help='Noise variance')
parser.add_argument('linewidth', type=float,
                    help='Lorentzian line broadening.')
parser.add_argument('output_dir', type=Path,
                    help='Output dir')

args = parser.parse_args()

basis_on = mrs_io.read_basis('basis_sets/uzay_svs_mpress_68_res_60_on/')
basis_off = mrs_io.read_basis('basis_sets/uzay_svs_mpress_68_res_60_off/')
basis_diff = mrs_io.read_basis('basis_sets/uzay_svs_mpress_68_res_60_diff/')


def synthesize(basis, noise, lw, conc):
    synthesised = syn.synthetic_from_basis.syntheticFromBasisFile(
        basis,
        broadening=lw,
        noisecovariance=[[noise]],
        concentrations=conc)
    mrs = synthesised[1]
    mrs.FID = synthesised[0]
    concs_out = synthesised[2]
    return mrs, concs_out


def synthesize_diff(mrs_on, mrs_off):
    fid_diff = mrs_on.FID - mrs_off.FID\
         * (mrs_on.scaling['basis'] / mrs_off.scaling['basis'])
    mrs_diff = MRS(
        FID=fid_diff,
        cf=mrs_on.centralFrequency,
        bw=mrs_on.bandwidth,
        basis=basis_diff)
    mrs_diff.keep = ['NAA', 'NAAG', 'GABA', 'GSH', 'Glu', 'Gln']
    mrs_diff.processForFitting()
    return mrs_diff


def run_iteration(lw, noise):

    # Create an instance of data:
    # 1. The ON condition
    syn_mrs_on, on_concs = synthesize(basis_on, noise, lw, {'GABA': 3.5})
    # 2. The OFF condition
    syn_mrs_off, _ = synthesize(basis_off, noise, lw, on_concs)
    # 3. The OFF condition, but double the acqusition time (sqrt(2) less noise)
    syn_mrs_off_equiv, _ = synthesize(basis_off, noise / 1.4, lw, on_concs)
    # 4. The difference spectrum
    syn_mrs_diff = synthesize_diff(syn_mrs_on, syn_mrs_off)

    # Run the fitting
    # Fitting options
    mg = [0, ] * len(on_concs)
    fitargs = {
        'model': 'lorentzian',
        'baseline_order': 0,
        'metab_groups': mg}
    fitargs_diff = {
        'model': 'lorentzian',
        'baseline_order': 0,
        'metab_groups': [0, ] * 6}

    # Run individual fits
    res_on = fit_FSLModel(syn_mrs_on, **fitargs,)
    res_off = fit_FSLModel(syn_mrs_off, **fitargs)
    res_off_equiv = fit_FSLModel(syn_mrs_off_equiv, **fitargs)
    res_diff = fit_FSLModel(syn_mrs_diff, **fitargs_diff)

    on_off_to_diff_scaling = \
        (syn_mrs_diff.scaling['basis'] / syn_mrs_on.scaling['basis'])\
        * (syn_mrs_on.scaling['FID'] / syn_mrs_diff.scaling['FID'])

    # Extract individual concnetration parameters
    df_res = pd.concat(
        (res_off.getConc(function=None),
         res_off_equiv.getConc(function=None),
         res_on.getConc(function=None),
         res_diff.getConc(function=None) * on_off_to_diff_scaling))
    df_res.set_index(
        np.array(['Off', 'Off Matched', 'On', 'Diff']),
        inplace=True)

    # Run dynamic fitting
    mrs_list = [syn_mrs_off, syn_mrs_on]
    tvar = [0, 1]
    dyn_obj = dyn.dynMRS(
        mrs_list,
        tvar,
        'editconfig.py',
        rescale=False,
        **fitargs)
    dyn_res = dyn_obj.fit()

    # Extract dynamic concentration parameters
    df_dyn = dyn_res.dataframe_free.filter(like='conc', axis=1)
    df_dyn.columns = df_res.columns[:-1]
    df_dyn.set_index(np.array(['Dyn']), inplace=True)

    return pd.concat((df_res, df_dyn)),\
        {'dyn': dyn_res,
         'diff': (syn_mrs_diff, res_diff),
         'off': (syn_mrs_off_equiv, res_off_equiv)}


df_container = []
for idx in range(args.mc_reps):
    df_container.append(
        run_iteration(
            (args.linewidth, 0),
            args.noise_lvl)[0])
df = pd.concat(df_container, axis=0, keys=np.arange(0, len(df_container)))

out_str = f'noise_{args.noise_lvl:04.0f}_lw_{args.linewidth:0.0f}.csv'
df.to_csv(
    args.output_dir / out_str)
