#!/bin/bash -l
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -N Jup_notbk
#$ -l gpu=1
##################$ -pe mpirun 32
#$ -j y
#$ -o notbk_log.out
########################$ -q all.q
#$ -q all.q@gpunode-57


echo "Starting MPI job at: " `date`
echo "Starting MPI job on: " `hostname`
echo "Total cores demanded: " $NSLOTS
echo "Job name given: " $JOB_NAME
echo "Job ID: " $JOB_ID
echo "Starting MPI job..."

conda activate /home/thattai/kritikak/.conda/envs/KK

## Change the executable to match your path and executable filename (last line with ./xxx)
#python t.py

jupyter lab --ip=0.0.0.0 --port=8889
