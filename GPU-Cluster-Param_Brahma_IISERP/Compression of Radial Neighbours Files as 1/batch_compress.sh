#!/bin/bash
#SBATCH --job-name=K_7.5cmprsd
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --error=/scratch/madhu/kritika/Depth/compressd_nbrs/Job.%J.err
#SBATCH --output=/scratch/madhu/kritika/Depth/compressd_nbrs/compressd.%J.out
#SBATCH --time=96:00:00



cd /scratch/madhu/kritika/Depth/compressd_nbrs

module load cdac/DL_conda_3.7/3.7



python3 Clean.py



