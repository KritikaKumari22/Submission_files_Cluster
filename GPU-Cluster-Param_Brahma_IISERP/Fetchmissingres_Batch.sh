#!/bin/bash
#SBATCH --job-name=kk_charpdbs
#SBATCH --error=/scratch/madhu/kritika/Depth//Filtered_pdbs//outputs/err/Job.%J.err
#SBATCH --output=/scratch/madhu/kritika/Depth//Filtered_pdbs//outputs/out/Job.%J.out
##SBATCH --ntasks=50
#SBATCH --time=6:00:00
#SBATCH --qos=array-job
#SBATCH --array=[1-9999]%90


cd /scratch/madhu/kritika/Depth/Filtered_pdbs/

module load DL_conda_3.7/3.7
N0=9999*0
SLURM_ARRAY_TASK_ID_0=$((SLURM_ARRAY_TASK_ID+N0))

#this test_list.txt contains arguments that are passed to script.py. (The number of subjobs would be equal to the number of lines in this list)
var0=$(sed -n "$SLURM_ARRAY_TASK_ID_0"p /scratch/madhu/kritika/Depth/Filtered_pdbs/nr30_list.txt)

python Param_get_chainbreaks.py $var0

wait
