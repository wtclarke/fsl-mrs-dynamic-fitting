from pathlib import Path
import argparse

from scipy.io import loadmat
import numpy as np

from fsl_mrs.utils import preproc as proc
from fsl_mrs.core import nifti_mrs as ntools

dwell_time = 0.0002
bw = 1/dwell_time
cf = 500.3


def process_single(single_dir):
    bval = []
    fid_list = []
    for file in single_dir.glob('*.mat'):
        bval.append(float(file.stem.lstrip('high_b_'))*0.001)
        tmpload = loadmat(file)
        fid = tmpload['soustraction'].squeeze().conj()
        fid = proc.hlsvd(fid, dwell_time, cf, [-0.35, 0.35])
        fid = proc.phaseCorrect(fid, bw, cf)[0]
        fid[0] *= 2.0
        fid = proc.applyLinPhase(
            fid,
            np.linspace(-bw/2, bw, len(fid)),
            -0.061E-3)
        fid_list.append(fid)


    fid_list, phs, freq = proc.phase_freq_align(
        fid_list,
        bw,
        cf,
        ppmlim=(0.2, 4.0),
        niter=4,
        apodize=0)

    fid_list = [x for _, x in sorted(zip(bval, fid_list))]
    bval = sorted(bval)

    fixed_shift = proc.shiftToRef(
        fid_list[0],
        2.01,
        bw,
        cf,
        ppmlim=(1.8, 2.2))[1]

    fid_list = [proc.freqshift(ff, dwell_time, -fixed_shift * cf) for ff in fid_list]
    fid_list = np.stack(fid_list).T
    fid_list = fid_list.reshape(((1, 1, 1,) + fid_list.shape))
    nifti_obj = ntools.create_nmrs.gen_nifti_mrs(
        fid_list,
        dwell_time,
        cf,
        dim_tags=['DIM_USER_0', None, None])

    nifti_obj.set_dim_tag(
        'DIM_USER_0',
        'DIM_USER_0',
        'b-value increment',
        {'b_value': {'Value': bval, 'Description': 'b-value in ms.μm^-2'}})

    return nifti_obj


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Convert and pre-process dwMRS mouse datasets in a directory")

    parser.add_argument('dir', type=Path, help='Directory containing datasets')
    parser.add_argument('output', type=Path, help='Directory to output data')
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)

    for child in args.dir.iterdir():
        if child.is_dir():
            print(child.name)
            process_single(child).save(args.output / child.name)


if __name__ == '__main__':
    main()
