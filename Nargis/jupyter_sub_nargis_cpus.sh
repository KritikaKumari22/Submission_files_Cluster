#!/bin/bash -l
#$ -S /bin/bash
#$ -cwd
#$ -V

## Change the name below (after -N) to suite your requirement
#$ -N KK

# Change the number of cores demanded (after orte) to suite your code-run requirement
#$ -pe orte 64
## Change the name below (after -o and -e ) to output and error log files, here the error file will have the info for the URL to load Jupyter on Browser
#$ -o notbk_result.out
#$ -e notbk_error.out

## set the queue depending on Job run time.
#$ -q all.q

## Email address to send email to
#$ -M kritikak@ncbs.res.in

## To send email when job ends or aborts
#$ -m ea

echo "Starting MPI job at: " `date`
echo "Starting MPI job on: " `hostname`
echo "Total cores demanded: " $NSLOTS
echo "Job name given: " $JOB_NAME
echo "Job ID: " $JOB_ID
echo "Starting MPI job..."

#module load /softwares/miniconda/bin/python3.9
#source activate KK #Load your Environment
module load /softwares/miniconda/bin/python3.9
conda activate /home/thattai/kritikak/.conda/envs/KK

cd /home/thattai/kritikak

## Change the executable to match your path and executable filename (last line with ./xxx)
#python t.py

jupyter lab --ip=0.0.0.0 --port=8888