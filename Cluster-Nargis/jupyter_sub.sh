#!/bin/bash -l
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -N Jup_notbk
#$ -j y
#$ -o notbk_log.out
########################$ -q all.q
#$ -q all.q@compute-0-8.local 


echo "Starting MPI job at: " `date`
echo "Starting MPI job on: " `hostname`
echo "Total cores demanded: " $NSLOTS
echo "Job name given: " $JOB_NAME
echo "Job ID: " $JOB_ID
echo "Starting MPI job..."

conda activate /home/thattai/kritikak/.conda/envs/KK

jupyter lab --ip=0.0.0.0 --port=8889
