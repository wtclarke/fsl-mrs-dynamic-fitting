#!/bin/sh

mkdir sim_results

for n in 9 18 36 72 144 288 576 1152
do
    for lw in 7.95 11.1 14.2 20.5
    do
        fsl_sub -q short.q python run_mc_editing.py 500 $n $lw sim_results
    done
done