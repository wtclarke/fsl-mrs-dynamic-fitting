#!/usr/bin/env python
import numpy as np
import os
import argparse
from subprocess import run

# Helper functions                                                                                                                  

def normalise(bvecs, bvals):
    # Normalise non zero bvecs 
    notzero = np.where(np.sum(np.abs(bvecs), axis=1)!=0)[0]
    bvecs[notzero, :] = bvecs[notzero, :] / np.linalg.norm(bvecs[notzero, :], axis=1, keepdims=True)
    # Scale all bvecs such that the norm is 1 for the max bval
    return bvecs * bvals[:, None] / max(bvals)

def generate_siemens(bvecs):
    # Produce the string                                                                                                            
    S  = f'[directions={bvecs.shape[0]}]\nCoordinateSystem = xyz\nNormalisation=none\n'
    for i,v in enumerate(bvecs):
        S += f'Vector[{i}] = ( {v[0]:1.5f}, {v[1]:1.5f}, {v[2]:1.5f}  )\n'
    return S

def savetxt(filename,textstring):
    with open(filename,'w') as f:
        f.write(textstring)

def run_gps(ndirs):
    tmp = os.popen('tmpnam').read().rstrip('\n')
    print('...Running GPS')
    result = run([
        'gps',
        f'--ndir={ndirs}',
        f'--out={tmp}'],
        capture_output=True,
        text=True)
    print(result.stdout)
    print(result.stderr)
    bvecs = np.loadtxt(tmp, ndmin=2)
    return bvecs



from itertools import chain, zip_longest
def ziplists(*args):
    return np.array([x for x in chain(*zip_longest(*args)) if x is not None])


def create_directions_file(bs,ndirs,nzeros,pairs,filename,stagger=False,save_bfiles=False):
    # start by running gps
    bvecs = []
    if len(nzeros) != len(ndirs):
        raise ValueError('please specify the frequency of b=0 for each shell')

    for ndir, nzero in zip(ndirs, nzeros):
        if nzero>0:
            # breakpoint()
            num_zeros = int(np.round(ndir / nzero))
            mod_ndir = ndir-num_zeros
        else:
            mod_ndir = ndir
            num_zeros = 0
        if pairs:
            # check ndirs is even, if not add one zero
            if mod_ndir % 2 > 0:
                mod_ndir -= 1
                num_zeros +=1
            mod_ndir /= 2
            mod_ndir = int(mod_ndir)

        print(mod_ndir)
        print(num_zeros)
        curr_bvec = run_gps(mod_ndir)
        if pairs:
            mod_ndir *= 2
            mod_ndir = int(mod_ndir)
            paired = np.empty((mod_ndir, 3), dtype=curr_bvec.dtype)
            paired[0::2, :] = curr_bvec
            paired[1::2, :] = curr_bvec * -1
            curr_bvec = paired
        insert_indices = np.floor(np.linspace(0, mod_ndir, num_zeros+1)).astype(int)
        insert_indices = insert_indices[:-1]
        print(insert_indices)
        curr_bvec = np.insert(curr_bvec, insert_indices, np.zeros((3)), axis=0)
        bvecs.append(curr_bvec)
    # create bvals                                                                                                                  
    bvals = [np.ones(i)*j for i,j in zip(ndirs,bs)]
    if stagger:
        bvals,bvecs = ziplists(*bvals),ziplists(*bvecs)
    else:
        bvals = np.concatenate(bvals)
        bvecs = np.concatenate(bvecs,axis=0)
    # save                                                                                                     
    #print(bvals)
    norm_bvecs = normalise(bvecs,bvals)
    savetxt(filename, generate_siemens(norm_bvecs))
    print(f'...Generated file {filename} with {bvecs.shape[0]} directions and {len(bs)} shells')

    if save_bfiles:
        np.savetxt(filename.rstrip('.txt')+'.bval',bvals)
        np.savetxt(filename.rstrip('.txt')+'.bvec',bvecs)
        
    return norm_bvecs

# MULTISHELL PROTOCOL FOR SPINAL CORD
# --> num dir not as important as num shells


#bs    = [5, 700, 1000, 1500, 2000]   # b-values
#ndirs = [4, 10,  20,   20,   20]     # directions per bvalue

#filename = '/home/fs0/saad/DirectionsSpinal_multishell.txt'


def main():
    p = argparse.ArgumentParser('Create Siemens Directions File')
    p.add_argument('-b','--bvals',  required=True,  type=float, help='b-shells',                   nargs='*')
    p.add_argument('-n','--ndirs',  required=True,  type=int,   help='Total directions per shell (inc b=0)',       nargs='*')
    p.add_argument('-z','--nzero',  required=False,  type=int,  help='Include a b=0 every n directions',  default=0, nargs='*')
    p.add_argument('-o','--out',    required=True,  type=str,   help='output file name')
    p.add_argument('-p','--pairs',  required=False,  action="store_true",   help='Make pairs of opposite b values, effectively halfs number of dirs')
    p.add_argument('--stagger',     required=False,             help='interleave the shells',      action='store_true')
    p.add_argument('--save_bfiles', required=False,             help='save FSL-style bvals/bvals', action='store_true')
    p.add_argument('--plot',  required=False,  action="store_true",   help='Visualise the b vectors')

    a = p.parse_args()
    if len(a.bvals) != len(a.ndirs) :
        raise(Exception('Numer of shells must match number of directions per shell'))

    bvecs = create_directions_file(a.bvals,a.ndirs,a.nzero,a.pairs,a.out,a.stagger,a.save_bfiles)

    if a.plot:
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter(bvecs[:,0], bvecs[:,1], -1.1 + 0*bvecs[:,2], c='b', s=1)
        ax.scatter(bvecs[:,0], 1.1 + 0*bvecs[:,1], bvecs[:,2], c='b', s=1)
        ax.scatter(-1.1 + 0*bvecs[:,0], bvecs[:,1], bvecs[:,2], c='b', s=1)
        ax.scatter(bvecs[:,0], bvecs[:,1], bvecs[:,2], c='k')
        ax.set_xlim([-1.1, 1.1])
        ax.set_ylim([-1.1, 1.1])
        ax.set_zlim([-1.1, 1.1])
        plt.show()
    

if __name__ == '__main__':
    main()
    

