#!/bin/bash
#SBATCH --job-name=kk_plt
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --error=/scratch/madhu/kritika/Depth/distribution/job.%J.err
#SBATCH --output=/scratch/madhu/kritika/Depth/distribution/job.%J.out
#SBATCH --time=96:00:00


cd /scratch/madhu/kritika/Depth/distribution/

module load cdac/DL_conda_3.7/3.7
export MKL_THREADING_LAYER=GNU

python3 plt.py



