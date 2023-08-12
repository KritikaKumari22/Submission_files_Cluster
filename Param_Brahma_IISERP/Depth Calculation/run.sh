#!/bin/bash

#SBATCH --job-name=kk_cDEPTH
#SBATCH --ntasks=100
#SBATCH --error=job.%J.err
#SBATCH --output=job.%J.out

cd $SLURM_SUBMIT_DIR

#module load iiser/apps/modeller/10.1
#module load python/3.9
module load cdac/DL_conda_3.7/3.7
module swap gnu8 cdac/compiler/gcc/10.2.0

old_ifs=$IFS
IFS='
'
for cmd in `cat cmd_list`
do
srun -N1 -n1 -c1 --exclusive bash -c ${cmd} &
done
wait
IFS=$old_ifs

